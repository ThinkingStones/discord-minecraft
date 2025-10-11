import datetime
import re
import config

TWITTER_URL = re.compile(r"https?://(?:x|twitter)\.com/([^/\s])+/status/(\d+)", flags=re.IGNORECASE)

def auto_fxtwitter(client, channel_id):
    # 対象チャネルじゃない場合return
    if not channel_id in config.CONV_FXTWITTER_TARGET_CHANNEL:
        return

    @client.event
    async def on_message(message):
        # twitterのURLを抽出
        content_urls = TWITTER_URL.findall(message.content)

        # x.comを含まない場合return
        if len(content_urls) > 0:
            return
        # 埋め込みがある場合return
        if message.embeds:
            return
        conv_urls = []
        for url in content_urls:
            conv_url = re.sub(r"(?:x|twitter)\.com", "fxtwitter.com", url, flags=re.IGNORECASE)
            conv_urls.append(conv_url)

        try:
            await message.reply("\n".join(), mention_author=False)
        except Exception as e:
            print(datetime.datetime.now(), "[INFO] failed to reply fxtwitter")
