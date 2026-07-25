# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class GenerateVA(models.TransientModel):
    """
    Wizard to generate a Virtual Account (VA) generator document
    (``va_generator``) for one or more partners, launched as an
    ``Action`` from the Contact list/form view. Populates the resulting
    document's ``source_data_ids`` with one line per selected partner
    and leaves it in the ``draft`` state for manual review/confirmation.
    """

    _name = "generate_va"
    _description = "Generate Virtual Account"

    partner_ids = fields.Many2many(
        string="Partners",
        comodel_name="res.partner",
        relation="generate_va_res_partner_rel",
        column1="wizard_id",
        column2="partner_id",
        required=True,
        default=lambda self: self._default_partner_ids(),
        help="Partners to generate Virtual Account numbers for. One "
        "source data line is created on the resulting document for "
        "each partner selected here. Defaults to the Contact records "
        "selected in the list view this wizard was launched from.",
    )
    type_id = fields.Many2one(
        string="Generator Type",
        comodel_name="va_generator_type",
        required=True,
        domain=[
            "|",
            ("model_id", "=", False),
            ("model_id.model", "=", "res.partner"),
        ],
        help="Generator type whose python_code computes the unique VA "
        "code. Only generator types not restricted to a model, or "
        "restricted to Contact, are offered.",
    )
    biller_id = fields.Many2one(
        string="Biller",
        comodel_name="va_biller",
        required=True,
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

    @api.model
    def _default_partner_ids(self):
        active_ids = self.env.context.get("active_ids", [])
        return self.env["res.partner"].browse(active_ids)

    def action_generate(self):
        for record in self.sudo():
            result = record._generate()
        return result

    def _generate(self):
        self.ensure_one()
        self._check_partner_ids()
        generator = self.env["va_generator"].create(self._prepare_va_generator_data())
        return self._open_va_generator(generator)

    def _check_partner_ids(self):
        self.ensure_one()
        if not self.partner_ids:
            error_message = """
Document Type: %s
Context: Generate Virtual Account
Database ID: %s
Problem: No partner has been selected
Solution: Select at least one partner before generating Virtual Account
""" % (
                self._description,
                self.id,
            )
            raise UserError(_(error_message))

    def _prepare_va_generator_data(self):
        self.ensure_one()
        return {
            "type_id": self.type_id.id,
            "biller_id": self.biller_id.id,
            "merchant_id": self.merchant_id.id,
            "source_data_ids": [
                (0, 0, self._prepare_source_data_data(partner))
                for partner in self.partner_ids
            ],
        }

    def _prepare_source_data_data(self, partner):
        self.ensure_one()
        return {
            "model_id": self.env.ref("base.model_res_partner").id,
            "res_id": partner.id,
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
