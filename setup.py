#!/usr/bin/env python

from setuptools import setup

setup(
    name='imdb_user_ratings',
    packages=['imdb_user_ratings'],
    description='Python library for fetching and parsing a user\'s submitted ratings from IMDb.com',
    long_description='''Python library for fetching and parsing a user\'s submitted ratings from IMDb.com.
    For more description, visit http://www.github.com/rgj7/imdb_user_ratings''',
    version='1.0.0',
    url='http://www.github.com/rgj7/imdb_user_ratings',
    author='Raul Gonzalez',
    author_email='raul@whoisrgj.com',
    license='GNU General Public License v2.0',
    keywords=['imdb', 'movies', 'tv', 'ratings'],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: XML",
    ]
)
