import json
from pathlib import Path



class SystemPrompt:
    def load(node) -> str:
        current_dir = Path(__file__).parent
        config_path = current_dir / "system_prompt.json"

        config_path = config_path.resolve()

        with open(config_path, "r", encoding="utf-8") as file:
            config = json.load(file)
            return config['node'][node]['system_prompt']
