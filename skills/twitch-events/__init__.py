from opsdroid.skill import Skill
from opsdroid.matchers import match_event
from opsdroid.connector.twitch.events import UserFollowed, StreamStarted, StreamEnded
from opsdroid.events import Message
import logging


class TwitchEvents(Skill):
    def __init__(self, opsdroid, config):
        super(TwitchEvents, self).__init__(opsdroid, config)
        logging.debug(f"Loaded twitch-events skill")

    @match_event(UserFollowed)
    async def user_followed(self, event):
        await event.connector.send(Message(f"thanks for the follow, {event.follower}!"))
        logging.debug(event)

    @match_event(StreamStarted)
    async def stream_started(self, event):
        await event.connector.send(Message(f"lets go!"))
        logging.debug(event)

    @match_event(StreamEnded)
    async def stream_ended(self, event):
        await event.connector.send(Message(f"have a great day, everyone!"))
        logging.debug(event)
