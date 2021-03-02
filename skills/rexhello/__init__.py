import random
import logging
from datetime import datetime, timedelta

from opsdroid.matchers import match_regex
from opsdroid.skill import Skill

# potentially toggle hello/goodbye without timeouts
# case insensitive matches?
# update patterns and responses, make them more rexish, or rexy, or rexington


class RexHello(Skill):
    def __init__(self, opsdroid, config):
        super(RexHello, self).__init__(opsdroid, config)
        self.timepast = timedelta(hours=2)
        logging.debug(f"Loaded rexhello skill")

    @match_regex(r"hi|hello|hey|hallo|good morning|good afternoon|howdy")
    async def hello(self, message):
        lasthello = await self.opsdroid.memory.get("lasthello")
        if lasthello == None:
            lasthello = {}

        willsend = False

        if message.user in lasthello:
            if (lasthello[message.user] + self.timepast) < datetime.now():
                willsend = True
        else:
            willsend = True

        if willsend:
            text = random.choice(["Hi {}", "Hello {}", "howdy {}"]).format(message.user)
            await message.respond(text)
            lasthello[message.user] = datetime.now()
            await self.opsdroid.memory.put("lasthello", lasthello)

    @match_regex(r"bye( bye)?|see y(a|ou)|au revoir|gtg|I(\')?m off")
    async def goodbye(self, message):
        lastgoodbye = await self.opsdroid.memory.get("lastgoodbye")
        if lastgoodbye == None:
            lastgoodbye = {}
        willsend = False

        if message.user in lastgoodbye:
            if (lastgoodbye[message.user] + self.timepast) < datetime.now():
                willsend = True
        else:
            willsend = True

        if willsend:
            text = random.choice(
                ["Bye {}", "See you {}", "no worries, have a good day {}"]
            ).format(message.user)
            await message.respond(text)
            lastgoodbye[message.user] = datetime.now()
            await self.opsdroid.memory.put("lastgoodbye", lastgoodbye)
