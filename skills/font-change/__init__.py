from opsdroid.skill import Skill
from opsdroid.matchers import match_regex, match_always
from opsdroid.constraints import constrain_users
from voluptuous import Required
import yaml
import logging
import os

CONFIG_SCHEMA = {
    Required("max_font_size", default=45): int,
    Required("min_font_size", default=6): int,
}


class FontChange(Skill):
    def __init__(self, opsdroid, config):
        self.yamlfile = os.getenv("ALACRITTY_YAML", "/usr/src/app/alacritty.yml")
        super(FontChange, self).__init__(opsdroid, config)
        self.max_font_size = config["max_font_size"]
        self.min_font_size = config["min_font_size"]
        logging.debug(f"Loaded font-change skill")

    def font_size(self, size):
        with open(self.yamlfile, "r+") as file:
            yamlconfig = yaml.load(file, Loader=yaml.FullLoader)
            yamlconfig["font"]["size"] = size
            file.seek(0)
            yaml.dump(yamlconfig, file)
            file.truncate()

    def font_face(self, face):
        with open(self.yamlfile, "r+") as file:
            yamlconfig = yaml.load(file, Loader=yaml.FullLoader)
            yamlconfig["font"]["normal"]["family"] = face
            file.seek(0)
            yaml.dump(yamlconfig, file)
            file.truncate()

    @match_regex(r"^#\s*font face (.+)$")
    @constrain_users(["rexroof"])
    async def chat_face(self, message):
        face = message.regex.group(1)
        self.font_face(face)
        await message.respond(f'tried to change face to "{face}"')

    @match_regex(r"^#\s*font smaller")
    async def smaller(self, message):
        with open(self.yamlfile, "r+") as file:
            yamlconfig = yaml.load(file, Loader=yaml.FullLoader)
            yamlconfig["font"]["size"] -= 2
            file.seek(0)
            yaml.dump(yamlconfig, file)
        logging.info(f"{message.user} made font smaller")

    @match_regex(r"^#\s*font bigger")
    async def bigger(self, message):
        with open(self.yamlfile, "r+") as file:
            yamlconfig = yaml.load(file, Loader=yaml.FullLoader)
            yamlconfig["font"]["size"] += 2
            file.seek(0)
            yaml.dump(yamlconfig, file)
            file.truncate()
        logging.info(f"{message.user} made font bigger")

    @match_regex(r"^#\s*font size ([\d]+)")
    async def chat_size(self, message):
        size = int(message.regex.group(1))

        if size >= self.min_font_size and size <= self.max_font_size:
            self.font_size(size)
            logging.info(f"{message.user} set font to {size}")
        else:
            await message.respond(
                f"size must be between {self.min_font_size} and {self.max_font_size}"
            )
