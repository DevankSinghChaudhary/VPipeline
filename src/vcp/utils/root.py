from pathlib import Path


class root:
    def find(self, path: str | None = None):
        current = Path(__file__).resolve()
        for dir in current.parents:
            if (dir / "pyproject.toml").exists():
                if path and path[0] == "/":
                    # if path[0] == "/":
                    path = path.replace("/", "", 1)
                    return dir / path
                elif path:
                    return dir / path
                return dir
        raise FileNotFoundError("Could not find 'pyproject.toml' in project root")
