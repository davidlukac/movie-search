from typing import List


class GenreRepository:
    ACTION_GENRE = 'action'
    ADVENTURE_GENRE = 'adventure'
    ANIMATION_GENRE = 'animation'
    BIOGRAPHY_GENRE = 'biography'
    COMEDY_GENRE = 'comedy'
    CRIME_GENRE = 'crime'
    DOCUMENTARY_GENRE = 'documentary'
    DRAMA_GENRE = 'drama'
    FAMILY_GENRE = 'family'
    FANTASY_GENRE = 'fantasy'
    FILM_NOIR_GENRE = 'film-noir'
    HISTORY_GENRE = 'history'
    HORROR_GENRE = 'horror'
    MUSIC_GENRE = 'music'
    MUSICAL_GENRE = 'musical'
    MYSTERY_GENRE = 'mystery'
    ROMANCE_GENRE = 'romance'
    SCI_FI_GENRE = 'sci-fi'
    SHORT_FILM_GENRE = 'short'
    SPORT_GENRE = 'sport'
    SUPERHERO = 'superhero'
    THRILLER_GENRE = 'thriller'
    WAR_GENRE = 'war'
    WESTERN_GENRE = 'western'

    ALL_GENRES = [ACTION_GENRE, ADVENTURE_GENRE, ANIMATION_GENRE, BIOGRAPHY_GENRE, COMEDY_GENRE, CRIME_GENRE,
                  DOCUMENTARY_GENRE, DRAMA_GENRE, FAMILY_GENRE, FANTASY_GENRE, FILM_NOIR_GENRE, HISTORY_GENRE,
                  HORROR_GENRE, MUSIC_GENRE, MUSICAL_GENRE, MYSTERY_GENRE, ROMANCE_GENRE, SCI_FI_GENRE,
                  SHORT_FILM_GENRE, SPORT_GENRE, SUPERHERO, THRILLER_GENRE, WAR_GENRE, WESTERN_GENRE]

    def get_all(self) -> List[str]:
        return self.ALL_GENRES
