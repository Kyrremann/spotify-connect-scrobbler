class LastfmCredentials:
    """LastFM API credentials.

    Args:
        session_key (str): Session key returned by the authentication endpoint.
    """

    def __init__(self, api_key, api_secret, session_key):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session_key = session_key

    def todict(self):
        return {'api_key': self.api_key,
                'api_secret': self.api_secret,
                'session_key': self.session_key}


class SpotifyCredentials:
    """Spotify credentials contains access and refresh tokens for requests to
    the Spotify API. It does not call the API.

    Args:
        access_token (str): The access token.
        token_type (str): OAuth2 token type, e.g. 'Bearer'
        refresh_token (str): Token used to retrieve a new access token.
        scope (str): Scope for all API calls. This should not change often.
    """

    def __init__(self, client_id, client_secret, access_token, token_type, refresh_token, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.token_type = token_type
        self.refresh_token = refresh_token
        self.scope = scope

    def todict(self):
        return {'client_id': self.client_id,
                'client_secret': self.client_secret,
                'access_token': self.access_token,
                'token_type': self.token_type,
                'refresh_token': self.refresh_token,
                'scope': self.scope}

    def update(self, new_credentials):
        """Update the credentials after new tokens were retrieve with the
        refresh token.

        Args:
            new_credentials (dict): Parsed repsonse from Spotify's auth
            endpoint.
        """
        if 'access_token' in new_credentials:
            self.access_token = new_credentials['access_token']

        if 'refresh_token' in new_credentials:
            self.refresh_token = new_credentials['refresh_token']


class Credentials:
    """Main object for LastFM and Spotify credentials"""

    def __init__(self, lastfm, spotify, document_id=None):
        self.lastfm = lastfm
        self.spotify = spotify
        self.document_id = document_id

    def load_from_document(document):
        lastfm = LastfmCredentials(
            document['lastfm']['api_key'],
            document['lastfm']['api_secret'],
            document['lastfm']['session_key'])
        spotify = SpotifyCredentials(
            document['spotify']['client_id'],
            document['spotify']['client_secret'],
            document['spotify']['access_token'],
            document['spotify']['token_type'],
            document['spotify']['refresh_token'],
            document['spotify']['scope']
        )

        return Credentials(lastfm, spotify, str(document['_id']))

    def todict(self):
        data = {}

        if self.lastfm is not None:
            data['lastfm'] = self.lastfm.todict()

        if self.spotify is not None:
            data['spotify'] = self.spotify.todict()

        return data
