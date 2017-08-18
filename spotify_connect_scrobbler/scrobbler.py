#!/usr/bin/env python
import dateutil.parser
from dateutil.tz import tzutc

from .credentials import Credentials


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
