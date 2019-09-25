from typing import Any, Dict

import requests


class YtsRepo:
    LIST_MOVIES = 'https://yts.lt/api/v2/list_movies.json'
    MIN_LIMIT = 1
    MAX_LIMIT = 50

    TITLE_SORT = 'title'
    YEAR_SORT = 'year'
    RATING_SORT = 'rating'
    PEERS_SORT = 'peers'
    SEEDS_SORT = 'seeds'
    DOWNLOAD_COUNT_SORT = 'download_count'
    LIKE_COUNT_SORT = 'like_count'
    DATE_ADDED_SORT = 'date_added'

    SORT_OPTIONS = [TITLE_SORT, YEAR_SORT, RATING_SORT, PEERS_SORT, SEEDS_SORT, DOWNLOAD_COUNT_SORT, LIKE_COUNT_SORT,
                    DATE_ADDED_SORT]

    def list_movies(self, min_rating: int, sort_by: str, limit: int = 50, page: int = 1) -> Dict[str, Any]:
        assert min_rating in range(0, 10)
        assert limit in range(self.MIN_LIMIT, self.MAX_LIMIT + 1)
        assert page > 0

        params = {
            'limit': limit,
            'minimum_rating': min_rating,
            'page': page,
            'sort_by': sort_by
        }

        response = requests.get(self.LIST_MOVIES, params=params)

        if response.status_code == 200:
            res = response.json()
        else:
            res = {
                'status': 'error'
            }

        return res
