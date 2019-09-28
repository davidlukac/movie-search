from typing import Any, Dict, List

import click

from repository.local_marking_repo import LocalMarkingRepo
from repository.omdb_repo import OmdbRepo
from repository.yts_repo import YtsRepo


# noinspection PyMethodMayBeStatic
class AdvancedRepo:
    OR_GENRE_OPERATOR = 'OR'
    AND_GENRE_OPERATOR = 'AND'
    GENRE_OPERATORS = [AND_GENRE_OPERATOR, OR_GENRE_OPERATOR]

    def __init__(self, yts_repo: YtsRepo, local_marking_repo: LocalMarkingRepo, omdb_repo: OmdbRepo) -> None:
        super().__init__()
        self._yts_repo = yts_repo
        self._local_marking_repo = local_marking_repo
        self._omdb_repo = omdb_repo

    def apply_year_filter(self, movie_list: List[Dict[str, Any]], year_since: int) -> List[Dict[str, Any]]:
        return [m for m in movie_list if m.get('year') >= year_since or m.get('year') is None]

    def apply_and_genre_filter(self, movie_list: List[Dict[str, Any]], genre: List[str]) -> List[Dict[str, Any]]:
        return [m for m in movie_list if all(g in map(str.lower, m.get('genres')) for g in genre)]

    def apply_seen_filter(self, movie_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [m for m in movie_list if not self._local_marking_repo.was_seen(m.get('id'))]

    def apply_genre_not_filter(self, movie_list: List[Dict[str, Any]], genre_not: List[str]) -> List[Dict[str, Any]]:
        return [m for m in movie_list if not any(g in map(str.lower, m.get('genres')) for g in genre_not)]

    def apply_least_votes_filter(self, movie_list: List[Dict[str, Any]], least_votes: int) -> List[Dict[str, Any]]:
        return [m for m in movie_list if m.get('imdb_votes') >= least_votes]

    def list_movies(self, rating: int, year_since: int, genre: List[str], genre_not: List[str], least_votes: int,
                    sort_by: str, genre_operator: str, result_limit: int) -> List[Dict]:
        final_movies = []
        total = None
        page = 1

        while True:
            gathered_ct = len(final_movies)
            needed_ct = result_limit - gathered_ct

            click.echo(f"\rFound {gathered_ct} ({gathered_ct / result_limit * 100:.2f}%) of {result_limit} movies...",
                       nl=False)

            res = self._yts_repo.list_movies(rating, genre, sort_by, limit=YtsRepo.MAX_LIMIT, page=page)
            movies = res.get('data').get('movies')

            if movies is None and res.get('status') == 'ok':
                raise Exception('Server error - no movies were returned!')

            real_returned = len(movies)

            filtered_movies = self.apply_year_filter(movies, year_since)
            filtered_movies = self.apply_seen_filter(filtered_movies)

            if genre_not:
                filtered_movies = self.apply_genre_not_filter(filtered_movies, genre_not)

            if genre_operator == self.AND_GENRE_OPERATOR and len(genre) > 1:
                filtered_movies = self.apply_and_genre_filter(filtered_movies, genre)

            for movie in filtered_movies:
                self.enhance_movie_with_imdb_voted(movie)

            if least_votes and least_votes > 0:
                filtered_movies = self.apply_least_votes_filter(filtered_movies, least_votes)

            filtered_ct = len(filtered_movies)

            if filtered_ct < needed_ct:
                cut_idx = filtered_ct
            else:
                cut_idx = needed_ct

            movies_to_add = filtered_movies[0:cut_idx]
            final_movies = final_movies + movies_to_add

            if total is None:
                total = res.get('data').get('movie_count')

            page = page + 1

            if real_returned < YtsRepo.MAX_LIMIT:
                break
            if len(final_movies) == result_limit:
                break

        click.echo('')

        return final_movies

    def get_movie_details(self, movie_id: int) -> Dict[str, Any]:
        movie = self._yts_repo.get_movie_details(movie_id)
        movie = self.enhance_movie_with_imdb_voted(movie)

        return movie

    def enhance_movie_with_imdb_voted(self, movie: Dict[str, Any]) -> Dict[str, Any]:
        votes_str = self._omdb_repo.get_title_for_imdb_id(movie.get('imdb_code')).get('imdbVotes', '').replace(',', '')

        try:
            votes = int(votes_str)
        except ValueError:
            votes = -1

        movie['imdb_votes'] = votes

        return movie
