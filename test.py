import unittest

from imdb_user_ratings import IMDBUserRatings, InvalidIMDBUserID
from mock import patch


class IMDBUserRatingsTest(unittest.TestCase):
    """Test cases for the IMDBUserRating module."""

    _test_file = "test_rss.xml"

    # test class methods
    def test_parse_imdb_id_from_url(self):
        example_url = "http://www.imdb.com/title/tt1234567/"
        exp_imdb_id = "tt1234567"
        act_imdb_id = IMDBUserRatings._parse_imdb_id(example_url)
        self.assertEqual(exp_imdb_id, act_imdb_id)

    def test_parse_date(self):
        example_date = "Wed, 13 Jan 2016 00:00:00 GMT"
        exp_date_str = "2016-01-13"
        act_date_str = IMDBUserRatings._parse_date(example_date)
        self.assertEqual(exp_date_str, act_date_str)

    def test_parse_title_without_media_type(self):
        example_title = "Star Wars: Episode VII - The Force Awakens (2015)"
        exp_title = "Star Wars: Episode VII - The Force Awakens"
        exp_year_released = 2015
        exp_media_type = "movie"
        act_title, act_year_released, act_media_type = IMDBUserRatings._parse_title_year_media_type(example_title)
        self.assertEqual(exp_title, act_title)
        self.assertEqual(exp_year_released, act_year_released)
        self.assertEqual(exp_media_type, act_media_type)

    def test_parse_title_with_media_type(self):
        example_title = "The Sopranos (1999 TV Series)"
        exp_title = "The Sopranos"
        exp_year_released = 1999
        exp_media_type = "tv-series"
        act_title, act_year_released, act_media_type = IMDBUserRatings._parse_title_year_media_type(example_title)
        self.assertEqual(exp_title, act_title)
        self.assertEqual(exp_year_released, act_year_released)
        self.assertEqual(exp_media_type, act_media_type)

    def test_parse_user_rating(self):
        example_description = """
            user rated this 8.
        """
        exp_rating = 8
        act_rating = IMDBUserRatings._parse_user_rating(example_description)
        self.assertEqual(exp_rating, act_rating)

    @patch('imdb_user_ratings.request.urlopen')
    def test_get_user_ratings(self, mock_urlopen):
        # run get_user_ratings() with urlopen() mocked
        with open(self._test_file, mode='rb') as mock_user_rss:
            mock_urlopen.return_value = mock_user_rss
            user_ratings = IMDBUserRatings("ur1234567").get_user_ratings()

        exp_items = [{
            'title': "Ex Machina",
            'year_released': 2015,
            'media_type': "movie",
            'imdb_id': "tt0470752",
            'rating': 7,
            'date_rated': "2016-02-07"
        }, {
            'title': "The Walking Dead",
            'year_released': 2010,
            'media_type': "tv-series",
            'imdb_id': "tt1520211",
            'rating': 8,
            'date_rated': "2016-01-16"
        }, {
            'title': "Hardhome",
            'year_released': 2015,
            'media_type': "tv-episode",
            'imdb_id': "tt3866850",
            'rating': 10,
            'date_rated': "2015-05-31"
        }, {
            'title': "Making a Murderer",
            'year_released': 2015,
            'media_type': "mini-series",
            'imdb_id': "tt5189670",
            'rating': 8,
            'date_rated': "2016-01-16"
        }]

        self.assertEqual(len(user_ratings), 4)
        for idx, exp_item in enumerate(exp_items):
            self.assertEqual(exp_item, user_ratings[idx].__dict__)

    # test exception
    def test_empty_user_id(self):
        with self.assertRaises(InvalidIMDBUserID):
            user_ratings = IMDBUserRatings("")


if __name__ == '__main__':
    unittest.main(verbosity=2)
