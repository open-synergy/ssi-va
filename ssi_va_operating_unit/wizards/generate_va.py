# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class GenerateVa(models.TransientModel):
    """
    Extends the ``generate_va`` wizard with an ``operating_unit_id``
    field, whose value is passed through as-is to the ``va_generator``
    created by ``action_generate`` (including when left empty).
    """

    _name = "generate_va"
    _inherit = "generate_va"

    operating_unit_id = fields.Many2one(
        string="Operating Unit",
        comodel_name="operating.unit",
        required=False,
        default=lambda self: self.env["res.users"].operating_unit_default_get(),
        help="Operating unit to assign to the Virtual Account generator "
        "created by this wizard. Left empty, the created document is "
        "created without an operating unit.",
    )

    def _prepare_va_generator_data(self):
        """Add ``operating_unit_id`` to the ``va_generator`` values.

        Extends the base implementation. The wizard's
        ``operating_unit_id`` value is always passed through as-is —
        including when empty/``False`` — instead of letting
        ``va_generator``'s own mixin default recompute it.

        :return: dict of ``va_generator`` values
        """
        self.ensure_one()
        res = super()._prepare_va_generator_data()
        res["operating_unit_id"] = self.operating_unit_id.id
        return res
