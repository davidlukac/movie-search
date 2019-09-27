from pathlib import Path
from typing import Any, Dict

from tinydb import Query, TinyDB


class OmdbCache:
    MOVIE_TABLE = 'omdb_movie'

    def __init__(self, storage: Path) -> None:
        super().__init__()
        self._storage = storage

        assert self._storage.exists()
        assert self._storage.is_file()

        self._db = TinyDB(self._storage, default_table=self.MOVIE_TABLE, sort_keys=True, indent=2,
                          separators=(',', ': '))
        self._table = self._db.table(self.MOVIE_TABLE)

    def __del__(self):
        print('Closing OMDB cache DB...')
        self._db.close()

    def get(self, imdb_id: str) -> Dict[str, Any]:
        q = Query()

        res = self._table.get(q.imdbID == imdb_id)

        return res

    def put(self, data: Dict[str, Any]) -> int:
        q = Query()

        db_id = self._table.upsert(data, q.imdbID == data.get('imdbID'))

        return db_id
