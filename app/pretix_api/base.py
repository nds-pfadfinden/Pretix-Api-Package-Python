class BaseAPI:
    def __init__(self, client):
        self.client = client

    def _url(self, event_slug: str, url_path: str) -> str:
        return f"{self.client.events_url}{event_slug}/{url_path}/"

    def _get(self, url: str):
        r = self.client.session.get(url)
        return self.client._check_response(r)

    def _post(self, url: str, data: dict):
        r = self.client.session.post(url, json=data)
        return self.client._check_response(r)

    def _patch(self, url: str, data: dict):
        r = self.client.session.patch(url, json=data)
        return self.client._check_response(r)

    def _delete(self, url: str):
        r = self.client.session.delete(url)
        return self.client._check_response(r)

    def _handle_pagination(self, url):
        data = []
        while True:
            r = self.client.session.get(url)
            self._check_response(r)
            data.extend(r.json()["results"])

            if not r.json()["next"]:
                break
            url = r.json()["next"]

        return data

    def _check_response(self, response):
        if not response.ok:
            print(response.status_code)
            print(response.text)
        response.raise_for_status()
        return response.json()
