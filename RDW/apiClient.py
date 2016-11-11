import requests


class ApiClient:
    """
        Author: Nick Bout
        Class: ApiClient
        This class uses the request library to make API calls
    """
    api_key = None
    api_url = None

    def __init__(self, url, key):
        """
            Constructor function to set necessary API variables

            ARGS:
                url STRING: API url
                key STRING: API key for authentication
        """
        self.api_url = url
        self.api_key = key

    def get(self, path, params = None):
        """
            Constructor function to set necessary API variables

            ARGS:
                path STRING: API url
                params DICT: API key for authentication
            RETURNS:
                DICT: returns API results in json format
        """
        # We can't give params default {} value because python is weird
        # http://stackoverflow.com/questions/9039191/mutable-default-method-arguments-in-python
        if not params:
            params = {}

        # NOTE: There should be a header argument so this class can be used for other api's but we don't use other api's
        data = requests.get(self.api_url + path, params = params, headers = {'ovio-api-key': self.api_key})

        if data.status_code == 200:
            return data.json()

        # API error
        raise Exception(data.reason)
