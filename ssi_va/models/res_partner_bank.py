# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartnerBank(models.Model):
    """
    Adds Virtual Account generator traceability to partner bank
    accounts. Links each bank account created by a ``va_generator``
    document back to the document that produced it, so the origin
    stays auditable.
    """

    _name = "res.partner.bank"
    _inherit = ["res.partner.bank"]

    va_generator_id = fields.Many2one(
        string="# VA Generator",
        comodel_name="va_generator",
        readonly=True,
        ondelete="set null",
        help="VA generator document that created this bank account, if "
        "any. Empty for bank accounts created manually or by other "
        "means.",
    )
