from .base import BaseAPI
import json


class QuestionsApi(BaseAPI):
    def create(self, event_slug: str, data: dict):
        r = self.session.post(
            f'{self.config["events_url"]}{event_slug}/questions/', json=data
        )
        return self._check_response(r)

    def get(self, event_slug: str) -> list[dict]:
        questions = self._handle_pagination(
            self.config["events_url"] + event_slug + "/questions/"
        )
        return questions

    def patch(self, event_slug: str, question_id: int, data: dict) -> dict:
        r = self.session.patch(
            f'{self.config["events_url"]}{event_slug}/questions/{question_id}/',
            json=data,
        )
        return self._check_response(r)

    def get_id(self, event_slug: str, identifier: str) -> int:
        questions = self.get_questions(event_slug=event_slug)
        identifier_norm = str(identifier).strip().lower()
        for q in questions:
            if str(q.get("identifier", "")).strip().lower() == identifier_norm:
                return int(q["id"])

        raise KeyError(f"Question identifier not found: {identifier}")
