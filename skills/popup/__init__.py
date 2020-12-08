from opsdroid.skill import Skill
from opsdroid.matchers import match_regex, match_always
import logging
import subprocess
import re


class Popup(Skill):
    def __init__(self, opsdroid, config):
        super(Popup, self).__init__(opsdroid, config)
        logging.debug(f"Loaded popup skill")

    @match_regex(r"^!popup")
    async def simple_popup(self, message):
        completed = subprocess.run(["su", "rex", "-c", 
            "tmux list-clients"
            ], capture_output=True)
        stdout = completed.stdout.decode('utf-8')
        # grabbing the pty for twitch client
        matches = re.search('^(/[^:]+): (?=twitch.)', stdout, re.MULTILINE)
        pty = matches.group(0)
        subprocess.run(
            [
                "su",
                "rex",
                "-c",
                # f"tmux popup -c {pty} -w95 -h6 -K -R 'toilet -t -f future $(date)'",
                f"tmux popup -c {pty} -K -R 'toilet -t -f future $(date)'",
            ]
        )
        await message.respond(f"generated a popup!")
