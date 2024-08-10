import json
import discord
from discord.ext import commands

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

DISCORD_BOT_TOKEN = config["DISCORD_BOT_TOKEN"]
source_channel_id = config["source_channel_id"]
destination_thread_id = config["destination_thread_id"]

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    # if message.author == bot.user:
    #     return

    # Check if the message is from the source channel
    if message.channel.id == source_channel_id:
        # Get the destination thread
        destination_thread = bot.get_channel(destination_thread_id)

        if destination_thread is not None:
            # Copy the message to the destination thread
            await destination_thread.send(f"{message.author}: {message.content}")

@bot.event
async def on_message_edit(before, after):
    # Check if the edited message is from the source channel
    if before.channel.id == source_channel_id:
        # Get the destination thread
        destination_thread = bot.get_channel(destination_thread_id)

        if destination_thread is not None:
            # Copy the edited message to the destination thread
            await destination_thread.send(f"**Edited message from {after.author}:** {after.content}")

# Start the bot
bot.run(DISCORD_BOT_TOKEN)
