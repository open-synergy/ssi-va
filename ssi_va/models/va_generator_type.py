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
    usage_id = fields.Many2one(
        string="Bank Account Usage",
        comodel_name="res_partner_bank_usage",
        required=False,
        ondelete="restrict",
        help="Usage/purpose copied to every res.partner.bank generated "
        "through this generator type. Optional - left empty, generated "
        "bank accounts are created with no usage set.",
    )
    partner_python_code = fields.Text(
        string="Partner Resolution Python Code",
        required=True,
        default="result = source_data.source_data_id",
        help="Python code executed via safe_eval to resolve the res.partner "
        "record Virtual Account numbers are generated for, out of the "
        "current source data line ('source_data', a va_generator."
        "source_data record). The code must assign the resulting record "
        "(exactly one res.partner) to the variable 'result'.",
    )

    def generate_partner(self, extra_localdict=None):
        """Execute ``partner_python_code`` and return the resolved partner.

        ``extra_localdict`` is merged into the evaluation context before
        executing ``partner_python_code``. It is the extension point
        ``va_generator`` uses to expose the current generator document and
        source data line (e.g. ``generator``, ``source_data``,
        ``source_record``, ``biller``, ``merchant``) to the code.
        """
        self.ensure_one()
        localdict = self._get_default_localdict()
        localdict.update(extra_localdict or {})
        try:
            safe_eval(
                self.partner_python_code,
                localdict,
                mode="exec",
                nocopy=True,
            )
            result = localdict["result"]
        except Exception as error:
            error_message = """
Document Type: %s
Context: Resolve source partner
Database ID: %s
Problem: Execution of partner_python_code failed with error: %s
Solution: Fix partner_python_code so it assigns a single res.partner \
record to the 'result' variable
""" % (
                self._description,
                self.id,
                error,
            )
            raise UserError(_(error_message))
        if (
            not isinstance(result, models.BaseModel)
            or result._name != "res.partner"
            or len(result) != 1
        ):
            error_message = """
Document Type: %s
Context: Resolve source partner
Database ID: %s
Problem: partner_python_code did not return a single res.partner record \
(got: %s)
Solution: Fix partner_python_code so it assigns exactly one res.partner \
record to the 'result' variable
""" % (
                self._description,
                self.id,
                result,
            )
            raise UserError(_(error_message))
        return result

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
