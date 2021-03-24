from opsdroid.skill import Skill
from opsdroid.matchers import match_regex, match_always
from opsdroid.constraints import constrain_users
import logging
import re


class Reply(Skill):
    def __init__(self, opsdroid, config):
        super(Reply, self).__init__(opsdroid, config)
        logging.debug(f"Loaded reply skill")

    @match_always
    async def token_reply(self, message):
        if hasattr(message, "text"):
            mat = re.match(r"^#\s*(?P<token>[\w]+)", message.text)
            if hasattr(mat, "group") and mat.group("token"):
                token = mat.group("token")
                replies = await self.opsdroid.memory.get("replies")
                if replies != None and token in replies:
                    # running this to possibly convert this item
                    replies = self.new_reply(replies, token)

                    replies[token]["count"] += 1
                    text = replies[token]["text"]

                    _user = message.user
                    _count = replies[token]["count"]

                    try:
                        result = text.format(user=_user, count=_count)
                    except KeyError as e:
                        logging.debug(f"reply keyerror {e}")
                        result = text
                    except ValueError as e:
                        logging.debug(f"reply valueerror {e}")
                        result = text
                    except Exception as e:
                        logging.debug(f"uncaught reply error {e}")
                        result = text

                    # add formats
                    #  - username
                    #  - counter
                    #  - arg to command? $1 & $2 ?
                    # add multiple replies, randomly choose between each

                    await self.opsdroid.memory.put("replies", replies)
                    await message.respond(result)

    def new_reply(self, replies, key):
        if replies == None:
            replies = {}
        if key not in replies:
            replies[key] = {"count": 0, "text": ""}

        # add block to convert
        if isinstance(replies[key], str):
            replies[key] = {"count": 0, "text": replies[key]}
        return replies

    @match_regex(r"^#\s*reply to #(?P<key>[\w]+) with (?P<response>.+)$")
    @constrain_users(["rexroof"])
    async def reply_record(self, message):
        key = message.regex.group("key")
        response = message.regex.group("response")
        replies = await self.opsdroid.memory.get("replies")
        replies = self.new_reply(replies, key)
        replies[key]["text"] = response
        await self.opsdroid.memory.put("replies", replies)
        await message.respond(f'wrote "{key}" to memory')

    @match_regex(r"^#\s*delete reply !(?P<key>[\w]+)")
    @constrain_users(["rexroof"])
    async def reply_del(self, message):
        key = message.regex.group("key")
        replies = await self.opsdroid.memory.get("replies")
        if replies == None:
            replies = {}
            await message.respond(f'"{key}" does not exist')
        else:
            ret = replies.pop(key, None)
            if ret == None:
                await message.respond(f'"{key}" does not exist')
            else:
                await self.opsdroid.memory.put("replies", replies)
                await message.respond(f'deleted "{key}" from memory')

    @match_regex(r"^#\s*list replies")
    async def reply_list(self, message):
        replies = await self.opsdroid.memory.get("replies")
        if replies == None:
            await message.respond(f"no replies found")
        else:
            cmds = [f"#{k}" for k in replies]
            logging.debug(" ".join(cmds))
            await message.respond(" ".join(cmds))
