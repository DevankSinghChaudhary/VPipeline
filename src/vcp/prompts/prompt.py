import json
from pathlib import Path

def getprompt(name) -> str:
    current_dir = Path(__file__).parent
    config_path = current_dir / "system_prompt.json"

    config_path = config_path.resolve()

    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)
        return config['node'][name]['system_prompt']
