# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class VAGeneratorType(models.Model):
    """
    Represents a Virtual Account (VA) code generation strategy. The
    strategy is written as configurable Python code (``python_code``)
    that is executed through ``generate_code`` to produce the unique VA
    code. This master data is used as the reference for the VA generation
    feature (implemented separately).
    """

    _name = "va_generator_type"
    _inherit = ["mixin.master_data", "mixin.localdict"]
    _description = "Virtual Account Generator Type"

    python_code = fields.Text(
        string="Python Code",
        required=True,
        default='result = ""',
        help="Python code executed via safe_eval to compute the unique VA "
        "code. The code must assign the resulting code (a string) to the "
        "variable 'result'.",
    )
    model_id = fields.Many2one(
        string="Restrict to Model",
        comodel_name="ir.model",
        required=False,
        help="Model this generator type is restricted to. When set, this "
        "generator type is only selectable from the VA generation wizard "
        "when run from this model. Left empty, it is available for all "
        "models.",
    )

    def generate_code(self, extra_localdict=None):
        """Execute ``python_code`` and return the generated VA code.

        ``extra_localdict`` is merged into the evaluation context before
        executing ``python_code``. It is the extension point future VA
        generation features use to pass domain variables (e.g. partner,
        bank, biller); this method itself does not add any of them
        automatically.
        """
        self.ensure_one()
        localdict = self._get_default_localdict()
        localdict.update(extra_localdict or {})
        try:
            safe_eval(
                self.python_code,
                localdict,
                mode="exec",
                nocopy=True,
            )
            result = localdict["result"]
        except Exception as error:
            error_message = """
Document Type: %s
Context: Generate VA code
Database ID: %s
Problem: Execution of python_code failed with error: %s
Solution: Fix python_code so it assigns a valid string to the 'result' variable
""" % (
                self._description,
                self.id,
                error,
            )
            raise UserError(_(error_message))
        return result
