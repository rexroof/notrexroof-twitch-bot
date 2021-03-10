# import random
# import re
# from datetime import datetime, timedelta
# from opsdroid.matchers import match_regex, match_event, match_always


import logging
from opsdroid.matchers import match_regex
from opsdroid.skill import Skill
from opsdroid.constraints import constrain_users

# from opsdroid.events import JoinRoom

# simple skill to record custom "shoutouts"

#  should I count how many times someone has been shouted out?


class ShoutOut(Skill):
    def __init__(self, opsdroid, config):
        super(ShoutOut, self).__init__(opsdroid, config)
        logging.debug(f"Loaded ShoutOut skill")

    def new_streamer(self, obj, username):
        if obj is None:
            obj = {}
        if username not in obj:
            obj[username] = {"msg": "", "count": 0}
        return obj

    @match_regex(r"^#\s*(soadd|addso) (?P<streamer>[\w]+) (?P<response>.+)$")
    @constrain_users(["rexroof"])
    async def shoutout_add(self, message):
        streamer = message.regex.group("streamer").lower()
        response = message.regex.group("response")
        shoutout = await self.opsdroid.memory.get("shoutout")
        shoutout = self.new_streamer(shoutout, streamer)

        shoutout[streamer]["msg"] = response
        await message.respond(f"replaced shoutout for https://twitch.tv/{streamer}")
        await self.opsdroid.memory.put("shoutout", shoutout)

    @match_regex(r"^#\s*(shoutout|so) (?P<streamer>[\w]+)")
    async def print_shoutout(self, message):
        streamer = message.regex.group("streamer").lower()
        shoutout = await self.opsdroid.memory.get("shoutout")
        shoutout = self.new_streamer(shoutout, streamer)

        stmr = shoutout[streamer]
        stmr["count"] += 1
        s = "s"
        if stmr["count"] == 1:
            s = ""
        if stmr["msg"]:
            await message.respond(
                f'rex says: {stmr["msg"]} https://twitch.tv/{streamer} ({streamer} has been shouted out {stmr["count"]} time{s})'
            )
        else:
            await message.respond(
                f'rex says: if you aren\'t watching and following {streamer}, what are you even doing?  https://twitch.tv/{streamer} ({streamer} has been shouted out {stmr["count"]} time{s})'
            )
        await self.opsdroid.memory.put("shoutout", shoutout)
