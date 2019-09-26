from typing import Tuple

import click
from click import Choice

from repository import AdvancedRepo, GenreRepository, YtsRepo
from service import MovieListService
from view import MovieListView


@click.group()
def yts():
    pass


@yts.command()
@click.option('-r', '--rating', type=int)
@click.option('-y', '--year-since', type=int)
@click.option('-g', '--genre', type=Choice(GenreRepository.ALL_GENRES), default=None, multiple=True)
@click.option('--sort-by', type=Choice(YtsRepo.SORT_OPTIONS), default=YtsRepo.RATING_SORT, show_default=True)
@click.option('--genre-operator', type=Choice(AdvancedRepo.GENRE_OPERATORS), default=AdvancedRepo.OR_GENRE_OPERATOR,
              show_default=True)
@click.option('-l', '--results-limit', type=int, default=100, show_default=True)
def movie_list(rating: int, year_since: int, genre: Tuple[str], sort_by: str, genre_operator: str, results_limit: int):
    yts_repo = YtsRepo()
    adv_repo = AdvancedRepo(yts_repo)
    svc = MovieListService(adv_repo)

    movie_lst = svc.list(rating, year_since, list(genre), sort_by, genre_operator, results_limit)

    click.echo('\n'.join(MovieListView.get_names_as_list(movie_lst)))


@yts.command()
def genre_list():
    print('\n'.join('{}'.format(g) for g in GenreRepository().ALL_GENRES))
