from .base import BaseAPI


class TransactionsApi(BaseAPI):

    def get(self, event_slug: str) -> list:
        quotas = self._handle_pagination(
            self.client.config["events_url"] + event_slug + "/transactions/"
        )
        return quotas

    def get_all_for_organizer(
        self,
    ) -> list:
        quotas = self._handle_pagination(
            self.client.config["organizer_url"] + "transactions/"
        )
        return quotas
