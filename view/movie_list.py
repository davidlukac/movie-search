from typing import Any, Dict, List


class MovieListView:
    @staticmethod
    def get_names_as_list(movie_list: List[Dict[str, Any]]):
        return [
            (f"{m.get('id')}: {m.get('title_english')} ({m.get('year')}), "
             f"rated {m.get('rating'):.1f} @ IMDB (https://imdb.com/title/{m.get('imdb_code')})") for m in movie_list]
