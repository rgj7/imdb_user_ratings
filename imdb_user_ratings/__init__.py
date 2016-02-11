from datetime import datetime
from re import match
from urllib import request
from xml.etree import ElementTree


class UserRating(object):
    """
    Attributes:
        title (str): media's title (ex. "The Matrix")
        year_released (int): year the title was released (ex. 1999)
        media_type (str): media type of the title (ex. "movie", "tv-series", ...)
        imdb_id (str): IMDb.com title id (ex. "tt1234567")
        rating (int): user's rating of the title (ex. 1-10)
        date_rated (str): date string when the user rated the title. (ex. "2005-12-25")
    """
    def __init__(self, title, year_released, media_type, imdb_id, rating, date_rated):
        self.title = title
        self.year_released = year_released
        self.media_type = media_type
        self.imdb_id = imdb_id
        self.rating = rating
        self.date_rated = date_rated

    def __repr__(self):
        return str(self.__dict__)


class InvalidIMDBUserID(Exception):
    pass


class IMDBUserRatings(object):
    """
    Fetches an IMDb.com user's ratings RSS feed, then parses each item into a 'UserRating' object.
    All 'UserRating' objects created are stored into a list.

    Attributes:
        user_id: A string containing a IMDb.com user id, used to retrieve RSS data from.
        user_ratings: A list of 'UserRating' objects, each containing parsed data.
    """
    _imdb_user_rss_url = "http://rss.imdb.com/user/{user_id}/ratings"

    def __init__(self, user_id):
        if user_id == "":
            raise InvalidIMDBUserID("user id cannot be empty.")
        self.user_id = user_id
        self.user_ratings = []

    def get_user_ratings(self):
        """Fetches and parses the a IMDb.com user's ratings RSS feed into a list of 'UserRating' objects.

        Returns:
            user_ratings (List[UserRating]): A list of 'UserRating' objects containing parsed data.

        Raises:
            HTTPError: The server couldn't fulfill the request.
            URLError: Failed to reach the server.
            ParseError: If there is a failure parsing the `user_rss` file object.
        """
        rss_url = self._imdb_user_rss_url.format(user_id=self.user_id)
        with request.urlopen(rss_url) as user_rss:
            items = ElementTree.parse(user_rss).getroot()[0][2:]  # skip over first two
        user_ratings = [self._parse_element(item) for item in items]
        return user_ratings

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
            element: An 'Element' from an 'ElementTree', to be parsed and turned into a
                'UserRating' object.

        Returns:
            A 'UserRating' object containing parsed data from the given element.
        """
        date_rated = self._parse_date(element[0].text)
        title, year_released, media_type = self._parse_title_year_media_type(element[1].text)
        imdb_id = self._parse_imdb_id(element[2].text)
        user_rating = self._parse_user_rating(element[4].text)
        return UserRating(title, year_released, media_type, imdb_id, user_rating, date_rated)

    def __repr__(self):
        return "<IMDBUserRatings: {} titles>".format(len(self.user_ratings))