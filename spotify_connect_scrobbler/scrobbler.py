#!/usr/bin/env python
import dateutil.parser
from dateutil.tz import tzutc
import os

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


def main(creds):
    """Retrieves the 50 most recently played tracks from Spotify and scrobbles
    them to Last.fm.
    """
    client = SpotifyClient(creds.spotify)
    response = client.recently_played_tracks()
    tracks = [convert_to_lastfm(item) for item in response['items']]

    fmclient = LastfmClient(creds.lastfm)
    scrobbles = fmclient.scrobble(tracks)

    # The credentials might have changed, so we return them to whoever called us
    return creds


if __name__ == "__main__":
    # Not supported anymore, or yet...
