import json
from datetime import timedelta
from typing import Tuple

import click
from click import Choice

from repository import AdvancedRepo, GenreRepository, LocalMarkingRepo, LocalStoragePathFactory, YtsRepo
from repository import CachedOmdbRepo, ConfigRepo, DefaultOmdbRepo, OmdbCache
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
@click.option('--least-votes', type=int)
@click.option('-s', '--sort-by', type=Choice(YtsRepo.SORT_OPTIONS), default=YtsRepo.RATING_SORT, show_default=True)
@click.option('-o', '--genre-operator', type=Choice(AdvancedRepo.GENRE_OPERATORS),
              default=AdvancedRepo.OR_GENRE_OPERATOR, show_default=True)
@click.option('-l', '--results-limit', type=int, default=100, show_default=True)
def movie_list(rating: int, year_since: int, genre: Tuple[str], genre_not: Tuple[str], least_votes: int, sort_by: str,
               genre_operator: str, results_limit: int):
    seen_store = LocalStoragePathFactory.get_seen_storage()
    config_store = LocalStoragePathFactory.get_config_storage()
    cache_store = LocalStoragePathFactory.get_cache_storage()

    config = ConfigRepo(config_store).get_config()

    yts_repo = YtsRepo()
    local_marking_repo = LocalMarkingRepo(seen_store)
    d_omdb_repo = DefaultOmdbRepo(config.omdb_api_key)
    omdb_cache = OmdbCache(cache_store)
    omdb_repo = CachedOmdbRepo(config.omdb_api_key, d_omdb_repo, omdb_cache)
    adv_repo = AdvancedRepo(yts_repo, local_marking_repo, omdb_repo)
    svc = MovieListService(adv_repo)

    movie_lst = svc.list(rating, year_since, list(genre), list(genre_not), least_votes, sort_by, genre_operator,
                         results_limit)

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
    seen_store = LocalStoragePathFactory.get_seen_storage()
    config_store = LocalStoragePathFactory.get_config_storage()
    cache_store = LocalStoragePathFactory.get_cache_storage()

    config = ConfigRepo(config_store).get_config()

    yts_repo = YtsRepo()
    local_marking_repo = LocalMarkingRepo(seen_store)
    d_omdb_repo = DefaultOmdbRepo(config.omdb_api_key)
    omdb_cache = OmdbCache(cache_store)
    omdb_repo = CachedOmdbRepo(config.omdb_api_key, d_omdb_repo, omdb_cache)
    advanced_repo = AdvancedRepo(yts_repo, local_marking_repo, omdb_repo)
    svc = MovieListService(advanced_repo)

    movie_ids = local_marking_repo.get_seen_movie_ids()
    click.echo(f"Found {len(movie_ids)} seen movies. Fetching details...")

    movie_lst = svc.get_list_for_ids(movie_ids)
    click.echo('\n'.join(MovieListView.get_names_as_list(movie_lst)))


@yts.group()
def omdb():
    pass


@omdb.command(name='get')
@click.argument('imdb_id', type=str)
def omdb_get_by_id(imdb_id: str):
    click.echo(f"Fetching data from OMDB for {imdb_id}...")

    config_store = LocalStoragePathFactory.get_config_storage()
    cache_store = LocalStoragePathFactory.get_cache_storage()

    config = ConfigRepo(config_store).get_config()

    omdb_repo = DefaultOmdbRepo(config.omdb_api_key)
    omdb_cache = OmdbCache(cache_store)
    repo = CachedOmdbRepo(config.omdb_api_key, omdb_repo, omdb_cache, timedelta(days=1))

    data = repo.get_title_for_imdb_id(imdb_id)

    click.echo(json.dumps(data, indent=2))
