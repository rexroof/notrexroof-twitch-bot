from opsdroid.skill import Skill
from opsdroid.matchers import match_regex, match_always
from voluptuous import Required
import logging

CONFIG_SCHEMA = {
    Required("filename", default="/usr/src/app/blastfile.txt"): str,
}

class BlastSkill(Skill):

    def __init__(self, opsdroid, config):
        super(BlastSkill, self).__init__(opsdroid, config)
        self.filename = config["filename"]
        with open(self.filename, 'w') as f:
            f.write('!blast');
        logging.debug(f'Loaded blast skill')

    @match_regex(r'^!blast')
    async def blast(self, message):
        with open(self.filename, 'w') as f:
            f.write(message.user);
        logging.debug(f'updated blastfile with {message.user}')
        await message.respond(f'updated blastfile with {message.user}')
