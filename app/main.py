import re
import time
import threading
from pathlib import Path
from datetime import datetime

from config import test_file_path, ts_regex, DEBOUNCE_TIME, TS_FORMAT
from app.timestamp import Timestamp

def file_pipeline(file_path: Path, fmt=TS_FORMAT):
    content = file_path.read_text()
    timestamp = Timestamp(datetime.now().time(), fmt)
    
    if r"\ts" in content:
        new_content = re.sub(ts_regex, str(timestamp), content)
        file_path.write_text(new_content)
        return True
    return False

if __name__ == "__main__":
    print(file_pipeline(test_file_path))

