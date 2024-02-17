import nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View
from nextcord import SyncWebhook
from utils.mongo_utils import add_user, get_user, update_apikey


class Register_Modal(nextcord.ui.Modal):
    def __init__(self, interaction):
        super().__init__(
            title="Register",
            custom_id="persistent_modal:register",
            timeout=None,
        )

        self.prn = nextcord.ui.TextInput(
            label="Please Input your prn number",
            placeholder="2023080......",
            required=True,
            style=nextcord.TextInputStyle.short,
            custom_id="persistent_modal:prn",
        )
        self.add_item(self.prn)

        self.email = nextcord.ui.TextInput(
            label="Input Mail Adress",
            placeholder="If you need mail about attendance then input your mail adress",
            required=False,
            style=nextcord.TextInputStyle.short,
            custom_id="persistent_modal:email",
        )
        self.add_item(self.email)

        self.api_key = nextcord.ui.TextInput(
            label="INPUT YOUR OPEN AI GPT API KEY",
            placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxx",
            style=nextcord.TextInputStyle.short,
            custom_id="persistent_modal:api_key",
        )
        self.add_item(self.api_key)

    async def callback(self, interaction: nextcord.Interaction):
        try:
            user_add = await add_user(
                interaction.user.id,
                self.api_key.value,
                self.prn.value,
                self.email.value,
            )
            if user_add == False:
                await interaction.user.send(
                    "> Error while storing data in database",
                )
            else:
                await interaction.user.send(
                    "> Successfully registered you 🍪",
                )
        except:
            await interaction.user.send(f"> Error while storing data in database")


class update_apikey_modal(nextcord.ui.Modal):
    def __init__(self, ctx):
        super().__init__(
            title="Update API Key",
            custom_id="persistent_modal:update_apikey",
            timeout=None,
        )

        self.api_key = nextcord.ui.TextInput(
            label="INPUT YOUR OPEN AI GPT API KEY",
            placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxx",
            style=nextcord.TextInputStyle.short,
            custom_id="persistent_modal:api_key",
        )
        self.add_item(self.api_key)

    async def callback(self, interaction: nextcord.Interaction):
        try:
            update = await update_apikey(interaction.user.id, self.api_key.value)
            if update == False:
                await interaction.send("> Error while updating data in database")
            else:
                await interaction.send("> Successfully updated your api key 🍪")
        except:
            await interaction.send("> Error while updating data in database")
