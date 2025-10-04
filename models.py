import re
import asyncio
import watchdog.events
import config
import datetime

# ログファイル監視用のハンドラ
class LogFileHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self, bot, channel_id, log_num):
        self.bot = bot
        self.channel_id = channel_id
        self.file_position = 0  # ファイルの位置を追跡
        self.log_num = log_num

    def on_modified(self, event):
        if event.src_path == config.LOG_FILE_PATH[self.log_num]:
            asyncio.run_coroutine_threadsafe(self.process_log(), self.bot.loop)

    def on_moved(self, event):
        if isinstance(event, watchdog.events.FileMovedEvent) and event.src_path == config.LOG_FILE_PATH[self.log_num]:
            print(datetime.datetime.now(), "[INFO] logfile moved")
            self.file_position = 0

    def on_created(self, event):
        if isinstance(event, watchdog.events.FileCreatedEvent) and event.src_path == config.LOG_FILE_PATH[self.log_num]:
            print(datetime.datetime.now(), "[INFO] logfile created")
            self.file_position = 0

    async def process_log(self):
        with open(config.LOG_FILE_PATH[self.log_num], 'r', encoding='utf-8') as log_file:
            log_file.seek(self.file_position)  # 前回の読み取り位置にシーク
            print(datetime.datetime.now(), "[INFO] file_position", self.file_position)
            lines = log_file.readlines()
            self.file_position = log_file.tell()  # 新しい読み取り位置を保存
            for line in lines[-1:]:  # 前回からの差分をチェック
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
            channel = self.bot.get_channel(channel)
            if channel:
                print(datetime.datetime.now(), "[INFO] sended to", channel, message)
                await channel.send(message)
