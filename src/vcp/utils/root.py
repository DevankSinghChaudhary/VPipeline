from pathlib import Path

class root:
    def find():
        current = Path(__file__).resolve()
        for dir in (current.parents):
            if (dir / "pyproject.toml").exists():
                return dir
        raise FileNotFoundError("Could not find 'pyproject.toml' in project root")
