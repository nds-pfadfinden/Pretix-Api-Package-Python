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

    def get_events_and_orders(self):

        events = self.client.events.get_events()
        orders = []

        for event in events:
            order = [
                {
                    **{"order_" + k: v for k, v in order.items()},
                    **event,
                }
                for order in self.get(event["event_slug"])
            ]
            orders.extend(order)

        return orders

    def get_events_and_orders_and_positions(self):

        orders = self.get_events_and_orders()
        positions = []
        for order in orders:
            for pos in order.get("order_positions", []):
                positions.append(
                    {
                        "event_slug": order["event_slug"],
                        "position_internal_id": pos["id"],
                        **{"position_" + k: v for k, v in pos.items()},
                    }
                )

        items = []
        for slug in {order["event_slug"] for order in orders}:
            items.extend(self.client.items.get_items(slug))

        items_by_id = {item["id"]: item for item in items}
        return [
            {
                **pos,
                **{
                    "item_" + k: v
                    for k, v in items_by_id.get(pos["position_item"], {}).items()
                },
            }
            for pos in positions
        ]

    def get_events_and_orders_and_positions_and_payment_details(self):

        positions = self.get_events_and_orders_and_positions()
        payment_details = []

        for pos in positions:
            payment = [
                {
                    **{"payment_" + k: v for k, v in pay.items()},
                    **pos,
                }
                for pay in self.get_payment_details(
                    pos["event_slug"], pos["order_order_code"]
                )
            ]
            payment_details.extend(payment)

        return payment_details

    def get_positions(self, slug: str, filter_by_item_id=None):
        orders = self.get(slug)

        positions = []
        for o in orders:
            positions.extend(o["positions"])
        if filter_by_item_id:
            positions = list(
                filter(lambda a: a["item"] in filter_by_item_id, positions)
            )
        return positions

    def get_answers(self, slug: str, filter_by_item_id=None):
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
        if new_answer is None or str(new_answer).strip() == "":
            return None

        question = self.client.questions.get_by_name(event_slug, question_identifier)
        question_id = question["id"]

        r = self.client.session.get(
            f'{self.client.config["events_url"]}{event_slug}/orderpositions/{position_id}/'
        )
        position = self._check_response(r)

        answers = position.get("answers") or []

        answers = [a for a in answers if a.get("answer") not in [None, ""]]

        updated = False

        for a in answers:
            if int(a.get("question")) == int(question_id):
                a["answer"] = str(new_answer)
                updated = True
                break

        if not updated:
            answers.append(
                {
                    "question": int(question_id),
                    "answer": str(new_answer),
                }
            )

        payload = {"answers": answers}

        r = self.client.session.patch(
            f'{self.client.config["events_url"]}{event_slug}/orderpositions/{position_id}/',
            json=payload,
        )

        return self._check_response(r)

    def get_payment_details(self, slug: str, order_code: str):
        payment_details = self._handle_pagination(
            self.client.config["events_url"]
            + slug
            + "/orders/"
            + order_code
            + "/payments/"
        )
        return payment_details
