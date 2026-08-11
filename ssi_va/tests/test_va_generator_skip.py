# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestVAGeneratorSkip(YamlTransactionCase):
    """Cover skipping bank account creation for colliding VA numbers.

    Kept in its own file/transaction (separate from
    ``test_va_generator.py``) because these scenarios pre-create
    ``res.partner.bank`` fixtures that would collide with the
    ``acc_number`` values used by scenarios in
    ``test_data_va_generator.yaml`` if they shared one transaction.
    """

    def test_va_generator_skip(self):
        """Run the source data skip evaluation scenario file."""
        self.run_yaml_scenario("test_data_va_generator_skip.yaml")
