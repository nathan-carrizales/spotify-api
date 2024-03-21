from setuptools import setup, find_packages

setup(
    name='spotify-api',
    version='0.1.0',
    description='Client for making Spotify playlists',
    url='',
    author='Nathan Carrizales',
    license='Proprietary',
    zip_safe=False,
    packages=find_packages(include=['spotify_api']),
    install_requires=[
        'requests==2.28.2',
        'pandas==1.5.0',
    ]
)
