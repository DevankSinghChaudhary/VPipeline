import os
import shutil
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

AUDIO_PATH = Path(os.getenv("AUDIO_PATH"))

def find_project_root() -> Path:
    current = Path(__file__).resolve()
    for directory in (current, *current.parents):
        if (directory / ".env").exists():
            return directory
    raise FileNotFoundError(
        "Couldn't find project root"
    )

PROJECT_ROOT = find_project_root()

AUDIO_PATH = PROJECT_ROOT / os.getenv("AUDIO_PATH")

print(
    f"Cleaning {AUDIO_PATH}"
)

def clear_audio():
    if AUDIO_PATH.exists():
        shutil.rmtree(AUDIO_PATH)

    AUDIO_PATH.mkdir(
        parents=True,
        exist_ok=True
    )
