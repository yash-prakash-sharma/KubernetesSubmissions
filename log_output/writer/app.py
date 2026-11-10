import os
import time
import uuid
from datetime import datetime, timezone

FILE = os.environ.get("LOG_FILE", "/shared/log.txt")
random_string = str(uuid.uuid4())


def now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


os.makedirs(os.path.dirname(FILE), exist_ok=True)

while True:
    line = f"{now()}: {random_string}"
    with open(FILE, "a") as f:
        f.write(line + "\n")
    print(line, flush=True)
    time.sleep(5)