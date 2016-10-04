import requests


class ApiClient:
    api_key = None
    api_url = None

    def __init__(self, url, key):
        self.api_url = url
        self.api_key = key

    def get(self, path, params = {}):
        data = requests.get(self.api_url + path, params = params, headers = {'ovio-api-key': self.api_key})

        if data.status_code == 200:
            return data.json()

        # API error
        raise Exception(data.reason)
