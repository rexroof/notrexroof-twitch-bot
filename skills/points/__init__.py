import random
import re
import logging
from datetime import datetime, timedelta

from opsdroid.matchers import match_regex, match_event, match_always
from opsdroid.skill import Skill
from opsdroid.events import JoinRoom

# update hellos to make them more rexish, or rexy, or rexington
# maybe restrict points given/taken per minute/hour?


class Points(Skill):
    def __init__(self, opsdroid, config):
        super(Points, self).__init__(opsdroid, config)
        logging.debug(f"Loaded Points skill")

    # initialize points object and a new user
    def new_user(self, points, user):
        if points == None:
            points = {}
        if user not in points:
            points[user] = {"joined": None, "points": 0, "lastchat": None}
        return points

    @match_event(JoinRoom)
    async def user_joined(self, event):
        if not event.user:
            return
        points = await self.opsdroid.memory.get("points")
        points = self.new_user(points, event.user)
        points[event.user]["joined"] = datetime.now()
        await self.opsdroid.memory.put("points", points)

    @match_always
    async def chatted(self, message):
        # if this is a normal chat message, not events
        if hasattr(message, "text"):
            points = await self.opsdroid.memory.get("points")
            points = self.new_user(points, message.user)
            # say hi if first time seeing this user in a while, suggest a random command?
            lastchat = points[message.user]["lastchat"]
            if (lastchat is None) or ((lastchat + timedelta(hours=6)) < datetime.now()):
                text = random.choice(["Hi {}", "Hello {}", "howdy {}"]).format(
                    message.user
                )
                await message.respond(text)

            points[message.user]["lastchat"] = datetime.now()
            await self.opsdroid.memory.put("points", points)

    @match_regex(r"([+]{2}|[-]{2})", matching_condition="search")
    # I used to do this with a bigger regex... but this is easier and simpler to read
    async def parse_add_subtract(self, message):
        is_user = re.compile(r"[a-z0-9][\w]{2,24}")  # looks like twitch id
        changed = []
        for word in message.text.lower().split():
            amt = 0
            if word.endswith("--") or word.startswith("--"):
                amt = -1
            if word.endswith("++") or word.startswith("++"):
                amt = 1
            # remove plusses/minuses
            word = re.sub("[+-]", "", word)
            if amt != 0 and is_user.search(word):
                if await self.add_to_points(word, amt):
                    changed.append(word)
        if changed:
            await message.respond("assigned points to " + " ".join(set(changed)))

    @match_regex(r"^#\s*points(\s*(?P<u>[a-z0-9][\w]{2,24}))?")
    async def respond_points(self, message):
        target = message.user
        if message.regex.group("u"):
            target = message.regex.group("u")
        p = await self.get_points(target)
        s = "s"
        if p == 1:
            s = ""
        await message.respond(f"{target} has {p} point{s}")

    async def get_points(self, user):
        points = await self.opsdroid.memory.get("points")
        if user in points:
            return points[user]["points"]
        else:
            return 0

    async def add_to_points(self, user, amount):
        points = await self.opsdroid.memory.get("points")
        if user in points:
            before = points[user]["points"]
            points[user]["points"] += amount
            after = points[user]["points"]
            logging.debug(f"{user} went from {before} to {after}")
            await self.opsdroid.memory.put("points", points)
            return True
        else:
            return False
