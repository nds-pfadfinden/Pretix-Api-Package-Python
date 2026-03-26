from .base import BaseAPI
import json
from typing import List, Dict


class ItemsApi(BaseAPI):
    # GET Items

    def get_items(self, event_slug: str):
        items = self._handle_pagination(
            self.client.config["events_url"] + event_slug + "/items"
        )
        return items

    # create item
    def add_item(self, event_slug: str, data: dict):
        r = self.client.session.post(
            f'{self.client.config["events_url"]}{event_slug}/items/', json=data
        )
        return self._check_response(r)

    def add_items_with_questions(
        self, event_slug: str, item: dict, questions: List[Dict]
    ):
        item = self.add_item(event_slug=event_slug, data=item)

        for question in questions:
            question["item"] = [item["id"]]
            self.create_question(event_slug, question)

    def add_items_with_questions_by_question_name(
        self, event_slug: str, item: dict, question_identifiers: List[str]
    ):
        item = self.add_item(event_slug=event_slug, data=item)
        existing_questions = self.client.questions.get(event_slug=event_slug)

        for new_question in question_identifiers:
            identifier_norm = str(new_question).strip().lower()
            current_question = None

            for q in existing_questions:
                if str(q.get("identifier", "")).strip().lower() == identifier_norm:
                    current_question = q
                    break

            if current_question is None:
                raise KeyError(f'Question with identifier "{new_question}" not found')

            current_items = current_question.get("items", [])

            if item["id"] not in current_items:
                current_items = current_items + [item["id"]]

                self.client.questions.patch(
                    event_slug, current_question["id"], {"items": current_items}
                )

        return item

    # Patch Items

    def change_item(self, id: int, event_slug: str, update_dict: dict):
        r = self.client.session.patch(
            f'{self.client.config["events_url"]}{event_slug}/items/{str(id)}/',
            json=update_dict,
        )
        return self._check_response(r)
