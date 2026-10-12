import yaml

from vcp.utils import root

path = root()


class ConfigLoader:
    def __init__(self, _path):
        self._path = path.find(_path)

    def load(self):
        with self._path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}
            return data


config = ConfigLoader("profile/technical.yaml")
data = config.load()
print(data)
