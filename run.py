from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
import sys
import os

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_app()
    
    def start_app(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        
        print("\n🚀 アプリを起動するナリ！")
        self.process = subprocess.Popen([sys.executable, "pixelui.py"])
    
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"\n🔄 {event.src_path} が変更されたナリ！再起動するナリ！")
            self.start_app()

if __name__ == "__main__":
    path = "."
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        if event_handler.process:
            event_handler.process.terminate()
        observer.stop()
    observer.join() 