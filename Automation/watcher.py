import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ai_helper import generate_post_from_image
from linkedin_helper import post_text_with_image
import os

WATCH_DIR = "./posts"

class WatcherHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        print(f"📸 New image detected: {event.src_path}")

        try:
            post_text = generate_post_from_image(event.src_path)
            print("✅ Generated Post Text:")
            print(post_text)

            response = post_text_with_image(post_text, event.src_path)
            print("🚀 Successfully posted to LinkedIn:", response)

        except Exception as e:
            print("❌ Error while processing image:", e)

if __name__ == "__main__":
    observer = Observer()
    event_handler = WatcherHandler()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()
    print("👀 Watching directory:", WATCH_DIR)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
