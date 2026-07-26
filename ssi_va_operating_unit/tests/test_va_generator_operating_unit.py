# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestVAGeneratorOperatingUnit(YamlTransactionCase):
    def test_va_generator_operating_unit(self):
        """Run the va_generator/generate_va Operating Unit scenarios."""
        self.run_yaml_scenario("test_data_va_generator_operating_unit.yaml")
