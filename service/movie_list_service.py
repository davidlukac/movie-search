import datetime
import time
from typing import Any, Dict, List

import click

from repository import AdvancedRepo


class MovieListService:
    def __init__(self, advanced_repo: AdvancedRepo) -> None:
        super().__init__()
        self.advanced_repo = advanced_repo

    def list(self, rating: int, year_since: int, genre: List[str], genre_not: List[str], sort_by: str,
             genre_operator: str, results_limit: int) -> List[Dict]:
        dt = datetime.datetime(year_since, 1, 1)
        assert dt
        assert dt.year >= 1900
        assert dt.year <= datetime.datetime.fromtimestamp(time.time()).year

        assert results_limit > 0

        assert rating in range(0, 10)

        assert not any(g in genre for g in genre_not), "Genre can't be both included and excluded!"

        if year_since:
            year_string = str(year_since)
        else:
            year_string = 'ever'

        print((f"Searching for up to {results_limit} movies since {year_string} with rating {rating:.1f} to 10.0, "
               f"in{' ' if genre else ' any '}genre{'s' if len(genre) > 1 else ''}"
               f"{' ' if genre else ''}{''.join([' ', genre_operator.lower(), ' ']).join(genre)}, "
               f"{'and not in genre' if genre_not else ''}"
               f"{'s' if len(genre_not) > 1 else ''}{' ' if genre_not else ''}"
               f"{' and '.join(genre_not)}{', ' if genre_not else ''}"
               f"sorted by {sort_by}."))

        movie_lst = self.advanced_repo.list_movies(rating, year_since, genre, genre_not, sort_by, genre_operator,
                                                   results_limit)

        print(f"Found {len(movie_lst)} movies.")

        return movie_lst

    def get_list_for_ids(self, movie_ids: List[int]) -> List[Dict[str, Any]]:
        movies = []
        count = len(movie_ids)

        for i, mid in enumerate(movie_ids):
            click.echo(f"\r{i + 1}/{count} ({(i + 1) / count * 100:.2f}%)", nl=False)
            movies.append(self.advanced_repo.yts_repo.get_movie_details(mid))

        click.echo('')

        return movies
