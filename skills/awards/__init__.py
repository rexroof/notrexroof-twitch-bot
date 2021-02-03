from datetime import datetime
from io import BytesIO
from opsdroid.matchers import match_regex, match_always
from opsdroid.skill import Skill
from PIL import Image, ImageFont, ImageDraw
import logging
import random

# import requests
import subprocess
import re
import os


class Awards(Skill):
    def __init__(self, opsdroid, config):
        super(Awards, self).__init__(opsdroid, config)

        self.w = 1280
        self.h = 720
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        self.award_file = self.cwd + "/" + "award.png"
        self.background_file = "/tmp/bottmp/" + "background.png"
        self.font_file = self.cwd + "/" + "font.ttf"

        logging.debug(f"Loaded awards skill")

    # return only kinda random spots to maybe spread out images
    def kinda_random(self, low=1, high=256, scale=10):
        spread = high - low
        x = random.randint(0, scale)
        return int(low + (x * (spread / 10)))

    def font_bytes(self):
        # this font is too slow to dl.  should cache it.
        # req = requests.get("https://github.com/googlefonts/Pacifico/blob/master/fonts/Pacifico-Regular.ttf?raw=true")
        # return BytesIO(req.content)
        return self.font_file

    async def award_image(self, username="none", course="what course?"):
        now = datetime.now()
        today = now.strftime("%b%d,%Y")

        # these will come from vars/env
        user_color = "#2f3490"
        course_color = "#ff0000"
        award_template = self.award_file

        # creating a image object
        image = Image.open(award_template)
        draw = ImageDraw.Draw(image)
        userfont = ImageFont.truetype(self.font_bytes(), 200)
        coursefont = ImageFont.truetype(self.font_bytes(), 110)
        otherfont = ImageFont.truetype(self.font_bytes(), 75)

        draw.text((250, 380), username, font=userfont, fill=user_color, align="left")
        draw.text((350, 680), course, font=coursefont, fill=course_color, align="left")
        draw.text((1100, 825), today, font=otherfont, fill="black", align="left")
        draw.text(
            (450, 825), "twitch.tv/rexroof", font=otherfont, fill="black", align="left"
        )

        return image

    async def blank_background(self):
        background = Image.new("RGBA", (self.w, self.h))  # my obs canvas
        background.save(self.background_file)

    async def add_image(self, username="none"):
        if not os.path.exists(self.background_file):
            await self.blank_background()

        bg = Image.open(self.background_file)
        award = await self.award_image(username, "what is a k8s?")
        award.thumbnail((self.w / 4, self.h / 4), Image.NEAREST)
        tmpw, tmph = award.size
        bg.paste(
            award,
            (self.kinda_random(1, self.w - tmpw), self.kinda_random(1, self.h - tmph)),
        )
        bg.save(self.background_file)

    @match_regex(r"^#\s*claim")
    async def claim_award(self, message):
        logging.debug(f"{message.user} claim_award")
        logging.debug(os.getcwd())
        logging.debug(os.path.dirname(os.path.realpath(__file__)))
        await self.add_image(message.user)

    @match_regex(r"^#\s*wipeawards")
    async def wipe_background(self, message):
        logging.debug(f"{message.user} wipe_background")
        await self.blank_background()
