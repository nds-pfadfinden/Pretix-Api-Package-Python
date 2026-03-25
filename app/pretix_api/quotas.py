from .base import BaseAPI
import json


class QuotasApi(BaseAPI):

    def get(self, event_slug: str) -> list:
        quotas = self._handle_pagination(
            self.config["events_url"] + event_slug + "/quotas/"
        )
        return quotas

    def create(self, event_slug: str, data: dict):
        r = self.s.post(f'{self.config["events_url"]}{event_slug}/quotas/', json=data)
        return self._check_response(r)

    def update(self, event_slug: str, quota_id: int, update_dict: dict):
        r = self.s.patch(
            f'{self.config["events_url"]}{event_slug}/quotas/{quota_id}/',
            json=update_dict,
        )
        return self._check_response(r)
