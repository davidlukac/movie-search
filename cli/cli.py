from typing import Tuple

import click
from click import Choice

from repository import AdvancedRepo, GenreRepository, LocalMarkingRepo, LocalStoragePathFactory, YtsRepo
from service import MarkingService, MovieListService
from view import MovieListView


@click.group()
def yts():
    pass


@yts.command()
@click.option('-r', '--rating', type=int)
@click.option('-y', '--year-since', type=int)
@click.option('-g', '--genre', type=Choice(GenreRepository.ALL_GENRES), default=None, multiple=True)
@click.option('--genre-not', type=Choice(GenreRepository.ALL_GENRES), default=None, multiple=True)
@click.option('-s', '--sort-by', type=Choice(YtsRepo.SORT_OPTIONS), default=YtsRepo.RATING_SORT, show_default=True)
@click.option('-o', '--genre-operator', type=Choice(AdvancedRepo.GENRE_OPERATORS),
              default=AdvancedRepo.OR_GENRE_OPERATOR, show_default=True)
@click.option('-l', '--results-limit', type=int, default=100, show_default=True)
def movie_list(rating: int, year_since: int, genre: Tuple[str], genre_not: Tuple[str], sort_by: str,
               genre_operator: str, results_limit: int):
    yts_repo = YtsRepo()
    storage = LocalStoragePathFactory.get_seen_storage()
    local_marking_repo = LocalMarkingRepo(storage)
    adv_repo = AdvancedRepo(yts_repo, local_marking_repo)
    svc = MovieListService(adv_repo)

    movie_lst = svc.list(rating, year_since, list(genre), list(genre_not), sort_by, genre_operator, results_limit)

    click.echo('\n'.join(MovieListView.get_names_as_list(movie_lst)))


@yts.command()
def genre_list():
    print('\n'.join('{}'.format(g) for g in GenreRepository().ALL_GENRES))


@yts.command()
@click.argument('ids', nargs=-1, type=int, required=True)
def mark_seen(ids: Tuple[int]):
    """IDS - List of space separated movie IDs to mark as seen."""
    storage = LocalStoragePathFactory.get_seen_storage()
    marking_svc = MarkingService(LocalMarkingRepo(storage))
    marking_svc.mark_seen(list(ids))


@yts.command()
@click.argument('ids', nargs=-1, type=int, required=True)
def un_mark_seen(ids: Tuple[int]):
    """IDS - List of space separated movie IDs to un-mark as seen."""
    storage = LocalStoragePathFactory.get_seen_storage()
    marking_svc = MarkingService(LocalMarkingRepo(storage))
    marking_svc.un_mark_seen(list(ids))


@yts.command()
def seen_list():
    storage = LocalStoragePathFactory.get_seen_storage()

    yts_repo = YtsRepo()
    local_marking_repo = LocalMarkingRepo(storage)
    advanced_repo = AdvancedRepo(yts_repo, local_marking_repo)
    svc = MovieListService(advanced_repo)

    movie_ids = local_marking_repo.get_seen_movie_ids()
    click.echo(f"Found {len(movie_ids)} seen movies. Fetching details...")

    movie_lst = svc.get_list_for_ids(movie_ids)
    click.echo('\n'.join(MovieListView.get_names_as_list(movie_lst)))
