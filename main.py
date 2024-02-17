import os, nextcord, csv
from nextcord.ext import commands, tasks
from datetime import datetime
import motor.motor_asyncio as moto
import dotenv
from utils.mongo_utils import (
    get_collection,
    add_user,
    get_user,
    attendance_add,
    attendance_remove,
    get_all_attendance_prns,
)
from events.socrative_attendance import mark_attendance

current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")


# token and discord uri using dotenv
dotenv.load_dotenv()

token = os.getenv("DISCORD_TOKEN")
mongo_uri = os.getenv("MONGO_URI")
attendance_channel = os.getenv("ATTENDANCE_CHANNEL")
attendance_removal_channel = os.getenv("ATTENDANCE_REMOVAL_CHANNEL")
announcement_channel = int(os.getenv("ANNOUNCEMENT_CHANNEL"))


class Chotu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.my_task.start()

    def cog_unload(self):
        self.my_task.cancel()

    @tasks.loop(seconds=59)
    async def my_task(self):
        now = datetime.now()
        with open("./config/schedule.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                schedule_time = datetime.strptime(row["time"], "%H:%M")
                if (
                    row["day"].lower() == now.strftime("%A").lower()
                    and schedule_time.hour == now.hour
                    and schedule_time.minute == now.minute
                ):
                    # Your code to do something goes here
                    print(f"It's time for room {row['room']}!")
                    channel = self.bot.get_channel(announcement_channel)
                    await channel.send(f"It's time for room {row['room']}!")
                    await mark_attendance(row["room"])

    # creaing an event , when message in a channel
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.channel.id == int(attendance_channel):
            user = message.author.id
            if await get_user(user) == None:
                await message.channel.send(
                    f"Hey {message.author.mention}! You are not registered with me. Please register yourself using `/register` command."
                )
            else:
                await attendance_add(user)
                await message.author.send(
                    f"Hey {message.author.mention}! Your attendance has been marked for the day."
                )
        elif message.channel.id == int(attendance_removal_channel):
            user = message.author.id
            if await get_user(user) == None:
                await message.channel.send(
                    f"Hey {message.author.mention}! You are not registered with me. Please register yourself using `/register` command."
                )
            else:
                await attendance_remove(user)
                await message.author.send(
                    f"Hey {message.author.mention}! Your attendance has been removed for the day."
                )

    # Greetings
    @commands.Cog.listener()
    async def on_ready(self):
        await bot.change_presence(
            activity=nextcord.Activity(
                type=nextcord.ActivityType.watching, name="Kya dekh Raha he bsdk"
            )
        )
        print("\n\tLogged in as...\t")
        print(
            f"\n> NAME: {self.bot.user} \n> ID : {self.bot.user.id}\n> AT TIME : {formatted_time}"
        )

    # Reconnect
    @commands.Cog.listener()
    async def on_resumed(self):
        print("Bot has reconnected!")

    # Error Handlers
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Bot does not have permission
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Invalid Command!")

        # Bot does not have permission
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Bot Permission Missing!")


intents = nextcord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True


bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description="Chotu",
    intents=intents,
)

# connect to mongo db database and load all cogs
if __name__ == "__main__":
    # Load extension
    os.system("clear")
    # connecting to mongo db
    print("Connecting to MongoDB...")
    try:
        bot.mongo = moto.AsyncIOMotorClient(mongo_uri)
        bot.db = bot.mongo["Chotu"]
        bot.db["students"]
        print("Connected to MongoDB!")
    except Exception as e:
        print("Unable to connect to MongoDB!")
        print(e)
    for filename in os.listdir("commands"):
        if filename.endswith(".py"):
            bot.load_extension(f"commands.{filename[: -3]}")
    bot.add_cog(Chotu(bot))
    bot.run(token, reconnect=True)
