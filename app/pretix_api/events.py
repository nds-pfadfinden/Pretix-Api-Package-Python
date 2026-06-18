from .base import BaseAPI
import json


class EventsApi(BaseAPI):

    def get_event(self, slug):
        r = self.client.session.get(f'{self.client.config["events_url"]}{slug}/')

        return self.client._check_response(r)

    def get_events(self, exclude_slugs: list[str] = []):

        events = self._handle_pagination(self.client.config["events_url"])
        preferred_langs = ["en", "de"]
        events = [
            {
                "event_slug": d["slug"],
                "shop_name": next(
                    (d["name"][lang] for lang in preferred_langs if lang in d["name"]),
                    None,
                ),
                "public_url": d["public_url"],
                "backend_url": self.client.config["organizer_url"] + d["slug"],
            }
            for d in events
            if not any(s in d["slug"] for s in exclude_slugs)
        ]

        return events

    # POST Requests for Events

    def create_event(self, file_path: str, update_dict={}):
        """
        method to create Events

        can't create plugins or saleschannels

        Args:
            file_path (String): path to json file with object to create an event
            update_dict (dict, optional): dict to update the json object.  Defaults to {}.

        Returns:
            response status
        """

        with open(file_path, "r") as read_file:
            data = json.load(read_file)
        data.update(update_dict)

        r = self.client.session.post(self.client.config["events_url"], json=data)

        return self.client._check_response(r)

    def clone(self, event_slug: str, update_dict: dict):
        """
        method to Clone Events

        Args:
            file_path (String): path to json file with object to create an event
            update_dict (dict, optional): dict to update the json object.  Defaults to {}.

        Returns:
            response status
        """

        r = self.client.session.post(
            url=f'{self.client.config["events_url"]}{event_slug}/clone/',
            json=update_dict,
        )

        return self._check_response(r)

    # Patch Events

    def change(self, event_slug: str, data: dict):
        r = self.client.session.patch(
            f'{self.client.config["events_url"]}{event_slug}/', json=data
        )
        return self._check_response(r)

    # Delete Events

    def delete(self, event_slug: str):
        r = self.client.session.delete(
            f'{self.client.config["events_url"]}{event_slug}/'
        )
        return self._check_response(r)
