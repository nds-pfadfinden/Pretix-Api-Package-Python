import requests


class PretixClient:
    def __init__(self, organizer_url: str, api_token: str) -> None:
        """
        Args:
        events_url (String) -> Url for the Pretix-Organizer (default from .env file)
        api_token (String) -> API Token for the Pretix-Organizer (default from .env file)
        """

        self.s = requests.Session()
        self.config = {
            "organizer_url": organizer_url,
            "events_url": f"{organizer_url}events/",
        }
        self.authHeader = {
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json",
        }
        self.session.headers.update(self.authHeader)

        from .items import ItemsApi
        from .questions import QuestionsApi
        from .categories import CategoriesApi

        from .categories import CategoriesApi
        from .events import EventsApi
        from .invoices import InvoicesApi
        from .orders import OrdersApi
        from .quotas import QuotasApi

        self.items = ItemsApi(self)
        self.questions = QuestionsApi(self)
        self.categories = CategoriesApi(self)
        self.events = EventsApi(self)
        self.invoices = InvoicesApi(self)
        self.orders = OrdersApi(self)
        self.quotas = QuotasApi(self)

    def __del__(self) -> None:
        self.session.close()
        return

    def _check_response(self, response):
        response.raise_for_status()
        return response.json()

    def _handle_pagination(self, url):
        data = []
        while True:
            r = self.session.get(url)
            self._check_response(r)
            data.extend(r.json()["results"])

            if not r.json()["next"]:
                break
            url = r.json()["next"]

        return data
