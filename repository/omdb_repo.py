from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from time import time
from typing import Any, Dict

import requests

from repository.omdb_cache import OmdbCache


class OmdbRepo(ABC):
    BASE_URL = 'http://www.omdbapi.com/'

    def __init__(self, api_key: str) -> None:
        super().__init__()
        self.api_key = api_key

        assert len(api_key) > 0

    @abstractmethod
    def get_title_for_imdb_id(self, imdb_id: str) -> Dict[str, Any]:
        pass


class DefaultOmdbRepo(OmdbRepo):
    def get_title_for_imdb_id(self, imdb_id: str) -> Dict[str, Any]:
        params = {
            'i': imdb_id,
            'apikey': self.api_key
        }

        response = requests.get(self.BASE_URL, params)

        if response.status_code == 200:
            res = response.json()
        else:
            res = {
                'error': response.content
            }

        return res


class CachedOmdbRepo(OmdbRepo):

    def __init__(self, api_key: str, repo: DefaultOmdbRepo, cache: OmdbCache,
                 valid_for: timedelta = timedelta(days=1)) -> None:
        super().__init__(api_key)
        self._repo = repo
        self._cache = cache
        self._valid_for = valid_for

    def item_is_valid(self, item: Dict[str, Any]) -> bool:
        is_valid = datetime.now() - datetime.fromtimestamp(item.get('_timestamp')) < self._valid_for

        return is_valid

    def get_title_for_imdb_id(self, imdb_id: str) -> Dict[str, Any]:
        cached_item = self._cache.get(imdb_id)

        if cached_item is None or not self.item_is_valid(cached_item):
            hot_item = self._repo.get_title_for_imdb_id(imdb_id)

            if hot_item and hot_item.get('error') is None:
                hot_item['_timestamp'] = time()
                self._cache.put(hot_item)

            movie = hot_item
        else:
            movie = cached_item

        return movie
