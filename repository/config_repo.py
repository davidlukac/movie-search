import json
from pathlib import Path


class Config:
    omdb_api_key = None


class ConfigRepo:
    def __init__(self, config: Path) -> None:
        super().__init__()
        self.config = config
        assert config.exists()
        assert config.is_file()

    def get_config(self) -> Config:
        with self.config.open('r') as f:
            j = json.load(f)
            c = Config()
            c.omdb_api_key = j.get('omdb_api_key')

            return c
