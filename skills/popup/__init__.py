from opsdroid.skill import Skill
from opsdroid.matchers import match_regex, match_always
import logging
import subprocess

import re

class Popup(Skill):
    def __init__(self, opsdroid, config):
        super(Popup, self).__init__(opsdroid, config)
        logging.debug(f"Loaded popup skill")

    async def tmux_popup(self, cmd):
        completed = subprocess.run(["su", "rex", "-c", 
            "tmux list-clients"
            ], capture_output=True)
        stdout = completed.stdout.decode('utf-8')
        stderr = completed.stderr.decode('utf-8')
        retcode = completed.returncode
        # check retcode, print stderr.

        if retcode != 0:
            logging.warning(f"retcode is {retcode}")

        if stderr:
            logging.debug(f"stderr is {stderr}")

        # grabbing the pty for twitch client
        matches = re.search('^(/[^:]+): (?=twitch.)', stdout, re.MULTILINE)
        pty = matches.group(0)

        completed = subprocess.Popen(
            [
                "su",
                "rex",
                "-c",
                f"tmux popup -c {pty} -w 80% -h 80% -K -R '{cmd}'"
            ]
        )
        return completed.returncode

    @match_regex(r"^#\s*aquarium")
    async def aquarium(self, message):
        await self.tmux_popup("docker run --rm -t wernight/funbox timeout --preserve-status -s 9 10 asciiquarium")

    @match_regex(r"^#\s*steam train")
    async def train(self, message):
        await self.tmux_popup("docker run --rm -t wernight/funbox sl")

    @match_regex(r"^#\s*(kubectl|k) get pod")
    async def kgetpods(self, message):
        await self.tmux_popup("kubectl get pods")

    @match_regex(r"^#\s*popup date")
    async def popup_date(self, message):
        await self.tmux_popup( "toilet -t -f future $(date)" )
