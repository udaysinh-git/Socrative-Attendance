import nextcord
from nextcord.ext import commands
from nextcord.application_command import slash_command
from utils.yaml_utils import read_yaml_file, load_yaml_data
from modals.register_modal import Register_Modal
from modals.register_modal import update_apikey_modal
import dotenv, os

dotenv.load_dotenv()
guild = int(os.getenv("GUILD_ID"))
test_guilds = [guild]


class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Register Command
    @nextcord.slash_command(
        name="register", description="Registeration for the bot", guild_ids=test_guilds
    )
    async def register(self, interac: nextcord.Interaction):
        await interac.response.send_modal(
            modal=Register_Modal(interac),
        )

    # Update API KEY
    @nextcord.slash_command(
        name="update_apikey",
        description="Update your api key",
        guild_ids=test_guilds,
    )
    async def update_apikey(self, interac: nextcord.Interaction):
        await interac.response.send_modal(
            modal=update_apikey_modal(interac),
        )


def setup(bot):
    bot.add_cog(Register(bot))
    print("Register is loaded")
