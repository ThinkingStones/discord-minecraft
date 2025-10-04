
import config
import discord
import minecraft_bot

def main():

    intents = discord.Intents.default()
    intents.message_content = True  # メッセージコンテンツを受け取るためのintent

    client = discord.Client(intents=intents)

    # minecraft
    minecraft_bot.minecraft_bot(client)

    client.run(config.TOKEN)


if __name__ == "__main__":
    main()
