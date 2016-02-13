imdb_user_ratings
=================

Python library for fetching and parsing a user's saved ratings from IMDb.com.

Quick Start
===========

Your IMDb.com user id can be seen when accessing your profile page.

![IMDb.com user id](http://i.imgur.com/UxTGfVa.png "IMDb.com user id")

```python
>>> from imdb_user_ratings import IMDBUserRatings
>>> IMDBUserRatings().get_user_ratings("ur1234567")
[{'rating': 8, 'media_type': 'movie', 'title': 'The Intern', 'imdb_id': 'tt2361509', 
'date_rated': '2016-02-07', 'year_released': 2015}, ... ]
```

Unit Tests
==========
```bash
python tests.py
```