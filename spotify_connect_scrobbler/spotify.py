#!/usr/bin/env python
import base64
import requests
import secrets
import sys

class SpotifyClient:
    """ A simple client for the Spotify Web API."""

    def __init__(self, creds):
        """Create Spotify client.

        Args:
            client_id (str): Identifies the client and the app.
            client_secret (str): API secret.
        """
        self.creds = creds

    def _make_authorization_headers(self):
        auth = "{}:{}".format(self.creds.__client_id, self.creds.__client_secret)
        auth_base64 = base64.b64encode(auth.encode('utf-8')).decode('utf-8')
        return {'Authorization': "Basic {}".format(auth_base64)}

    def refresh_access_token(self):
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
            'refresh_token': self.creds.refresh_token
        }
        headers = self._make_authorization_headers()
        return requests.post(
            'https://accounts.spotify.com/api/token',
            data=payload,
            headers=headers
        ).json()

    def recently_played_tracks(self):
        """Query Spotify for the recently played tracks of user.

        Args:
            auth (SpotifyCredentials): The authentication credentials returned
                by Spotify.

        Returns:
            dict: A dictionary including tracks and metadata.
        """
        payload = {}
        token = "{} {}".format(self.creds.token_type, self.creds.access_token)
        headers = {'Authorization': token}
        response = requests.get(
            'https://api.spotify.com/v1/me/player/recently-played?limit=50',
            data=payload,
            headers=headers
        )
        if response.ok:
            return response.json()
        elif response.status_code == 401:
            print("Spotify access token expired")
            self.creds.update(self.refresh_access_token())
            # Retry
            return self.recently_played_tracks()
        else:
            print(response.text)
            sys.exit(1)
