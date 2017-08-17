#!/usr/bin/env python
import dateutil.parser
from dateutil.tz import tzutc
import os

from .credentials import Credentials
from .lastfm import LastfmClient
from .spotify import SpotifyClient


def to_posix_timestamp(dt):
    """Converts dt to POSIX timestamp.

    Args:
        dt (datetime): The datetime object that is converted.

    Returns:
        int: The POSIX timestamp.
    """
    return int(dt.replace(tzinfo=tzutc()).timestamp())


def convert_to_lastfm(item):
    """Converts Spotify items to Last.fm tracks."""
    track = item['track']['name']
    artists = [a['name'] for a in item['track']['artists']]
    played_at = to_posix_timestamp(dateutil.parser.parse(item['played_at']))

    return {'name': track, 'artists': artists, 'played_at': played_at}


def scrobble(credentials_dict, spotify_client, lastfm_client):
    """Retrieves the 50 most recently played tracks from Spotify and scrobbles
    them to Last.fm.
    """

    user_credentials = Credentials.load_from_dict(credentials_dict)

    response = spotify_client.recently_played_tracks(user_credentials.spotify)
    tracks = [convert_to_lastfm(item) for item in response['items']]

    lastfm_client.scrobble(user_credentials.lastfm, tracks)

    # The credentials might have changed, so we return them to whoever
    # called us
    return user_credentials


if __name__ == "__main__":
    SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
    SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
    LASTFM_API_KEY = os.environ['LASTFM_API_KEY']
    LASTFM_API_SECRET = os.environ['LASTFM_API_SECRET']

    spotify_client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    lastfm_client = LastfmClient(LASTFM_API_KEY, LASTFM_API_SECRET)

    # TODO: Load the document from a file
    scrobble(credentials_dict, spotify_client, lastfm_client)
