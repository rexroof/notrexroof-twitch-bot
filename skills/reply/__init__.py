from opsdroid.skill import Skill
from opsdroid.matchers import match_regex, match_always
import logging


class Reply(Skill):

    def __init__(self, opsdroid, config):
        super(Reply, self).__init__(opsdroid, config)
        logging.debug(f'Loaded reply skill')

    @match_regex(r'^%(?P<token>[\w]+)')
    async def find_replies(self, message):
        token = message.regex.group('token')
        replies = await self.opsdroid.memory.get("replies")
        if replies == None or token not in replies:
            logging.debug(f'replies: did not find {token}')
        else:
            await message.respond(f'{replies[token]}')

    @match_regex(r'^!reply to %([\w]+) with (.+)$')
    async def reply_record(self, message):
        key = message.regex.group(1)
        response = message.regex.group(2)
        replies = await self.opsdroid.memory.get("replies")
        if replies == None:
            replies = {}
        replies[key] = response
        await self.opsdroid.memory.put("replies", replies)
        await message.respond(f'wrote "{key}" to memory')
