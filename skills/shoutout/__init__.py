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

    @match_regex(r"^#\s*addso (?P<streamer>[\w]+) (?P<response>.+)$")
    @constrain_users(["rexroof"])
    async def shoutout_add(self, message):
        streamer = message.regex.group("streamer").lower()
        response = message.regex.group("response")
        shoutout = await self.opsdroid.memory.get("shoutout")
        if shoutout == None:
            shoutout = {}

        if streamer in shoutout:
            await message.respond(
                f"replacing shoutout for https://twitch.tv/{streamer}"
            )
        else:
            await message.respond(
                f"creating new shoutout for https://twitch.tv/{streamer}"
            )
        shoutout[streamer] = response
        await self.opsdroid.memory.put("shoutout", shoutout)

    @match_regex(r"^#\s*(shoutout|so) (?P<streamer>[\w]+)")
    async def print_shoutout(self, message):
        streamer = message.regex.group("streamer").lower()
        shoutout = await self.opsdroid.memory.get("shoutout")
        shoutout_counts = await self.opsdroid.memory.get("shoutout_counts")
        if streamer in shoutout:
            await message.respond(
                f"rex says: {shoutout[streamer]} https://twitch.tv/{streamer}"
            )
        else:
            await message.respond(f"no shoutout recorded for {streamer}!")
