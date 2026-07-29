# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class GenerateVA(models.TransientModel):
    """
    Wizard to generate a Virtual Account (VA) generator document
    (``va_generator``) out of the record(s) it is launched from,
    whatever their model. Reads the source model/record IDs from the
    context (``active_model``/``active_ids``) instead of storing them
    on any field, populates the resulting document's
    ``source_data_ids`` with one line per source record, and leaves it
    in the ``draft`` state for manual review/confirmation.
    """

    _name = "generate_va"
    _description = "Generate Virtual Account"

    type_id = fields.Many2one(
        string="Generator Type",
        comodel_name="va_generator_type",
        required=True,
        help="Generator type whose python_code computes the unique VA "
        "code. Generator types restricted to a model different from "
        "the model this wizard is launched from are rejected when "
        "Generate VA is pressed.",
    )
    bank_id = fields.Many2one(
        string="Bank",
        comodel_name="res.bank",
        required=True,
        help="Bank the generated Virtual Account numbers are for. "
        "Restricts the selectable Biller to those holding a Virtual "
        "Account code for this bank, and is carried over to the "
        "resulting va_generator document, which in turn restricts the "
        "generated Virtual Account bank accounts to this bank only.",
    )
    biller_id = fields.Many2one(
        string="Biller",
        comodel_name="va_biller",
        required=True,
        domain="[('bank_code_ids.bank_id', '=', bank_id)]",
        help="Biller the generated Virtual Account numbers are for.",
    )
    merchant_id = fields.Many2one(
        string="Merchant",
        comodel_name="va_biller_merchant",
        required=False,
        domain="[('biller_code_ids.biller_id.va_biller_id', '=', biller_id)]",
        help="Optional merchant under the selected biller. Only "
        "merchants that have a biller code registered for the selected "
        "biller are offered. Left empty, Virtual Account numbers are "
        "generated at biller level.",
    )
    usage_id = fields.Many2one(
        string="Bank Account Usage",
        comodel_name="res_partner_bank_usage",
        required=False,
        help="Usage/purpose carried over to the resulting va_generator "
        "document, which in turn copies it to every generated "
        "res.partner.bank. Left empty, the resulting document is "
        "created with no usage set.",
    )

    @api.onchange("bank_id")
    def onchange_biller_id(self):
        self.biller_id = False

    @api.onchange("bank_id")
    def onchange_merchant_id(self):
        self.merchant_id = False

    def action_generate(self):
        for record in self.sudo():
            result = record._generate()
        return result

    def _generate(self):
        self.ensure_one()
        self._check_type_id()
        generator = self.env["va_generator"].create(self._prepare_va_generator_data())
        return self._open_va_generator(generator)

    def _get_source_model_criteria(self):
        active_model = self.env.context.get("active_model")
        return [("model", "=", active_model)]

    def _get_source_model(self):
        self.ensure_one()
        active_model = self.env.context.get("active_model")
        model = (
            self.env["ir.model"].search(self._get_source_model_criteria(), limit=1)
            if active_model
            else self.env["ir.model"]
        )
        if not active_model or not model:
            error_message = """
Document Type: %s
Context: Generate Virtual Account
Database ID: %s
Problem: No source model could be resolved from the context this \
wizard was launched from (active_model: %s)
Solution: Launch this wizard from a list/form view action so its \
context carries a valid active_model
""" % (
                self._description,
                self.id,
                active_model,
            )
            raise UserError(_(error_message))
        return model

    def _get_source_res_ids(self):
        self.ensure_one()
        active_ids = self.env.context.get("active_ids", [])
        if not active_ids:
            error_message = """
Document Type: %s
Context: Generate Virtual Account
Database ID: %s
Problem: No source record has been selected
Solution: Select at least one record before generating Virtual Account
""" % (
                self._description,
                self.id,
            )
            raise UserError(_(error_message))
        return active_ids

    def _check_type_id(self):
        self.ensure_one()
        source_model = self._get_source_model()
        restrict_model = self.type_id.model_id
        if restrict_model and restrict_model != source_model:
            error_message = """
Document Type: %s
Context: Generate Virtual Account
Database ID: %s
Problem: Generator type %s is restricted to model %s, but this wizard \
was launched from model %s
Solution: Select a generator type that is not restricted, or is \
restricted to %s
""" % (
                self._description,
                self.id,
                self.type_id.name,
                restrict_model.model,
                source_model.model,
                source_model.model,
            )
            raise UserError(_(error_message))

    def _prepare_va_generator_data(self):
        self.ensure_one()
        return {
            "type_id": self.type_id.id,
            "bank_id": self.bank_id.id,
            "biller_id": self.biller_id.id,
            "merchant_id": self.merchant_id.id,
            "usage_id": self.usage_id.id,
            "source_data_ids": [
                (0, 0, self._prepare_source_data_data(res_id))
                for res_id in self._get_source_res_ids()
            ],
        }

    def _prepare_source_data_data(self, res_id):
        self.ensure_one()
        return {
            "model_id": self._get_source_model().id,
            "res_id": res_id,
        }

    def _open_va_generator(self, generator):
        self.ensure_one()
        return {
            "name": _("Generate VA"),
            "type": "ir.actions.act_window",
            "res_model": "va_generator",
            "res_id": generator.id,
            "view_mode": "form",
            "target": "current",
        }
