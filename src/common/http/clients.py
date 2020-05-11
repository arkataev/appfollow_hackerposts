import requests


class HttpClientError(Exception):
    pass


class SimpleHttpClient:
    """A very basic http-client for demo purposes"""

    @property
    def session(self) -> requests.Session:
        if not self._session:
            self._session = requests.Session()
        return self._session

    def __init__(self):
        self._session = None

    def send(self, **kwargs) -> requests.Response:
        p_request = requests.Request(**kwargs).prepare()

        response = self.session.send(p_request, timeout=15)

        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise HttpClientError(e)

        return response
