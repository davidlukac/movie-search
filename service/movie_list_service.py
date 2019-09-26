import datetime
import time
from typing import Dict, List

from repository import AdvancedRepo


class MovieListService:
    def __init__(self, advanced_repo: AdvancedRepo) -> None:
        super().__init__()
        self.advanced_repo = advanced_repo

    def list(self, rating: int, year_since: int, genre: List[str], sort_by: str, genre_operator: str,
             results_limit: int) -> List[Dict]:
        dt = datetime.datetime(year_since, 1, 1)
        assert dt
        assert dt.year >= 1900
        assert dt.year <= datetime.datetime.fromtimestamp(time.time()).year

        assert results_limit > 0

        assert rating in range(0, 10)

        if year_since:
            year_string = str(year_since)
        else:
            year_string = 'ever'

        print((f"Searching for up to {results_limit} movies since {year_string} with rating {rating:.1f} to 10.0, "
               f"in{' ' if genre else ' any '}genre{'s' if len(genre) > 1 else ''}"
               f"{' ' if genre else ''}{''.join([' ', genre_operator.lower(), ' ']).join(genre)}, "
               f"sorted by {sort_by}."))

        movie_lst = self.advanced_repo.list_movies(rating, year_since, genre, sort_by, genre_operator, results_limit)

        print(f"Found {len(movie_lst)} movies.")

        return movie_lst
