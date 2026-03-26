class BaseAPI:
    def __init__(self, client):
        self.client = client

    def _url(self, event_slug: str, url_path: str) -> str:
        return f"{self.client.events_url}{event_slug}/{url_path}/"

    def _get(self, url: str):
        r = self.client.client.session.get(url)
        return self.client._check_response(r)

    def _post(self, url: str, data: dict):
        r = self.client.client.session.post(url, json=data)
        return self.client._check_response(r)

    def _patch(self, url: str, data: dict):
        r = self.client.client.session.patch(url, json=data)
        return self.client._check_response(r)

    def _delete(self, url: str):
        r = self.client.client.session.delete(url)
        return self.client._check_response(r)
