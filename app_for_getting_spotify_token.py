from flask import Flask, redirect, request
import urllib.parse
import requests
from project_secrets import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import base64

app = Flask(__name__)


PORT = 8888
REDIRECT_URI = f'http://127.0.0.1:{PORT}/callback'


@app.route('/login')
def login():

    query_params = {
        'response_type': 'code',
        'client_id': SPOTIFY_CLIENT_ID,
        'scope': 'playlist-modify-public',
        'redirect_uri': REDIRECT_URI,
    }

    redirect_url = 'https://accounts.spotify.com/authorize?' + urllib.parse.urlencode(query_params)

    html_response = redirect(redirect_url)

    return html_response


@app.route('/callback')
def callback():
    code = request.url.split('?')[1].split('=')[1]

    query_params = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }

    auth_headers = {
        'Authorization': f'Basic {base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request(
        method='post',
        url='https://accounts.spotify.com/api/token',
        headers=auth_headers,
        data=query_params
    ).json()

    token = response['access_token']
    scope = response['scope']
    expires_in = response['expires_in']

    content = f'Scope={scope} <br> Expiration={expires_in} seconds <br>Token={token} '

    return content


if __name__ == '__main__':
    app.run(port=PORT)
