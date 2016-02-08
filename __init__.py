from urllib import request
from enum import Enum
from xml.etree import ElementTree
from datetime import datetime

import re


class MediaType(Enum):
    OTHER = "other"
    MOVIE = "movie"
    TV_SERIES = "tv-series"
    TV_EPISODE = "tv-episode"


class UserRating:
    """
    Attributes:
        title (str): A string of the media's title.
        year_released (int): The year the title was released.
        media_type (MediaType): The type of media of the title.
        imdb_id (str): IMDb.com title id
        user_rating (int): The user's rating of the title (1-10).
        date_rated (date): The date the user rated the title.
    """
    def __init__(self, title, year_released, media_type, imdb_id, user_rating, date_rated):
        self.title = title
        self.year_released = year_released
        self.media_type = media_type
        self.imdb_id = imdb_id
        self.user_rating = user_rating
        self.date_rated = date_rated


class IMDBUserRatings:
    """
    Attributes:
        user_id (str): The IMDb.com user id used to retrieve RSS data from.
        user_ratings (List[UserRating]): A list of UserRating objects containing parse data.
    """
    _user_rss_url = "http://rss.imdb.com/user/{user_id}/ratings"

    def __init__(self, user_id):
        self.user_id = user_id
        self.user_ratings = self._parse_user_rss(self._get_user_rss())

    def get_user_ratings(self):
        return self.user_ratings

    def _get_user_rss(self):
        """Sends a request for the user's rating RSS feed.

        Returns:
            Returns a file-like object containing response from URL.

        Raises:
            HTTPError: The server couldn't fulfill the request.
            URLError: Failed to reach the server.
        """
        user_rss_url = self._user_rss_url.format(user_id=self.user_id)
        return request.urlopen(user_rss_url)

    def _parse_user_rss(self, user_rss):
        """Parses the response into a list of UserRating objects.

        Args:
            user_rss (file): File-like object containing fetched RSS data.

        Returns:
            user_ratings (List[UserRating]): A list of UserRating objects containing parsed data.

        Raises:
            ParseError: If there is a failure parsing the `user_rss` file object.
        """
        user_ratings = list()
        if user_rss:
            tree = ElementTree.parse(user_rss)
            root = tree.getroot()
            for item in root[0][2:]:  # skips the first two non-item elements
                user_rating = self._parse_element(item)
                user_ratings.append(user_rating)
        return user_ratings

    @staticmethod
    def _parse_media_type(string):
        if string == "":
            return MediaType.MOVIE
        if string == "TV Series":
            return MediaType.TV_SERIES
        if string == "TV Episode":
            return MediaType.TV_EPISODE
        return MediaType.OTHER

    @staticmethod
    def _parse_date(string):
        return datetime.strptime(string, "%a, %d %b %Y %H:%M:%S %Z").date()

    @staticmethod
    def _parse_imdb_id(string):
        return re.match('.*/([t0-9]+)/$', string).group(1)

    @staticmethod
    def _parse_user_rating(string):
        return int(re.match('.*\s([0-9]+)\.?$', string.strip()).group(1))

    def _parse_title_year_media_type(self, string):
        results = re.match('^(.+)\s\((\d{4})\s?(.*)?\)$', string)
        title = results.group(1)
        year_released = int(results.group(2))
        media_type = self._parse_media_type(results.group(3))
        return title, year_released, media_type

    def _parse_element(self, element):
        """Parses an Element from an ElementTree

            Args:
                element: An Element object containing data for an individual UserRating.
        """
        # parse the date
        # ex. Wed, 13 Jan 2016 00:00:00 GMT
        date_rated = self._parse_date(element[0].text)
        # title splits into title, year released and media type
        # ex1. Movie Title (2015)
        # ex2. Television Series (2015 TV Series)
        title, year_released, media_type = self._parse_title_year_media_type(element[1].text)
        # parse title id from link
        # ex. http://www.imdb.com/title/tt123456789/
        imdb_id = self._parse_imdb_id(element[2].text)
        # parse user rating from description
        # note: element has whitespace around it, so strip() is used
        # ex. User rated this 9.
        user_rating = self._parse_user_rating(element[4].text)
        return UserRating(title, year_released, media_type, imdb_id, user_rating, date_rated)
