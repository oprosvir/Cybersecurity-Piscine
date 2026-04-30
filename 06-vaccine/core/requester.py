#!/usr/bin/env python3
import requests

class Requester:
    def __init__(self, timeout=5, headers=None):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Vaccine/1.0",
            "Accept": "*/*",
            "Connection": "close",
        }
        if headers:
            self.headers.update(headers)
            
    def send(self, method, url, params=None, data=None):
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            return {
                "status_code": response.status_code,
                "body": response.text,
                "headers": dict(response.headers),
                "url": response.url
            }
        except requests.RequestException as e:
            raise RuntimeError(f"HTTP request failed: {e}")
