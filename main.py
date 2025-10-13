
import config
import discord
from discord.ext import commands
import fxtwitter
import minecraft_bot

def main():

    intents = discord.Intents.default()
    intents.message_content = True  # メッセージコンテンツを受け取るためのintent

    client = discord.ext.commands.Bot(command_prefix="/", intents=intents)
    ## minecraft
    minecraft_bot.minecraft_bot(client)
    ## Twitter(old name: X)
    fxtwitter.auto_fxtwitter(client)

    client.run(config.TOKEN)

if __name__ == "__main__":
    main()
