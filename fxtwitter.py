import datetime
import re
import config
import asyncio

TWITTER_URL = re.compile(r"https://(?:x|twitter)\.com/[^/\s]+/status/\d+", flags=re.IGNORECASE)

def auto_fxtwitter(client):
    @client.event
    async def on_ready():
        print(datetime.datetime.now(), "[INFO] start auto fxtwitter")

    @client.event
    async def on_message(message):
        # 対象チャネルじゃない場合return
        if not message.channel.id in config.CONV_FXTWITTER_TARGET_CHANNEL:
            return

        # twitterのURLを抽出
        content_urls = TWITTER_URL.findall(message.content)

        # x.comを含まない場合return
        if len(content_urls) == 0:
            return
        # 埋め込みがある場合return
        await asyncio.sleep(2)  # 1秒待機
        if message.embeds:
            return

        # URL変換
        print("conv url (auto fxtwitter) target:", content_urls)
        conv_urls = []
        for url in content_urls:
            conv_url = re.sub(r"(?:x|twitter)\.com", "fxtwitter.com", url, flags=re.IGNORECASE)
            conv_urls.append(conv_url)

        # 返信
        try:
            await message.reply("\n".join(conv_urls), mention_author=False)
            print(datetime.datetime.now(), "[INFO] reply converted fxtwitter")
        except Exception as e:
            print(e)
            print(datetime.datetime.now(), "[INFO] failed to reply fxtwitter")
