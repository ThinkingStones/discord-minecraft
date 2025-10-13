import config
import os
import watchdog.observers
import watchdog
import models

def minecraft_bot(client):
    async def on_ready_minecraft_bot():
        print("start stone's discord bot")
        print(f'Logged in as {client.user.name}')

        # ログ監視
        watcher = [None] * len(config.LOG_FILE_PATH)
        observer = watchdog.observers.Observer()

        for log_num in range(len(config.LOG_FILE_PATH)):
            watcher[log_num] = models.LogFileHandler(client, config.ENTER_EXIT_LOG_CHANNEL_ID, log_num)
            observer.schedule(watcher[log_num], path=os.path.dirname(config.LOG_FILE_PATH[log_num]), recursive=False)
        observer.start()
    client.add_listener(on_ready_minecraft_bot, "on_ready")
