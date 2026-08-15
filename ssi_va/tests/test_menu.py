# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestMenu(YamlTransactionCase):
    """Cover the module's menu structure and placement."""

    def test_menu_placement(self):
        """Run the menu placement YAML scenario."""
        self.run_yaml_scenario("test_data_menu.yaml")
