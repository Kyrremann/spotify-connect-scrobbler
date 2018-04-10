# A Spotify Connect Scrobbler

[![Build Status](https://travis-ci.org/Kyrremann/spotify-connect-scrobbler.svg?branch=master)](https://travis-ci.org/Kyrremann/spotify-connect-scrobbler)
[![codecov](https://codecov.io/gh/Kyrremann/spotify-connect-scrobbler/branch/master/graph/badge.svg)](https://codecov.io/gh/Kyrremann/spotify-connect-scrobbler)

A Small library That Scrobbles Spotify Connect Plays

# Setup

The Scrobbler is written for Python3.6 and up, and it dosn't have an CLI any more. At least for now.
It's purely a library that you can interact with through your Python application.

See below for a simple example where the users credentials is retreive from OS ENVS:

```python
from spotify_connect_scrobbler import scrobbler
from database import Database

import sys
import os
import json


def start_scrobbling():
    spotify_client = scrobbler.SpotifyClient(
        os.environ['SPOTIFY_CLIENT_ID'],
        os.environ['SPOTIFY_CLIENT_SECRET'])
    lastfm_client = scrobbler.LastfmClient(
        os.environ['LASTFM_API_KEY'],
        os.environ['LASTFM_API_SECRET'])

    user_credentials = {
        "lastfm": {
            "session_key": os.environ['LASTFM_SESSION_KEY']
        },
        "spotify": {
            "access_token": os.environ['SPOTIFY_ACCESS_TOKEN'],
            "token_type": os.environ['SPOTIFY_BEARER'],
            "refresh_token": os.environ['SPOTIFY_REFRESH_TOKEN'],
            "scope": os.environ['SPOTIFY_SCOPE']
        }
    }

    credentials = scrobbler.scrobble(
        user_credentials, spotify_client, lastfm_client)


if __name__ == "__main__":
       start_scrobbling()
```

As you can see, the library require that you create the `LastfmClient` and `SpotifyClient` for it, so it won't dictate how you store you credentials and keys. Also, the method `scrobble.scrobble()` will return an updated user credentials if it's been changed. A typical scenario for this, is when the Spotify access token has expired.

# Build Instructions

We use tox for building and testing. Just install and run tox

  ```
  pip install tox
  tox
  ```
