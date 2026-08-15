# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class VaBillerCode(models.Model):
    """
    Represents the Virtual Account code issued by a specific bank for a
    biller (``va_biller``). A biller can have at most one code per bank.
    This model is referenced through Many2one from other models (e.g.
    ``va_biller_merchant.code``), so its display name is customized to
    be informative when selected from a dropdown.
    """

    _name = "va_biller.code"
    _description = "Virtual Account Biller - Bank Code"
    _order = "va_biller_id, sequence"

    va_biller_id = fields.Many2one(
        string="# Biller",
        comodel_name="va_biller",
        required=True,
        ondelete="cascade",
        help="Biller that owns this bank-specific Virtual Account code.",
    )
    bank_id = fields.Many2one(
        string="Bank",
        comodel_name="res.bank",
        required=True,
        help="Bank that issued the biller code for this Virtual Account.",
    )
    biller_code = fields.Char(
        string="Biller Code",
        required=True,
        help="Biller code issued by the bank, used when generating "
        "Virtual Account numbers for this bank.",
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Determines the display order of bank codes within a biller.",
    )

    @api.constrains("va_biller_id", "bank_id")
    def _check_duplicate_bank_id(self):
        """Ensure a biller has at most one code per bank.

        Raises ``ValidationError`` when another ``va_biller.code``
        record already exists for the same ``va_biller_id`` and
        ``bank_id`` combination.
        """
        for record in self.sudo():
            if not record._check_duplicate_bank_id_condition():
                error_message = """
Context: Create/update Virtual Account biller bank code
Database ID: %s
Problem: Bank %s is already used by another bank code of biller %s
Solution: Choose a different bank, or edit the existing bank code instead
of adding a duplicate one
""" % (
                    record.id,
                    record.bank_id.name,
                    record.va_biller_id.name,
                )
                raise ValidationError(error_message)

    def _check_duplicate_bank_id_condition(self):
        """Return whether this record's bank is still unique for its biller.

        :return: ``True`` when no other ``va_biller.code`` shares the
            same ``va_biller_id``/``bank_id`` pair, ``False`` otherwise
        """
        self.ensure_one()
        if not self.va_biller_id or not self.bank_id:
            return True
        duplicate = self.search(
            [
                ("id", "!=", self.id),
                ("va_biller_id", "=", self.va_biller_id.id),
                ("bank_id", "=", self.bank_id.id),
            ]
        )
        return not duplicate

    def name_get(self):
        """Build a display name combining biller, bank and code.

        Overridden so this model reads informatively when selected
        from a Many2one dropdown (e.g. ``va_biller_merchant.code``).

        :return: list of ``(id, name)`` tuples
        """
        result = []
        for record in self:
            name = "%s - %s (%s)" % (
                record.va_biller_id.name,
                record.bank_id.name,
                record.biller_code,
            )
            result.append((record.id, name))
        return result
