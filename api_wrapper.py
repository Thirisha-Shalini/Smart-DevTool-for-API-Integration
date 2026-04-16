import requests

class APIWrapper:
    def __init__(self, base_url, token=None, api_key=None):
        self.base_url = base_url
        self.session = requests.Session()
        self.token = token
        self.api_key = api_key

    def set_auth(self, token=None, api_key=None):
        if token:
            self.token = token
        if api_key:
            self.api_key = api_key

    def get(self, path, params=None):
        headers = self._get_headers()
        url = self.base_url + path
        response = self.session.get(url, headers=headers, params=params)
        return self._handle_response(response)

    def post(self, path, data=None):
        headers = self._get_headers()
        url = self.base_url + path
        response = self.session.post(url, headers=headers, json=data)
        return self._handle_response(response)

    def put(self, path, data=None):
        headers = self._get_headers()
        url = self.base_url + path
        response = self.session.put(url, headers=headers, json=data)
        return self._handle_response(response)

    def delete(self, path):
        headers = self._get_headers()
        url = self.base_url + path
        response = self.session.delete(url, headers=headers)
        return self._handle_response(response)

    def _get_headers(self):
        headers = {}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        if self.api_key:
            headers['x-api-key'] = self.api_key
        return headers

    def _handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

# Usage: wrapper = APIWrapper(base_url, token='...', api_key='...')