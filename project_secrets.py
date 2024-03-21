"""
Passwords, tokens, ID's, and any other classified information that is relevant for the project. All variables here are
available for use.
"""
from os import environ

# Spotify client ID and secret is associate with a Spotify "app". To create a spotify "app", visit the following URL
# 'https://developer.spotify.com/dashboard/applications'
SPOTIFY_CLIENT_ID = environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = environ.get('SPOTIFY_CLIENT_SECRET')

# Spotify user ID is what is used when logging into Spotify.
SPOTIFY_USER_ID = environ.get('SPOTIFY_USER_ID')

# Spotify token, which gets issued when authenticating with Spotify.
SPOTIFY_TOKEN = ''

# Ticketmaster token for accessing its API
TICKETMASTER_TOKEN = environ.get('TICKETMASTER_TOKEN')
