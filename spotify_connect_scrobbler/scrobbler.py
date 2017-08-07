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


# Maybe use a better name, scrobble()?
def main(json_document):
    """Retrieves the 50 most recently played tracks from Spotify and scrobbles
    them to Last.fm.
    """

    # TODO: Maybe send these variables as arguments to the method
    SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
    SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
    LASTFM_API_KEY = os.environ['LASTFM_API_KEY']
    LASTFM_API_SECRET = os.environ['LASTFM_API_SECRET']

    # TODO: We should handle a document with several users, so we can iterate over them later
    user_credentials = Credentials.load_from_document(json_document)

    client = SpotifyClient(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    fmclient = LastfmClient(LASTFM_API_KEY, LASTFM_API_SECRET)

    # while something
    response = client.recently_played_tracks(user_credentials.spotify)
    tracks = [convert_to_lastfm(item) for item in response['items']]

    scrobbles = fmclient.scrobble(user_credentials.lastfm, tracks)
    # while end

    # The credentials might have changed, so we return them to whoever called us
    # TODO: How to do this with several users, export the json?
    return user_credentials


if __name__ == "__main__":
    print("Not supported anymore, or yet...")
