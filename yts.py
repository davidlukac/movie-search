import datetime
import json
import time

import click

from repository import YtsRepo
from repository.advanced_repo import AdvancedRepo
from view import MovieListView


@click.group()
def yts():
    pass


@yts.command()
@click.option('--rating', type=int)
@click.option('--year-since', type=int)
@click.option('--sort-by', type=click.Choice(YtsRepo.SORT_OPTIONS), default=YtsRepo.RATING_SORT)
@click.option('--results-limit', type=int, default=100)
def movie_list(rating: int, year_since: int, sort_by: str, results_limit: int):
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
           f"sorted by {sort_by}."))

    yts_repo = YtsRepo()
    advanced_repo = AdvancedRepo(yts_repo)
    movie_lst = advanced_repo.list_movies(rating, year_since, sort_by, results_limit)

    print(f"Found {len(movie_lst)} movies.")
    print(json.dumps(MovieListView.get_names_as_list(movie_lst), indent=2))


if __name__ == '__main__':
    yts()
