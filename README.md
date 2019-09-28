**DISCLAIMER: This project is intended for academical purpose, to learn working with APIs and other technologies.**
**It under no circumstances encourages illegal distribution of any copyrighted materials.**


# Installation

`pipenv install`


# Usage

`pipenv run python yts.py --help`


## Examples

```
pipenv run python yts.py movie-list -r 6 -y 2000 -l 10
pipenv run python yts.py movie-list -r 6 -y 2017 -g horror --genre-not=animation --genre-not=biography -g mystery -o AND
pipenv run python yts.py movie-list -r 6 -y 2015 -l 20 --least-votes 250000
pipenv run python yts.py mark-seen 3175 3489 1606 3488 3490
pipenv run python yts.py seen-list
pipenv run python yts.py omdb get tt8291224
```


# Features

- List and filter movies from [YTS.lt](http://yts.lt)
- Filter by minimal rating _(as per YTS API)_
- Filter by published year (and newer) _(extra - no in API)_
- Filter by genre 
- Apply multiple genre filter with OR/AND conditions _(extra - no in API)_
- Exclude movies with genre, also multiple _(extra - no in API)_
- Limit number of results
- Filter movies by minimal number of rating votes at OMDB 
- Mark (and un-mark) movies as seen so they are excluded from the search results
- List seen movies
- Get movie details from OMDB database
- Caching of OMDB data for faster operation
