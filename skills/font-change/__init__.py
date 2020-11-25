from opsdroid.skill import Skill
from opsdroid.matchers import match_regex, match_always
import yaml
import logging
import os


class FontChange(Skill):
    def __init__(self, opsdroid, config):
        self.yamlfile = os.getenv("ALACRITTY_YAML", "/usr/src/app/alacritty.yml")
        super(FontChange, self).__init__(opsdroid, config)
        logging.debug(f"Loaded font-change skill")

    def font_size(self, size):
        with open(self.yamlfile, 'r+') as file:
            yamlconfig = yaml.load(file, Loader=yaml.FullLoader)
            yamlconfig['font']['size'] = int(size)
            file.seek(0)
            yaml.dump(yamlconfig, file)
            file.truncate()

    def font_face(self, face):
        with open(self.yamlfile, 'r+') as file:
            yamlconfig = yaml.load(file, Loader=yaml.FullLoader)
            yamlconfig['font']['normal']['family'] = face
            file.seek(0)
            yaml.dump(yamlconfig, file)
            file.truncate()

    @match_regex(r"^!font face (.+)$")
    async def chat_face(self, message):
        face = message.regex.group(1)
        self.font_face(face)
        await message.respond(f'tried to change face to "{face}"')

    @match_regex(r"^!font size ([\d]+)")
    async def chat_size(self, message):
        size = message.regex.group(1)
        self.font_size(size)
        await message.respond(f'tried to change size to "{size}"')
