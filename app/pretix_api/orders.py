from .base import BaseAPI
import json


class OrdersApi(BaseAPI):
    def get(self, slug: str):
        orders = self._handle_pagination(
            self.client.config["events_url"]
            + slug
            + "/orders?include_canceled_positions=true"
        )
        return orders

    def get_positions(self, slug: str, filter_by_item_id=None):
        orders = self.get()

        positions = []
        for o in orders:
            positions.extend(o["positions"])
        if filter_by_item_id:
            positions = list(
                filter(lambda a: a["item"] in filter_by_item_id, positions)
            )
        return positions

    def get_positions(self, slug: str, filter_by_item_id=None):
        positions = self.get_positions(slug, filter_by_item_id)
        answers = []
        for p in positions:
            answers.extend(p["answers"])
        return answers

    def patch_position(
        self,
        event_slug: str,
        question_identifier: str,
        position_id: int,
        new_answer: str,
    ):

        question_id = self.client.questions.get_by_name(event_slug, question_identifier)

        r = self.client.session.get(
            f'{self.client.config["events_url"]}{event_slug}/orderpositions/{str(position_id)}/'
        )

        postions = self._check_response(r)

        answers = postions.get("answers")

        updated = False
        for a in answers:
            if int(a.get("question")) == question_id:
                a["answer"] = new_answer
                updated = True
                break

        if not updated:
            answers.append({"question": question_id, "answer": new_answer})

        # 3. PATCH full answers list
        update_dict = {"answers": answers}
        r = self.client.session.patch(
            f'{self.client.config["events_url"]}{event_slug}/orderpositions/{str(position_id)}/',
            json=update_dict,
        )
        return self._check_response(r)
