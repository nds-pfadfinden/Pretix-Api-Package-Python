from .base import BaseAPI
import json


class CategoriesApi(BaseAPI):
    def create(self, event_slug: str, data: dict):
        r = self.session.post(
            f'{self.config["events_url"]}{event_slug}/categories/', json=data
        )
        return self._check_response(r)
