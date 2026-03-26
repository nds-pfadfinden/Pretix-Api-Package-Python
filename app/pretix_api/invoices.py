from .base import BaseAPI
import json


class InvoicesApi(BaseAPI):

    def get_invoices(self, event_slug: str) -> list[dict]:
        invoices = self._handle_pagination(
            self.config["events_url"] + event_slug + "/invoices/"
        )
        return invoices

    def download_invoice(
        self, event_slug: str, invoice_number: str, path: str, invoice_filename=""
    ) -> None:
        if invoice_filename == "":
            invoice_filename = invoice_number

        invoice_pdf_r = self.client.session.get(
            f'{self.config["events_url"]}{event_slug}/invoices/{invoice_number}/download/'
        )
        with open(path + f"\\{invoice_filename}.pdf", "wb") as f:
            f.write(invoice_pdf_r.content)

        return

    def download_all_invoices(self, event_slug: str, path: str) -> None:
        invoices = self.get_invoices(event_slug)
        for invoice in invoices:
            self.download_invoice(event_slug, invoice["number"], path)

        return
