# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class VaBiller(models.Model):
    """
    Represents a biller entity that receives payment through Virtual
    Account (VA). A biller may hold a different VA code per bank,
    stored on the child model ``va_biller.code``. This master data is
    used as the reference for generating Virtual Account numbers.
    """

    _name = "va_biller"
    _inherit = ["mixin.master_data"]
    _description = "Virtual Account Biller"

    bank_code_ids = fields.One2many(
        string="Bank Codes",
        comodel_name="va_biller.code",
        inverse_name="va_biller_id",
        help="List of biller codes issued by each bank for this biller. "
        "Used as reference data when generating Virtual Account numbers.",
    )
