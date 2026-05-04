import requests


class Requester:
    def __init__(self, headers, timeout=5):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Vaccine/1.0",
            "Accept": "*/*",
            "Connection": "close",
        }
        self.headers.update(headers)

    def send(self, config, params=None):
        if params is None:  # baseline request
            params = {p["name"]: p["value"] for p in config.params}
        try:
            if config.method == "GET":
                return requests.get(
                    config.url,
                    params=params,
                    headers=self.headers,
                    timeout=self.timeout,
                    allow_redirects=True,
                )
            else:
                return requests.post(
                    config.url,
                    data=params,
                    headers=self.headers,
                    timeout=self.timeout,
                    allow_redirects=True,
                )
        except requests.RequestException as e:
            raise RuntimeError(f"HTTP request failed: {e}")
