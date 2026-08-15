# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestVABiller(YamlTransactionCase):
    """Cover CRUD and constraint scenarios for ``va_biller``."""

    def test_va_biller(self):
        """Run the master data and bank code YAML scenario."""
        self.run_yaml_scenario("test_data_va_biller.yaml")
