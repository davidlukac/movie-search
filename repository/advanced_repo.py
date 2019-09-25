from typing import Any, Dict, List

from repository import YtsRepo


class AdvancedRepo:
    def __init__(self, yts_repo: YtsRepo) -> None:
        super().__init__()
        self.yts_repo = yts_repo

    def year_filter(self, movie_list: List[Dict[str, Any]], year_since: int) -> List[Dict[str, Any]]:
        return [m for m in movie_list if m.get('year') >= year_since or m.get('year') is None]

    def list_movies(self, rating: int, year_since: int, sort_by: str, result_limit: int) -> List[Dict]:
        movies = []
        total = None
        page = 1

        while True:
            needed = result_limit - len(movies)

            res = self.yts_repo.list_movies(rating, sort_by, limit=YtsRepo.MAX_LIMIT, page=page)
            i_movies = res.get('data').get('movies')

            real_returned = len(i_movies)
            filtered_movies = self.year_filter(i_movies, year_since)

            if real_returned < needed:
                cut_idx = len(filtered_movies)
            else:
                cut_idx = needed

            movies = movies + filtered_movies[0:cut_idx]

            if total is None:
                total = res.get('data').get('movie_count')

            page = page + 1

            if real_returned < YtsRepo.MAX_LIMIT:
                break
            if len(movies) == result_limit:
                break

        return movies
