from opsdroid.skill import Skill
from opsdroid.matchers import match_regex, match_always
import logging

FILENAME = "/usr/src/app/blastfile.txt"

class BlastSkill(Skill):

    def __init__(self, opsdroid, config):
        super(BlastSkill, self).__init__(opsdroid, config)
        with open(FILENAME, 'w') as f:
            f.write('!blast');
        logging.debug(f'Loaded blast skill')

    @match_regex(r'^!blast')
    async def blast(self, message):
        with open(FILENAME, 'w') as f:
            f.write(message.user);
        logging.debug(f'updated blastfile with {message.user}')
        await message.respond(f'updated blastfile with {message.user}')
