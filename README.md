# Spotify-API

This project aims at enabling users to use the Spotify and Ticketmaster API to dynamically create playlists.

## Create Spotify Playlist using Ticketmaster and Spotify API

The script `create_playlist.py` allows to create a Spotify playlist based  off of artists coming to an area
according to Ticketmaster. Users can pick the start and end date, location ID, and number of songs for each artist.

The default behavior adds the top 3 songs of each artist as well as one podcast episode featuring them.
To use the script, users must have access to the Ticketmaster and Spotify API.

## Ticketmaster API

To use the Ticketmaster API, users must have a token called the client "Consumer Key". To create a consumer key, the
user needs to create an "App" via the Ticketmaster developer portal. For more information on how to do this, visit the
link below

https://developer.ticketmaster.com/products-and-docs/apis/getting-started/

## Spotify API

To use the Spotify API, users must have a Spotify account and the following:
1. User ID
2. Client ID
3. Client secret
4. Access token

## Environment variables

`SPOTIFY_CLIENT_ID` - Client ID associated with a developer App

`SPOTIFY_CLIENT_SECRET` - Client secret associated with a developer App

`SPOTIFY_USER_ID` - User ID when logging into Spotify

`SPOTIFY_TOKEN` - Token for API calls, issued only through running "app_for_getting_spotify_token.py"

`TICKETMASTER_CONSUMER_KEY` Consumer key associated with a Tickermaster developer App

## Generating a Spotify API token

Spotify API tokens only last for one hour, and can only be issued by local authentication by running 
`app_for_getting_spotify_token.py`. To begin, first start by whitelisting the "Redirect URI".

1. Visit https://developer.spotify.com/ and login
2. Navigate to the dashboard https://developer.spotify.com/dashboard
3. Select the appropriate "App"
4. Select "Settings"
5. Add the "Redirect URI" in the *Redirect URIs* section

To generate the token:

1. Run `app_for_getting_spotify_token.py`
2. Using any browser, navigate to the URL "http://127.0.0.1:8888/login"
3. Follow the instructions and enter the user ID and password for Spotify authentication.
4. Upon signing in, a HTML page should show the token, scope, and expiration. Copy and paste the token to the variable `SPOTIFY_TOKEN` in the project_secrets.py  
