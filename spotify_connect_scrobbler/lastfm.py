#!/usr/bin/env python
import hashlib
import requests

class LastfmClient:
    """ A simple client for the Last.fm API."""

    def __init__(self, creds):
        """Creates a Last.fm client.

        Args:
            key (str): Web API key.
            secret (str): Web API secret.
        """
        self.creds = creds

    def sign(self, parameters):
        """ Generates the signature for autheorized API calls.

        Args:
            parameters (dict): Name and value of parameters for API call.

        Returns:
            string: Signature according to http://www.last.fm/api/webauth#6.
        """
        sorted_params = ("{}{}".format(k, parameters[k])
                         for k
                         in sorted(parameters))

        md5 = hashlib.md5()

        string = "{}{}".format(''.join(sorted_params), self.__secret)
        md5.update(string.encode('utf-8'))
        return md5.hexdigest()

    def scrobble(self, tracks):
        """ Scrobble tracks.

        Args:
            tracks (list(dict)): List over {name, artists, played_at}
            credentials (LastfmCredentials): LastFM API credentials object.
        """
        payload = {
            'api_key': self.creds.api_key,
            'method': 'track.scrobble',
            'sk': self.creds.session_key
        }

        for i, track in enumerate(tracks):
            payload["track[{}]".format(i)] = track['name']
            payload["artist[{}]".format(i)] = track['artists'][0]
            payload["timestamp[{}]".format(i)] = track['played_at']

        payload['api_sig'] = self.sign(payload)
        payload['format'] = 'json'
        return requests.post(
            'https://ws.audioscrobbler.com/2.0/', params=payload).json()
