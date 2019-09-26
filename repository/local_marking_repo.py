from pathlib import Path
from typing import List

from tinydb import Query, TinyDB


class LocalStoragePathFactory:
    DEFAULT_STORAGE_FOLDER_LOCATION = Path.home()
    DEFAULT_FOLDER_NAME = Path('.yts')
    DEFAULT_SEEN_FILE = Path('seen.json')

    @classmethod
    def get_seen_storage(cls, folder_location: Path = DEFAULT_STORAGE_FOLDER_LOCATION,
                         folder_name: Path = DEFAULT_FOLDER_NAME, file_name: Path = DEFAULT_SEEN_FILE) -> Path:
        target_dir = Path.joinpath(folder_location, folder_name)
        if not target_dir.exists():
            print(f"Setting up data folder {target_dir}")
            target_dir.mkdir(exist_ok=True)
        assert target_dir.exists()
        assert target_dir.is_dir()

        storage = Path.joinpath(target_dir, file_name)
        storage.touch(exist_ok=True)
        assert storage.exists()
        assert storage.is_file()

        return storage


class LocalMarkingRepo:
    SEEN_TABLE = 'seen'

    def __init__(self, storage: Path) -> None:
        super().__init__()
        self.storage = storage
        storage.touch(exist_ok=True)
        assert self.storage.exists()
        assert self.storage.is_file()
        assert self.storage.suffix == '.json'

        self.db = TinyDB(self.storage, default_table=self.SEEN_TABLE, sort_keys=True, indent=2, separators=(',', ': '))
        self.seen_t = self.db.table(self.SEEN_TABLE)

    def __del__(self):
        print('Closing DB...')
        self.db.close()

    def mark_seen(self, mid: int) -> List[int]:
        doc = {
            'id': mid,
            'seen': True
        }

        db_ids = self.seen_t.upsert(doc, Query().id == mid)

        return db_ids

    def un_mark_seen(self, mid: int) -> List[int]:
        q = Query()

        db_ids = self.seen_t.remove(q.id == mid)

        return db_ids

    def was_seen(self, mid: int) -> bool:
        q = Query()

        contains = self.seen_t.contains((q.id == mid) & q.seen.test(bool))

        return contains

    def get_seen_movie_ids(self) -> List[int]:
        q = Query()

        movie_ids = [m.get('id') for m in self.seen_t.search(q.seen.test(bool))]

        return movie_ids
