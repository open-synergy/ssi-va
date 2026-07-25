# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class VAGeneratorSourceData(models.Model):
    """
    Represents one source record (e.g. a partner) that a Virtual
    Account (VA) generator document (``va_generator``) generates VA
    numbers for. Populated through a dedicated wizard (implemented
    separately) or directly via ORM — not meant to be filled in
    manually by the user.
    """

    _name = "va_generator.source_data"
    _description = "Virtual Account Generator - Source Data"
    _order = "va_generator_id, id"

    va_generator_id = fields.Many2one(
        string="# VA Generator",
        comodel_name="va_generator",
        required=True,
        ondelete="cascade",
        help="VA generator document that this source data line belongs to.",
    )
    model_id = fields.Many2one(
        string="Source Model",
        comodel_name="ir.model",
        required=True,
        ondelete="cascade",
        help="Technical model of the source record that Virtual "
        "Account numbers are generated for.",
    )
    model_name = fields.Char(
        related="model_id.model",
        store=True,
        readonly=True,
        compute_sudo=True,
        help="Technical name of the source model, derived from Source "
        "Model. Used to resolve the source record.",
    )
    res_id = fields.Integer(
        string="Source Record ID",
        required=True,
        help="Database ID of the source record within Source Model.",
    )
    source_data_id = fields.Reference(
        string="Source Data",
        selection="_selection_target_model",
        compute="_compute_source_data_id",
        compute_sudo=True,
        store=False,
        help="Read-only reference to the source record, derived from "
        "Source Model and Source Record ID. Used for display/"
        "navigation purposes only.",
    )

    @api.model
    def _selection_target_model(self):
        return [(model.model, model.name) for model in self.env["ir.model"].search([])]

    @api.depends("model_name", "res_id")
    def _compute_source_data_id(self):
        for record in self:
            result = False
            if record.model_name and record.res_id:
                result = "%s,%s" % (record.model_name, record.res_id)
            record.source_data_id = result

    @api.constrains("va_generator_id", "model_id", "res_id")
    def _check_duplicate_source_data(self):
        for record in self.sudo():
            if not record._check_duplicate_source_data_condition():
                error_message = """
Context: Create/update Virtual Account generator source data
Database ID: %s
Problem: Source record %s (ID %s) is already added to this VA generator
Solution: Remove the duplicate source data line, or edit the existing \
one instead of adding a new one
""" % (
                    record.id,
                    record.model_id.name,
                    record.res_id,
                )
                raise ValidationError(error_message)

    def _check_duplicate_source_data_condition(self):
        self.ensure_one()
        if not self.va_generator_id or not self.model_id or not self.res_id:
            return True
        duplicate = self.search(
            [
                ("id", "!=", self.id),
                ("va_generator_id", "=", self.va_generator_id.id),
                ("model_id", "=", self.model_id.id),
                ("res_id", "=", self.res_id),
            ]
        )
        return not duplicate
