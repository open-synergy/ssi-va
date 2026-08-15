# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class IrModel(models.Model):
    """
    Extend ``ir.model`` with an action method (and its triggering
    button on the model form) that registers a Generate VA wizard
    binding (``ir.actions.act_window``) on the model, so any model can
    be turned into a Virtual Account source without hand-authoring the
    binding in XML. Pressing it repeatedly is allowed: each press
    creates a new, separately named binding rather than rejecting
    duplicates. No field is added to the model.
    """

    _name = "ir.model"
    _inherit = [
        "ir.model",
    ]

    def action_create_va_wizard(self):
        """Register a Generate VA wizard binding on the selected model(s).

        Delegates to ``_create_va_wizard`` for every record in
        ``self``, run with ``sudo()`` so the binding can be created
        regardless of the current user's rights on ``ir.model``.

        :return: nothing; creates an ``ir.actions.act_window`` per
            record
        """
        for record in self.sudo():
            record._create_va_wizard()

    def _create_va_wizard(self):
        """Create the Generate VA wizard binding for this model.

        Raises ``UserError`` (via ``_check_model``) when the model is
        transient.

        :return: nothing; creates an ``ir.actions.act_window`` record
        """
        self.ensure_one()
        self._check_model()
        self.env["ir.actions.act_window"].sudo().create(
            self._prepare_va_wizard_action_vals()
        )

    def _check_model(self):
        """Ensure the model can be a valid Virtual Account source.

        Raises ``UserError`` when the model is transient, since
        transient records do not survive past the transaction.
        """
        self.ensure_one()
        if self.transient:
            error_message = """
Document Type: %s
Context: Add Generate VA Wizard
Database ID: %s
Problem: Model %s is a transient model, so its records do not survive \
past the transaction and can never be a valid Virtual Account source
Solution: Select a non-transient model
""" % (
                self._description,
                self.id,
                self.model,
            )
            raise UserError(_(error_message))

    def _get_va_wizard_binding_criteria(self):
        """Build the domain matching this model's Generate VA bindings.

        Extension point: override to widen or narrow the criteria
        used to count existing bindings.

        :return: an Odoo search domain
        """
        self.ensure_one()
        return [
            ("res_model", "=", "generate_va"),
            ("binding_model_id", "=", self.id),
        ]

    def _get_va_wizard_binding_count(self):
        """Count the Generate VA wizard bindings already on this model.

        :return: number of matching ``ir.actions.act_window`` records
        """
        self.ensure_one()
        return (
            self.env["ir.actions.act_window"]
            .sudo()
            .search_count(self._get_va_wizard_binding_criteria())
        )

    def _prepare_va_wizard_action_vals(self):
        """Build the ``ir.actions.act_window`` values for a new binding.

        Names the binding ``Generate VA`` for the first one, and
        ``Generate VA #<n>`` for subsequent presses, so repeated
        presses create separately named bindings instead of being
        rejected as duplicates.

        :return: dict of ``ir.actions.act_window`` values
        """
        self.ensure_one()
        sequence = self._get_va_wizard_binding_count() + 1
        name = _("Generate VA") if sequence == 1 else _("Generate VA #%s") % sequence
        return {
            "name": name,
            "res_model": "generate_va",
            "view_mode": "form",
            "view_id": self.env.ref("ssi_va.generate_va_view_form").id,
            "target": "new",
            "binding_model_id": self.id,
            "binding_view_types": "list,form",
        }
