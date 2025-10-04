import config
import os
import watchdog.observers
import watchdog
import models

def minecraft_bot(client):
    # ログを監視して、入退室を通知
    # async def enter_exit_log():
    #     channel = client.get_channel(config.ENTER_EXIT_LOG_CHANNEL_ID)
    #     await channel.send()

    @client.event
    async def on_ready():
        print("start stone's discord bot")
        print(f'Logged in as {client.user.name}')

        # ログ監視
        watcher = models.LogFileHandler(client, config.ENTER_EXIT_LOG_CHANNEL_ID)
        observer = watchdog.observers.Observer()
        observer.schedule(watcher, path=os.path.dirname(config.LOG_FILE_PATH), recursive=False)
        observer.start()
