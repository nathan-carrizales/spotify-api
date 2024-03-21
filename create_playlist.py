"""
This script allows the user to extract a list of event names from ticketmaster, and then create a spotify playlist based
off of that list.
"""
from api.spotify import SpotifyClient
from api.ticketmaster import TicketmasterClient
import pandas as pd


def create_spotify_playlist(
        user_id: str,
        client_id: str,
        secret: str,
        token: str,
        artist_names: list,
        playlist_name: str = 'Untitled API Playlist',
        top_n_tracks: int = 3,
):
    """
    Creates a spotify playlist based off of a list of artists. Playlist has X number of songs from each artist and
    one podcast episode.

    :param user_id: Spotify username ID for signing in.
    :param client_id: Spotify client ID, associated with a Spotify 'app'.
    :param secret: Spotify secret, associated with a Spotify 'app'.
    :param token: Spotify token.
    :param playlist_name: Name of the Spotify playlist
    :param artist_names: List of artist names.
    :param top_n_tracks: Number of songs that will be added per artist.
    :return: None
    """

    # Create Spotify client
    spotify_client = SpotifyClient(
        client_id=client_id,
        client_secret=secret,
        token=token
    )

    # Create the playlist.
    playlist_id = spotify_client.create_playlist(
        user_id=user_id,
        playlist_name=playlist_name
    )['id']

    # For each artist in the artist list, attempt to find the spotify ID, and if it exists, add 3 songs and a podcast
    # episode.
    for ith_artist_name in set(artist_names):

        # get the artist ID
        ith_artist_id = spotify_client.get_artist_id_from_name(artist_name=ith_artist_name)

        # if the artist ID exists, continue
        if ith_artist_id:

            # add 'top_n_tracks' number of songs
            spotify_client.add_songs_from_artist_to_playlist(
                artist_id=ith_artist_id,
                playlist_id=playlist_id,
                n_tracks=top_n_tracks
            )

            # add a podcast episode
            spotify_client.add_podcast_to_playlist(
                artist_name=ith_artist_name,
                playlist_id=playlist_id
            )


def suggest_spotify_playlist_name(location_id: int, start: str, end: str) -> str:
    """
    Gives a nice readable name for a playlist.
    :param location_id: ticketmaster DMI
    :param start: start datetime
    :param end: end datetime
    :return: name of the playlist
    """

    df = pd.read_csv('ticketmaster_location_id.csv')
    df.index = df['Location ID']
    location_name = df.loc[location_id, 'Name']
    pretty_start_date = pd.to_datetime(start).strftime('%B %d')
    pretty_end_date = pd.to_datetime(end).strftime('%B %d')

    name = f'{location_name}, {pretty_start_date} - {pretty_end_date} (API)'

    return name


if __name__ == '__main__':
    from project_secrets import TICKETMASTER_CONSUMER_KEY, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_USER_ID,\
        SPOTIFY_TOKEN

    start_date = '2024-04-21'
    end_date = '2024-06-30'
    ticketmaster_location_id = 602  # https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/
    tracks_per_artist = 3

    artists = TicketmasterClient(token=TICKETMASTER_CONSUMER_KEY).get_music_events(
        start=start_date,
        end=end_date,
        location_id=ticketmaster_location_id,
        return_names_only=True
    )

    create_spotify_playlist(
        artist_names=artists,
        top_n_tracks=tracks_per_artist,
        secret=SPOTIFY_CLIENT_SECRET,
        client_id=SPOTIFY_CLIENT_ID,
        token=SPOTIFY_TOKEN,
        user_id=SPOTIFY_USER_ID,
        playlist_name=suggest_spotify_playlist_name(
            location_id=ticketmaster_location_id,
            start=start_date,
            end=end_date
        )
    )
