from rest.rest_base import HttpClient
import logging


class PlayPlatformService(HttpClient):
    def __init__(self):
        super().__init__()
        self.base_url = super().default_play_platform_url

    def get_arrangements(self, user_id, audience_id):
        rest_url = self.base_url + '/arrangements'
        super().get_service_token()

        if user_id is not None:
            rest_url = rest_url + '?joined=' + user_id
        if audience_id is not None:
            rest_url = rest_url + 'watched=' + audience_id

        arrangements_response = super().send_requests('GET', rest_url, req_body=None, req_headers=super().headers,
                                                      req_cookies=None)

        if len(arrangements_response.json()) == 0:
            logging.log('ERROR', 'no arrangements info')
        return arrangements_response.json()
