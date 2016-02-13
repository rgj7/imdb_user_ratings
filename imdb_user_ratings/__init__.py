"""
imdb_user_ratings
~~~~~~~~~~~~~~~~~
Created by Raul Gonzalez
"""

from datetime import datetime
from re import match
from urllib import request
from xml.etree import ElementTree


class InvalidIMDBUserID(Exception):
    pass


class IMDBUserRatings(object):
    """
    Fetches and parses an IMDb.com user's ratings RSS feed.
    """
    _imdb_user_rss_url = "http://rss.imdb.com/user/{user_id}/ratings"

    def __init__(self):
        pass

    def get_user_ratings(self, user_id):
        """Fetches and parses the a IMDb.com user's ratings RSS feed into a list of 'UserRating' objects.

        Args:
            user_id: A string containing a IMDb.com user id, used to create user RSS url.

        Returns:
            A list of dicts containing parsed data.

        Raises:
            InvalidIMDBUserID: The username is invalid (an empty string).
            HTTPError: The server couldn't fulfill the request.
            URLError: Failed to reach the server.
            ParseError: If there is a failure parsing the `user_rss` file object.
        """
        if not user_id:
            raise InvalidIMDBUserID("user id cannot be empty.")

        url = self._imdb_user_rss_url.format(user_id=user_id)
        with request.urlopen(url) as data:
            element_tree = ElementTree.parse(data)
            items = element_tree.getroot()[0][2:]  # skip over first two
        return [self._parse_element(item) for item in items]

    @staticmethod
    def _parse_date(string):
        """Parse a date string and return a date string in "YYYY-MM-DD" format.

        Args:
            string: A string representing the date (and time) rating was submitted.
                ex. "Wed, 13 Jan 2016 00:00:00 GMT"

        Returns:
            A date string in "YYYY-MM-DD" format based on the given string.
        """
        return datetime.strptime(string, "%a, %d %b %Y %H:%M:%S %Z").date().isoformat()

    @staticmethod
    def _parse_imdb_id(string):
        """Parse a URL string and return an IMDb title id.

        Args:
            string: A string containing a IMDb title URL. ex. "http://www.imdb.com/title/tt1234567/"

        Returns:
            A string containing an IMDb title id. ex. "tt1234567"
        """
        return match('.*/([t0-9]+)/$', string).group(1)

    @staticmethod
    def _parse_user_rating(string):
        """Parse a string and return a user rating as an integer.

        Args:
            string: A string containing a user rating. ex. "user rated this 10."

        Returns:
            An integer representing the user's rating. ex. 10
        """
        return int(match('.*\s([0-9]+)\.?$', string.strip()).group(1))

    @staticmethod
    def _parse_title_year_media_type(string):
        """Parse a string and return a tuple containing a title, year, and media type.

        Args:
            string: A string containing a title, year and media type.
                ex. "The Walking Dead (2010 TV Series)"

        Returns:
            A tuple containing:
                title: A string containing the title. ex. "The Walking Dead"
                year_released: An integer representing the year the title was released. ex. 2015
                media_type: A string containing the media type. ex. "tv-series"
        """
        results = match('^(.+)\s\((\d{4})\s?(.*)?\)$', string)
        title = results.group(1)
        year_released = int(results.group(2))
        media_type = results.group(3)
        # If the parsed media type string is empty, it means the title is a movie.
        if media_type == "":
            media_type = "movie"
        else:
            media_type = media_type.lower().replace(" ", "-")
        return title, year_released, media_type

    def _parse_element(self, element):
        """
        Parses an 'Element' from an 'ElementTree' containing data
        from an item of the IMDb.com user's ratings RSS feed.

        Args:
            element: An 'Element' from an 'ElementTree' containing parsed RSS data

        Returns:
            A dict containing parsed data from the given element.

            date_rated (str): date string when the user rated the title. (ex. "2005-12-25")
            title (str): media's title (ex. "The Matrix")
            year_released (int): year the title was released (ex. 1999)
            media_type (str): media type of the title (ex. "movie", "tv-series", ...)
            imdb_id (str): IMDb.com title id (ex. "tt1234567")
            rating (int): user's rating of the title (ex. 1-10)
        """
        title, year_released, media_type = self._parse_title_year_media_type(element[1].text)
        return dict(
            date_rated=self._parse_date(element[0].text),
            title=title,
            year_released=year_released,
            media_type=media_type,
            imdb_id=self._parse_imdb_id(element[2].text),
            rating=self._parse_user_rating(element[4].text)
        )

