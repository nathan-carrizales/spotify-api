"""
Spotify Client API for making requests
"""
import numpy as np
import json
from api.utility import _make_request
from typing import Dict


class SpotifyClient:
    """
    Client for Spotify API.
    """
    def __init__(self, client_id: str, client_secret: str, token: str):
        """
        :param client_id: client ID associated with Spotify 'app'
        :param client_secret: client secret associated with Spotify 'app'
        :param token: token for API calls
        """
        self._base_url = 'https://api.spotify.com/v1'
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token
        self._auth_headers = {'Authorization': f'Bearer {self.token}'}

    def search(self, query: str, query_type: str) -> Dict:
        """
        Generic searches. These can be either songs, albums, artists, or podcast episodes.
        :param query:
        :param query_type:
        :return: dictionary of results
        """

        supported_types = ['artist', 'episode', 'show']
        if query_type not in supported_types:
            raise NotImplementedError(f'"{query_type}" is not supported. Available options are {supported_types}')

        url = self._search_url + f'q={query}&type={query_type}'

        response = _make_request(
            request_method='get',
            url=url,
            headers=self._auth_headers
        )

        response_dictionary = response.json()

        return response_dictionary

    def get_user_config(self) -> Dict:
        """
        gets the user's config information
        :return: Dictionary
        """

        response = _make_request(
            request_method='get',
            url=self._config_url,
            headers=self._auth_headers
        )

        response_dictionary = response.json()

        return response_dictionary

    def get_top_tracks_from_artist(self, artist_id, market: str = 'ES') -> Dict:
        """
        Get top songs for the specified artist.
        :param artist_id: artist ID
        :param market: Spotify market
        :return: dictionary
        """

        url = self._artist_url + f'{artist_id}/top-tracks?market={market}'

        response = _make_request(
            request_method='get',
            url=url,
            headers=self._auth_headers
        )

        response_dictionary = response.json()

        return response_dictionary

    def create_playlist(self, user_id: str, playlist_name: str, public: bool = True) -> Dict:
        """
        Creates a playlist for user ID, with the name passed in.
        :param user_id: ID of the user
        :param playlist_name: Name of the playlist
        :param public: True if the playlist can be viewed by anyone
        :return: dictionary
        """

        url = self._user_url + f'{user_id}/playlists'

        data = {
            'name': playlist_name,
            'public': public,
        }

        response = _make_request(
            request_method='post',
            url=url,
            headers=self._auth_headers,
            data=json.dumps(data)
        )

        response_dictionary = response.json()

        return response_dictionary

    def add_entity_to_playlist(self, entity_ids: list, playlist_id: str) -> Dict:
        """
        Adds song, podcast, or other track to the playlist.
        :param entity_ids: list of track ID's
        :param playlist_id: playlist ID
        :return: dictionary
        """

        url = self._playlist_url + f'{playlist_id}/tracks'

        data = {
            "uris": entity_ids,
        }

        response = _make_request(
            request_method='post',
            url=url,
            headers=self._auth_headers,
            data=json.dumps(data)
        )

        response_dictionary = response.json()

        return response_dictionary

    def get_artist_id_from_name(self, artist_name: str) -> [Dict, None]:
        """
        Convert an artist name to artist ID.
        :param artist_name: name of the artist
        :return: Dictionary
        """

        # make a query to search for artist
        search_results = self.search(
            query=artist_name,
            query_type='artist'
        ).get('artists', {}).get('items')

        if search_results is None:
            return None

        else:

            # map the initial query to the name of the artist
            spotify_artist_id = None
            match_found = False
            number_of_attempts = 2
            counter = 0

            while not match_found:
                ith_artist = search_results[counter]

                if artist_name == ith_artist["name"]:
                    match_found = True
                    spotify_artist_id = ith_artist['id']
                    print(f'found artist "{artist_name}"!')

                if (counter == number_of_attempts) & (not match_found):
                    print(f'could not find artist {artist_name}')
                    return None

                else:
                    counter += 1

            return spotify_artist_id

    def add_songs_from_artist_to_playlist(self, artist_id: str, playlist_id: str, n_tracks: int) -> [None, Dict]:

        """

        :param artist_id:
        :param playlist_id:
        :param n_tracks:
        :return: Dictionary
        """

        top_tracks = self.get_top_tracks_from_artist(artist_id=artist_id).get('tracks', {})

        if top_tracks:

            number_of_tracks = min(
                [
                    len(top_tracks),
                    n_tracks
                ]
            )

            top_n_tracks_id = [f"spotify:track:{top_tracks[i]['id']}" for i in np.arange(number_of_tracks)]
            response = self.add_entity_to_playlist(
                entity_ids=top_n_tracks_id,
                playlist_id=playlist_id
            )

            return response

        else:
            return None

    def add_podcast_to_playlist(self, artist_name: str, playlist_id: str, n_tracks: int = 1) -> [None, Dict]:

        episodes_results = self.search(
            query=artist_name,
            query_type='episode'
        )

        if episodes_results:

            number_of_tracks = min(
                [
                    len(episodes_results['episodes']['items']),
                    n_tracks
                ]
            )

            episode_id = [
                f"spotify:episode:{episodes_results['episodes']['items'][i]['id']}" for i in np.arange(number_of_tracks)
            ]

            response = self.add_entity_to_playlist(
                entity_ids=episode_id,
                playlist_id=playlist_id
            )
            return response

        else:
            return None

    @property
    def _auth_url(self) -> str:
        auth_url = 'https://accounts.spotify.com/api/token'
        return auth_url

    @property
    def _search_url(self) -> str:
        search_url = f'{self._base_url}/search?'
        return search_url

    @property
    def _config_url(self) -> str:
        config_url = f'{self._base_url}/me'
        return config_url

    @property
    def _artist_url(self) -> str:
        artist_url = f'{self._base_url}/artists/'
        return artist_url

    @property
    def _user_url(self) -> str:
        user_url = f'{self._base_url}/users/'
        return user_url

    @property
    def _playlist_url(self) -> str:
        playlist_url = f'{self._base_url}/playlists/'
        return playlist_url


if __name__ == '__main__':
    from project_secrets import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_USER_ID

    spotify_client = SpotifyClient(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        token='BQA4jJVAsccS_5bZXChMeZOOWwN2O0aeIwy6zbYu26d_VErZpi7Gq6J2KE4r4VYQkxipNRwX38pGxTH-5PnB23cWEIasQ9EG6PA_JiN9AolrtJpCucw4b_RsIf1M7t4RHHa0pTRy009HYv1Wf23BCvkEvyENShW2ZJzCwxEfLAT3JC--7G3-bvKmvMpUaNhyN-sqw4xtpds9NH8RewA'

    )

    results = spotify_client.search(query='Bruno Mars', query_type='artist')

    print()