import os
import watchdog.events
import watchdog.observers
import config
import discord
import asyncio
import re
import watchdog

intents = discord.Intents.default()
intents.message_content = True  # メッセージコンテンツを受け取るためのintent

client = discord.Client(intents=intents)

# ログファイル監視用のハンドラ
class LogFileHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self, bot, channel_id):
        self.bot = bot
        self.channel_id = channel_id
        self.file_position = 0  # ファイルの位置を追跡

    def on_modified(self, event):
        if event.src_path == config.LOG_FILE_PATH:
            asyncio.run_coroutine_threadsafe(self.process_log(), client.loop)

    def on_moved(self, event):
        if isinstance(event, watchdog.events.FileMovedEvent) and event.src_path == config.LOG_FILE_PATH:
            print("[INFO]logfile moved")
            self.file_position = 0

    def on_created(self, event):
        if isinstance(event, watchdog.events.FileCreatedEvent) and event.src_path == config.LOG_FILE_PATH:
            print("[INFO]logfile created")
            self.file_position = 0

    async def process_log(self):
        with open(config.LOG_FILE_PATH, 'r', encoding='utf-8') as log_file:
            log_file.seek(self.file_position)  # 前回の読み取り位置にシーク
            lines = log_file.readlines()
            self.file_position = log_file.tell()  # 新しい読み取り位置を保存
            for line in lines[-1:]:  # 前回からの差分をチェック
                print("[INFO]read line: ", line)
                await self.check_log_line(line)

    async def check_log_line(self, line):
        join_pattern = re.compile(r'\[.*\]: (.*) joined the game')
        leave_pattern = re.compile(r'\[.*\]: (.*) left the game')
        # death_pattern = re.compile(r'\[.*\]: (.*) (was .*|died)')

        join_match = join_pattern.match(line)
        leave_match = leave_pattern.match(line)
        # death_match = death_pattern.match(line)

        if join_match:
            player = join_match.group(1)
            await self.send_message(f'{player} joined the game')
        elif leave_match:
            player = leave_match.group(1)
            await self.send_message(f'{player} left the game')
        # elif death_match:
        #     player = death_match.group(1)
        #     cause = death_match.group(2)
        #     await self.send_message(f'{player} {cause}')

    async def send_message(self, message):
        for channel in self.channel_id:
            channel = client.get_channel(channel)
            if channel:
                print("[INFO]sended to ", channel, message)
                await channel.send(message)

# ログを監視して、入退室を通知
# async def enter_exit_log():
#     channel = client.get_channel(config.ENTER_EXIT_LOG_CHANNEL_ID)
#     await channel.send()

@client.event
async def on_ready():
    print("start stone's discord bot")
    print(f'Logged in as {client.user.name}')

    # ログ監視
    watcher = LogFileHandler(client, config.ENTER_EXIT_LOG_CHANNEL_ID)
    observer = watchdog.observers.Observer()
    observer.schedule(watcher, path=os.path.dirname(config.LOG_FILE_PATH), recursive=False)
    observer.start()

client.run(config.TOKEN)
