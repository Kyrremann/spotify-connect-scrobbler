import json

from spotify_connect_scrobbler import credentials


def test_todict():
    lastfm = credentials.LastfmCredentials("some_key")
    spotify = credentials.SpotifyCredentials(
            "some_access",
            "Bearer",
            "refreshing",
            "scoping")
    creds = credentials.Credentials(lastfm, spotify)

    data = creds.todict()
    assert str(data) == ("{'lastfm': {'session_key': 'some_key'}, "
                         "'spotify': {'access_token': 'some_access', "
                         "'token_type': 'Bearer', "
                         "'refresh_token': 'refreshing', "
                         "'scope': 'scoping'}}")


def test_load_from_dict():
    with open('tests/fixtures/credentials.json', 'r') as f:
        document = json.load(f)

    creds = credentials.Credentials.load_from_dict(document)

    assert creds.lastfm.session_key == "other_key"
    assert creds.spotify.access_token == "other_access"
    assert creds.spotify.token_type == "Bearer"
    assert creds.spotify.refresh_token == "more refreshing"
    assert creds.spotify.scope == "scoped"
