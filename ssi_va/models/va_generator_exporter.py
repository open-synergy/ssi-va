# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import csv
import io

import xlsxwriter

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class VaGeneratorExporter(models.Model):
    """
    Represents a Virtual Account (VA) export layout for a specific bank or
    provider file format. The layout is written as configurable Python code
    (``python_code``) that fills a uniform ``result`` variable (a list of
    list/tuple rows), so the exact same snippet can be reused across
    serializations. Field ``format`` selects the serialization performed by
    ``generate_file`` — ``xlsx`` (via ``xlsxwriter``) or ``csv`` (delimiter
    configurable via ``csv_delimiter``). This master data is used as the
    reference for the VA export feature (implemented separately).
    """

    _name = "va_generator_exporter"
    _inherit = ["mixin.master_data", "mixin.localdict"]
    _description = "Virtual Account Generator Exporter"

    format = fields.Selection(
        string="Format",
        selection=[
            ("xlsx", "XLSX"),
            ("csv", "CSV"),
        ],
        required=True,
        default="xlsx",
        help="File format produced by generate_file(). This only "
        "determines how the rows computed by python_code are serialized "
        "- it does not affect python_code itself.",
    )
    csv_delimiter = fields.Char(
        string="CSV Delimiter",
        default=",",
        help="Column delimiter used when format is CSV. Ignored when "
        "format is XLSX.",
    )
    python_code = fields.Text(
        string="Python Code",
        required=True,
        default="result = []",
        help="Python code executed via safe_eval to compute the rows to "
        "export. The code must assign the resulting data to the variable "
        "'result' as a list where each item is a list or tuple "
        "representing one row (the first row is usually the header, but "
        "that is up to the snippet).",
    )

    def get_file_extension(self):
        """Return the file extension matching ``format`` (``xlsx``/``csv``)."""
        self.ensure_one()
        return self.format

    def generate_file(self, extra_localdict=None):
        """Execute ``python_code`` and return the export file as bytes.

        ``extra_localdict`` is merged into the evaluation context before
        executing ``python_code``. It is the extension point future VA
        export features use to pass domain variables (e.g.
        ``bank_account_ids``/``biller``/``generator``); this method itself
        does not add any of them automatically.

        ``python_code`` must assign a list of list/tuple rows to the
        ``result`` variable. The same rows are serialized to XLSX or CSV
        depending on ``format``, and returned as ``bytes`` either way, so
        the caller does not need to know the format.
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
Context: Generate export file
Database ID: %s
Problem: Execution of python_code failed with error: %s
Solution: Fix python_code so it assigns a list of list/tuple rows to the 'result' variable
""" % (
                self._description,
                self.id,
                error,
            )
            raise UserError(_(error_message))

        if not isinstance(result, list) or not all(
            isinstance(row, (list, tuple)) for row in result
        ):
            error_message = """
Document Type: %s
Context: Generate export file
Database ID: %s
Problem: python_code assigned a value to 'result' that is not a list of list/tuple rows
Solution: Fix python_code so 'result' is a list where each item is a list or tuple
""" % (
                self._description,
                self.id,
            )
            raise UserError(_(error_message))

        if self.format == "csv":
            return self._generate_csv_file(result)
        return self._generate_xlsx_file(result)

    def _generate_xlsx_file(self, result):
        """Serialize export rows to an in-memory XLSX file.

        :param result: list of list/tuple rows computed by
            ``python_code``
        :return: XLSX file content as ``bytes``
        """
        self.ensure_one()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        try:
            worksheet = workbook.add_worksheet(self.name[:31])
            for row_index, row in enumerate(result):
                for col_index, value in enumerate(row):
                    worksheet.write(row_index, col_index, value)
        finally:
            workbook.close()
        return output.getvalue()

    def _generate_csv_file(self, result):
        """Serialize export rows to a CSV file.

        Uses ``csv_delimiter`` (defaulting to ``,``) as the column
        delimiter.

        :param result: list of list/tuple rows computed by
            ``python_code``
        :return: CSV file content encoded as ``bytes`` (UTF-8)
        """
        self.ensure_one()
        output = io.StringIO()
        writer = csv.writer(
            output,
            delimiter=self.csv_delimiter or ",",
            quoting=csv.QUOTE_MINIMAL,
            lineterminator="\r\n",
        )
        writer.writerows(result)
        return output.getvalue().encode("utf-8")
