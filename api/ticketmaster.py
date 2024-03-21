"""
TicketMaster Client API for making requests
"""
import pandas as pd
from api.utility import _make_request
from typing import Dict
import datetime as dt


class TicketmasterClient:
    """Client API"""
    def __init__(self, token: str):
        """
        Parameters
        :param token: Ticketmaster API token.
        """
        self.token = token

    def get_music_events(
            self,
            start: str,
            end: str,
            location_id: int,
            return_names_only: bool,
            page_limit: int = 180
    ) -> list:
        """
        Get a list of artist names based off of query arguments.
        :param start: start datetime search
        :param end: end datetime search
        :param page_limit: number of pages to return. More pages means more results.
        :param location_id: DMA -> https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/
        :param return_names_only: Setting to 'True' will return a list of just the event names. 'False' will return
            the default.
        :return: list
        """

        # format the start and end times.
        start = self._datetime_str_to_datetime_obj(start)
        end = self._datetime_str_to_datetime_obj(end)

        base_url = 'https://app.ticketmaster.com/discovery/v2/events.json'

        full_url = f'{base_url}?' \
                   f'classificationName=music' \
                   f'&startDateTime={start}' \
                   f'&endDateTime={end}' \
                   f'&size={page_limit}' \
                   f'&dmaId={location_id}' \
                   f'&apikey={self.token}'

        response = _make_request(request_method='get', url=full_url)

        if '_embedded' not in response.json().keys():
            raise KeyError('Could not find any events')

        events = response.json()['_embedded']['events']

        if return_names_only:

            name_only_events = list()

            for e in events:

                try:
                    dummy = e['_embedded']['attractions'][0]['name']
                    name_only_events.append(dummy)
                except KeyError:
                    pass

            return name_only_events

        else:
            return events

    @staticmethod
    def _datetime_str_to_datetime_obj(date: str) -> dt.datetime:
        """
        convert date into a datetime object with the correct format
        :param date:
        :return: datetime object
        """

        formatted_date = pd.to_datetime(date).strftime('%Y-%m-%dT00:00:00Z')

        return formatted_date


