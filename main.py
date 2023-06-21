import discord

from replit import db
import os  # default module
from dotenv import load_dotenv
import keep_alive
 
# imports from other files
import encryption
from word_search import solve
from nasa import fetch_pic, date_changer
from space_others import update_sun_data
from weather import get_current_weather, update_today_weather
from api_limit import update_user_stats

load_dotenv()  # load all the variables from the env file
token = str(os.getenv("TOKEN"))
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!\n")
    print('Servers:')
    for guild in bot.guilds:
        print(f"- {guild.name}")


@bot.slash_command(name="hello", description="Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")


@bot.slash_command(name="api_uses", description="for testing purposes.")
async def api_uses(ctx):
    if ctx.author.id != 707282864139665532:
        await ctx.respond("This command is not for you", ephemeral=True)
    else:
        res = ""
        for k in db.keys():
            res += f"{k}: {db[k]}\n"
        await ctx.respond(res)


# encryption
@bot.slash_command(name="encrypt",
                   description="Encrypt text using transposition cipher")
async def encrypt(ctx, key: discord.Option(int), message: discord.Option(str)):
    if ctx.author.nick is None:
        await ctx.channel.send(
            f"*{ctx.author.name}#{ctx.author.discriminator}*: {await encryption.encrypt(message, key)}"
        )

    else:
        await ctx.channel.send(
            f"*{ctx.author.nick}* ({ctx.author.name}#{ctx.author.discriminator}): {await encryption.encrypt(message, key)}"
        )

    await ctx.respond(f"The key to decrypt the message is **{key}**",
                      ephemeral=True)


@bot.slash_command(
    name="decrypt",
    description="Decrypt text that was encrypted by this bot (need key)")
async def decrypt(ctx, key: discord.Option(int), message: discord.Option(str)):
    await ctx.respond(await encryption.decrypt(message, key))


@bot.slash_command(name="wordsearch", description="Solve a word search puzzle")
async def find_words(ctx, puzzle: discord.Option(str),
                     words: discord.Option(str)):
    res = await solve(words, puzzle)
    await ctx.respond(res)


@bot.slash_command(name="say", description="Make the bot talk")
async def say(ctx,
              text: discord.Option(str,
                                   "The message you want the bot to send"),
              channel: discord.Option(
                  str,
                  "(Channel name) Send message in a specific channel",
                  required=False)):
    try:
        if channel:
            channel = discord.utils.get(ctx.guild.channels, name=channel)
            await channel.send(text)
        else:
            await ctx.channel.send(text)
        await ctx.respond("message sent", ephemeral=True)

    except:
        await ctx.respond(
            "Could not send message. Possible causes include: Missing permissions to access channel, message is too long, and invalid channel name.",
            ephemeral=True)


@bot.slash_command(name="react", description="React to a message")
async def react(ctx, message: discord.Option(str,
                                             "ID of the MESSAGE to react to"),
                reaction: discord.Option(str,
                                         "Name of the reaction (omit colons)"),
                channel: discord.Option(str,
                                        "ID of the CHANNEL to react to",
                                        required=False)):
    try:
        reaction = reaction.strip(":")
        if not channel:
            channel = bot.get_channel(ctx.channel.id)
        else:
            channel = bot.get_channel(channel)

        message = await channel.fetch_message(message)
        reaction = discord.utils.get(bot.emojis, name=reaction)
        await message.add_reaction(reaction)
        await ctx.respond("Successfully reacted to message", ephemeral=True)

    except:
        await ctx.respond(
            "Invalid channel ID, message ID, or reaction name. Also make sure that the bot has permission to react external emojis (from other servers)",
            ephemeral=True)


@bot.slash_command(
    name="planetary-k",
    description=
    "(Planetary K-index) Recent information on solar activity and geomagnetic storms"
)
async def planetary_K(ctx):
    await ctx.respond("Fetching data...")
    try:
        update_sun_data()
        await ctx.respond(file=discord.File('sun_data.png'))
    except Exception as e:
        print(f"An error occured in the planetary-k command: {e}")
        await ctx.respond("Failed to fetch data.")


@bot.slash_command(name="weather",
                   description="Current weather data for any location")
async def current_weather(ctx, location: discord.Option(
    str, "Input a city name with its province or country name")):
    user = str(ctx.author.id)
    if update_user_stats(user) == "limit exceeded":
        await ctx.respond(
            "You have used weather commands too often today. Do not spam commands and try again tomorrow.",
            ephemeral=True)
        return

    try:
        weather_data = get_current_weather(location)
        await ctx.respond(weather_data)
    except:
        await ctx.respond(
            "An error has occured when fetching weather data. If you entered a valid city name, try being more specific by also entering the province/country that the city is in.",
            ephemeral=True)


@bot.slash_command(
    name="weather_today",
    description="Get today's temperature and precipitation data.")
async def weather_today(ctx, location: discord.Option(
    str, "Input a city name with its province or country name")):

    await ctx.respond("Fetching weather data...")
    user = str(ctx.author.id)
    if update_user_stats(user) == "limit exceeded":
        await ctx.respond(
            "You have used weather commands too often today. Do not spam commands and try again tomorrow.",
            ephemeral=True)
        return

    try:
        today_weather = update_today_weather(location)
        await ctx.respond(today_weather,
                          file=discord.File('today_temperature.png'))

    except Exception as e:
        print(f"An error occured in the weather_today command: {e}")
        await ctx.respond(
            "An error has occured when fetching weather data. If you entered a valid city name, try being more specific by also entering the province/country that the city is in.",
            ephemeral=True)


@bot.slash_command(
    name="apod",
    description="Fetch the Astronomy Picture of the Day with its description")
async def get_apod(ctx, date: discord.Option(
    str,
    "Find the APOD from a specific date in YYYY-MM-DD format",
    required=False,
    default='')):

    try:
        data, date = await fetch_pic(date)
        Apod_view = Buttons(ctx.author.id, date)
        await ctx.respond(data, view=Apod_view)
    except:
        await ctx.respond(
            "Unable to fetch APOD. Please check if the date is valid (YYYY-MM-DD). Note: APOD may be down if you keep getting this error."
        )


# buttons for apod
class Buttons(discord.ui.View):

    def __init__(self, user_id, date):
        super().__init__()
        self.user_id = user_id
        self.date = date

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous_button(self, button: discord.ui.Button,
                              interaction: discord.Interaction):
        if interaction.user.id == self.user_id:
            self.date = date_changer(self.date, '<')
            data = await fetch_pic(self.date)
            data = data[0]  # unpack tuple
            await interaction.response.edit_message(content=data, view=self)

        else:
            await interaction.response.send_message(
                "This interaction is not for you. Use /apod to start an intereaction.",
                ephemeral=True)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, button: discord.ui.Button,
                          interaction: discord.Interaction):
        if interaction.user.id == self.user_id:
            self.date = date_changer(self.date, '>')
            data = await fetch_pic(self.date)
            data = data[0]  # unpack tuple
            await interaction.response.edit_message(content=data, view=self)

        else:
            await interaction.response.send_message(
                "This interaction is not for you. Use /apod to start an intereaction.",
                ephemeral=True)


# def main():
#     keep_alive.keep_alive()
#     try:
#         bot.run(token)
#     except:
#         print("An error has occured (test Cloudflare)")

# while True:
#     main()
#     os.system("kill 1")
#     print("Rebooting")
keep_alive.keep_alive()
bot.run(token)

i = 0
while True:
    print(i)
