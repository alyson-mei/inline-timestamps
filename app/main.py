import re
import time
import threading
from pathlib import Path
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from config import (
    FILE_PATH,
    ts_regex, 
    SELF_WRITE_GUARD,
    DEBOUNCE_TIME, 
    TS_FORMAT,  
    STATS_SEPARATOR
    )
from app.timestamp import Timestamp
from app.stats import compute_stats, format_stats
from app.commands import Commands, replacer


last_write = 0.0
debounce_timer = None

def file_pipeline(file_path: Path, fmt=TS_FORMAT):
    global last_write
    content = file_path.read_text()
    timestamp = Timestamp(datetime.now().time(), fmt)

    content = re.sub(Commands.pattern(), lambda m: replacer(m, timestamp), content)

    lines = content.splitlines(keepends=True)
    sep = STATS_SEPARATOR.strip()

    sep_index = next((i for i, l in enumerate(lines) if l.strip() == sep), None)

    if sep_index is not None:
        main_content = "".join(lines[:sep_index])
    else:
        main_content = content

    if not main_content.endswith("\n\n"):
        if main_content.endswith("\n"):
            main_content += "\n"
        else:
            main_content += "\n\n"

    stats_str = format_stats(compute_stats(main_content))
    last_write = time.time()
    file_path.write_text(main_content + stats_str)

class OnSave(FileSystemEventHandler):
    def on_modified(self, event):
        global debounce_timer

        if event.src_path != str(FILE_PATH):
            return
        if time.time() - last_write < SELF_WRITE_GUARD:
            return
        if debounce_timer:
            debounce_timer.cancel()

        debounce_timer = threading.Timer(DEBOUNCE_TIME, file_pipeline, args=[FILE_PATH, TS_FORMAT])
        debounce_timer.start()

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(OnSave(), path=str(FILE_PATH.parent), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()