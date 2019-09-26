class ImdbService:
    @staticmethod
    def get_url_for_code(code: str) -> str:
        return f"https://imdb.com/title/{code}"
