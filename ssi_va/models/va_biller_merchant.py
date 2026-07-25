# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VABillerMerchant(models.Model):
    """
    Represents a merchant (sub-entity of a biller-bank combination, e.g. a
    branch/outlet) that has its own merchant code registered for that
    specific biller-bank combination, stored on the child model
    ``va_biller_merchant.code``. This master data is used as the reference
    data for generating Virtual Account numbers.
    """

    _name = "va_biller_merchant"
    _inherit = ["mixin.master_data"]
    _description = "Virtual Account Biller Merchant"

    biller_code_ids = fields.One2many(
        string="Biller Codes",
        comodel_name="va_biller_merchant.code",
        inverse_name="va_biller_merchant_id",
        help="List of merchant codes registered for each biller-bank "
        "combination. Used as reference data when generating Virtual "
        "Account numbers.",
    )
