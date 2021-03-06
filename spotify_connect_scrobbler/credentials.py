class LastfmCredentials:
    """LastFM API credentials.

    Args:
        session_key (str): Session key returned by the authentication endpoint.
    """

    def __init__(self, session_key):
        self.session_key = session_key

    def todict(self):
        return {'session_key': self.session_key}


class SpotifyCredentials:
    """Spotify credentials contains access and refresh tokens for requests to
    the Spotify API. It does not call the API.

    Args:
        access_token (str): The access token.
        token_type (str): OAuth2 token type, e.g. 'Bearer'
        refresh_token (str): Token used to retrieve a new access token.
        scope (str): Scope for all API calls. This should not change often.
    """

    def __init__(self, access_token, token_type, refresh_token, scope):
        self.access_token = access_token
        self.token_type = token_type
        self.refresh_token = refresh_token
        self.scope = scope

    def todict(self):
        return {'access_token': self.access_token,
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

    def __init__(self, lastfm, spotify):
        self.lastfm = lastfm
        self.spotify = spotify

    def load_from_dict(credentials_dict):
        """Load Spotify and Lastfm credentials from a dict.

        Args:
            credentials_dict: A dictonary with the credentials.
            Need to look like this:
                   {
                     'lastfm': { 'session_key': 'key' }
                     'spotify: {
                       'access_token': 'token',
                       'token_type': 'the type of token',
                       'refresh_token': 'token',
                       'scope': 'scope of the credentials',
                   }
        """
        lastfm = LastfmCredentials(
            credentials_dict['lastfm']['session_key'])
        spotify = SpotifyCredentials(
            credentials_dict['spotify']['access_token'],
            credentials_dict['spotify']['token_type'],
            credentials_dict['spotify']['refresh_token'],
            credentials_dict['spotify']['scope']
        )

        return Credentials(lastfm, spotify)

    def todict(self):
        data = {}

        if self.lastfm is not None:
            data['lastfm'] = self.lastfm.todict()

        if self.spotify is not None:
            data['spotify'] = self.spotify.todict()

        return data
