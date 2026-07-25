# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class VABillerMerchantCode(models.Model):
    """
    Represents the merchant code registered for a specific biller-bank
    combination (``va_biller.code``). A merchant can have at most one
    merchant code per biller-bank combination. The bank is automatically
    derived from the selected biller-bank code line.
    """

    _name = "va_biller_merchant.code"
    _description = "Virtual Account Biller Merchant - Code"
    _order = "va_biller_merchant_id, sequence"

    va_biller_merchant_id = fields.Many2one(
        string="# Merchant",
        comodel_name="va_biller_merchant",
        required=True,
        ondelete="cascade",
        help="Merchant that owns this biller-bank-specific merchant code.",
    )
    biller_id = fields.Many2one(
        string="Biller Bank Code",
        comodel_name="va_biller.code",
        required=True,
        help="Biller-bank code line that this merchant code is registered "
        "for. The bank is automatically derived from this selection.",
    )
    bank_id = fields.Many2one(
        string="Bank",
        comodel_name="res.bank",
        related="biller_id.bank_id",
        store=True,
        readonly=True,
        help="Bank associated with the selected biller-bank code. "
        "Automatically follows the bank of the selected biller bank code.",
    )
    merchant_code = fields.Char(
        string="Merchant Code",
        required=True,
        help="Merchant code registered for the selected biller-bank "
        "combination, used when generating Virtual Account numbers for "
        "this merchant.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Determines the display order of biller codes within a "
        "merchant.",
    )

    @api.constrains("va_biller_merchant_id", "biller_id")
    def _check_duplicate_biller_id(self):
        for record in self.sudo():
            if not record._check_duplicate_biller_id_condition():
                error_message = """
Context: Create/update Virtual Account merchant biller code
Database ID: %s
Problem: Biller bank code %s is already used by another biller code of \
merchant %s
Solution: Choose a different biller bank code, or edit the existing \
biller code instead of adding a duplicate one
""" % (
                    record.id,
                    record.biller_id.display_name,
                    record.va_biller_merchant_id.name,
                )
                raise ValidationError(error_message)

    def _check_duplicate_biller_id_condition(self):
        self.ensure_one()
        if not self.va_biller_merchant_id or not self.biller_id:
            return True
        duplicate = self.search(
            [
                ("id", "!=", self.id),
                ("va_biller_merchant_id", "=", self.va_biller_merchant_id.id),
                ("biller_id", "=", self.biller_id.id),
            ]
        )
        return not duplicate
