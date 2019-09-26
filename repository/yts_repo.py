from typing import Any, Dict, List

import requests


class YtsRepo:
    YTS_BASE_URL = 'https://yts.lt/api/v2/'
    LIST_MOVIES_ENDPOINT = 'list_movies.json'
    LIST_MOVIES_URL = f"{YTS_BASE_URL}{LIST_MOVIES_ENDPOINT}"

    MOVIE_DETAILS_ENDPOINT = 'movie_details.json'
    MOVIE_DETAILS_URL = f"{YTS_BASE_URL}{MOVIE_DETAILS_ENDPOINT}"

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

    def list_movies(self, min_rating: int, genre: List[str], sort_by: str, limit: int = 50,
                    page: int = 1) -> Dict[str, Any]:

        assert min_rating in range(0, 10)
        assert limit in range(self.MIN_LIMIT, self.MAX_LIMIT + 1)
        assert page > 0

        params = {
            'limit': limit,
            'minimum_rating': min_rating,
            'page': page,
            'sort_by': sort_by,
            'genre': genre
        }

        response = requests.get(self.LIST_MOVIES_URL, params=params)

        if response.status_code == 200:
            res = response.json()
        else:
            res = {
                'status': 'error'
            }

        return res

    def get_movie_details(self, movie_id: int) -> Dict[str, Any]:
        params = {
            'movie_id': movie_id
        }

        response = requests.get(self.MOVIE_DETAILS_URL, params=params)

        if response.status_code == 200:
            res = response.json().get('data').get('movie')
        else:
            res = {
                'status': 'error'
            }

        return res
