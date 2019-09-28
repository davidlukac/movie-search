from typing import Any, Dict, List

from service import ImdbService


class MovieListView:
    @staticmethod
    def get_names_as_list(movie_list: List[Dict[str, Any]]):
        return [
            (f"{m.get('id')}: {m.get('title_english')} ({m.get('year')}), "
             f"rated {m.get('rating'):.1f} by {m.get('imdb_votes'):,} @ IMDB "
             f"({ImdbService.get_url_for_code(m.get('imdb_code'))}), "
             f"genre: {', '.join(m.get('genres'))}")
            for m in movie_list
        ]
