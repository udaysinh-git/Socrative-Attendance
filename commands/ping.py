from nextcord.ext import commands
from datetime import datetime
from nextcord.application_command import slash_command
from utils.yaml_utils import read_yaml_file, load_yaml_data
import nextcord
from nextcord import *

test_guilds = [1130136251689873428, 882554097865218344]


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash Ping Command
    @nextcord.slash_command(
        name="ping", description="replys with bots ping", guild_ids=test_guilds
    )
    async def pingu(self, interac: Interaction):
        await interac.response.send_message(f"{self.bot.latency * 1000}ms")


def setup(bot):
    bot.add_cog(Basic(bot))
    print("Basic is loaded")
