import requests

class TossInvestClient:
    BASE_URL = "https://openapi.tossinvest.com"

    def __init__(self, credential_file="credentials"):
        self.account_seq = None
        self.access_token = None
        self.client_id = None
        self.client_secret = None
        self._load_credentials(credential_file)

    #################################################
    # credentials
    #################################################

    def _load_credentials(self, filename):
        data = {}
        with open(filename, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()
        self.client_id = data["client_id"]
        self.client_secret = data["client_secret"]

    #################################################
    # Token
    #################################################

    def authenticate(self):
        url = f"{self.BASE_URL}/oauth2/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        result = response.json()
        self.access_token = result["access_token"]
        return result

    #################################################
    # Header
    #################################################

    def _headers(self):
        if self.access_token is None:
            self.authenticate()
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        if self.account_seq:
            headers["X-Tossinvest-Account"] = self.account_seq
        return headers

    #################################################
    # Generic Request
    #################################################

    def request(self,
                method,
                endpoint,
                params=None,
                body=None,
                headers=None):

        url = self.BASE_URL + endpoint
        request_headers = self._headers()
        
        if headers:
            request_headers.update(headers)
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=request_headers,
            params=params,
            json=body
        )

        if response.status_code == 401:
            self.authenticate()
            request_headers = self._headers()
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=request_headers,
                params=params,
                json=body
            )
        response.raise_for_status()
        if response.text:
            return response.json()
        return None

    #################################################
    # Shortcut
    #################################################

    def get(self, endpoint, params=None):
        return self.request("GET", endpoint, params=params)

    def post(self, endpoint, body=None):
        return self.request("POST", endpoint, body=body)

    def put(self, endpoint, body=None):
        return self.request("PUT", endpoint, body=body)

    def delete(self, endpoint, body=None):
        return self.request("DELETE", endpoint, body=body)

    def patch(self, endpoint, body=None):
        return self.request("PATCH", endpoint, body=body)
