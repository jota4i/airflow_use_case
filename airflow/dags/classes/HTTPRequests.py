import requests


class HTTPRequester:
    def __init__(self, url):
        self.url = url

    def make_request(self, method="GET", params=None, data=None, headers=None):
        response = requests.request(
            method=method, url=self.url, params=params, data=data, headers=headers
        )
        return response
