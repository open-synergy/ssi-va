# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class VAGenerator(models.Model):
    """
    Extends ``va_generator`` with a single Operating Unit (OU) per
    document, via ``mixin.single_operating_unit``. The ``operating_unit_id``
    field itself comes from the mixin — this module only wires the
    inheritance, security, and view.
    """

    _name = "va_generator"
    _inherit = [
        "va_generator",
        "mixin.single_operating_unit",
    ]
