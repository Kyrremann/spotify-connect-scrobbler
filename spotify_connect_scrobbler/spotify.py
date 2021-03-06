#!/usr/bin/env python
import base64
import requests
import secrets

from .credentials import SpotifyCredentials


class SpotifyClient:
    """ A simple client for the Spotify Web API."""

    def __init__(self, client_id, client_secret):
        """Create Spotify client.

        Args:
            client_id (str): Identifies the client and the app.
            client_secret (str): API secret.
        """
        self.__client_id = client_id
        self.__client_secret = client_secret

    def _make_authorization_headers(self):
        auth = "{}:{}".format(self.__client_id, self.__client_secret)
        auth_base64 = base64.b64encode(auth.encode('utf-8')).decode('utf-8')
        return {'Authorization': "Basic {}".format(auth_base64)}

    def request_authorization(self, redirect_uri):
        """Returns an URL the user has to follow to authorize this app.

        Args:
            redirect_uri (str): Spotify redirects to this URL.
        """

        # Requests authorization
        request_secret = secrets.token_hex()
        payload = {
            'client_id': self.__client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'scope': 'user-read-recently-played',
            'state': request_secret
        }
        params = ("{}={}".format(param, value)
                  for param, value
                  in payload.items())
        auth_url = 'https://accounts.spotify.com/authorize?{}'.format(
            '&'.join(params))
        return auth_url

    def request_access_token(self, code, redirect_uri):
        """ Returns the access token for Spotify Web API.

        Args:
            code (string): The code passed by the authorization redirect.
            redirect_uri (str): Spotify redirectes to this URL.

        Returns:
            dict: The response from Spotify.
        """

        # Get auth token
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': self.__client_id,
            'client_secret': self.__client_secret
        }
        response = requests.post(
            'https://accounts.spotify.com/api/token', data=payload).json()

        return SpotifyCredentials(
            response['access_token'],
            response['token_type'],
            response['refresh_token'],
            response['scope'])

    def refresh_access_token(self, refresh_token):
        """ Returns the access token for Spotify Web API using a refresh token.

        Args:
            refresh_token (string): The token has been returned by the access
            token request.

        Returns:
            SpotifyCredentials: The parsed response from Spotify.
        """
        # Get new auth token
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        headers = self._make_authorization_headers()
        return requests.post(
            'https://accounts.spotify.com/api/token',
            data=payload,
            headers=headers
        ).json()

    def recently_played_tracks(self, credentials):
        """Query Spotify for the recently played tracks of user.

        Args:
            credentials (SpotifyCredentials): The authentication
                credentials returned by Spotify.

        Returns:
            dict: A dictionary including tracks and metadata.
        """
        return self.get_request_spotify(
            credentials,
            'https://api.spotify.com/v1/me/player/recently-played?limit=50')

    def get_track(self, track_id, credentials):
        """Get Spotify catalog information for a single track identified by
        its unique Spotify ID.

        Args:
            track_id: The Spotify ID for the track
            credentials (SpotifyCredentials): The authentication
                credentials returned by Spotify.

        Returns:
            dict: A dictionary including track information.
        """
        return self.get_request_spotify(
            credentials,
            'https://api.spotify.com/v1/tracks/{}'.format(track_id))

    def get_user_id(self, credentials):
        """Retrieves the username of the Spotify user.

        Args:
            credentials (SpotifyCredentials): The authentication
                credentials returned by Spotify.

        Returns:
            str: The username of the Spotify user.
        """
        return self.get_request_spotify(
            credentials,
            'https://api.spotify.com/v1/me')['id']

    def get_request_spotify(self, credentials, request_url):
        """Runs HTTP-GET request.

        Args:
            credentials (SpotifyCredentials): The authentication
                credentials returned by Spotify.
            request_url (Str): The URL to HTTP-GET.

        Returns:
            dict: A dictionary representation of the json-response.
        """
        payload = {}
        token = "{} {}".format(credentials.token_type,
                               credentials.access_token)
        headers = {'Authorization': token}
        response = requests.get(
            request_url,
            data=payload,
            headers=headers
        )
        if response.ok:
            return response.json()
        elif response.status_code == 401:
            print("Spotify access token expired")
            # TODO We should note that this function changes the object used,
            # or just return the result from refresh_access_token()
            credentials.update(
                self.refresh_access_token(credentials.refresh_token)
            )
            # Retry
            return self.get_request_spotify(credentials, request_url)
        else:
            print(response.text)
            raise Exception(
                'Got status code {} from Spotify, which we don\'t'
                .format(response.status_code))
