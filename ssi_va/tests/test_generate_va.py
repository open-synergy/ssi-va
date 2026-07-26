# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestGenerateVA(YamlTransactionCase):
    def test_generate_va(self):
        self.run_yaml_scenario("test_data_generate_va.yaml")

    def test_action_generate_returns_action(self):
        """Pure Python — trigger P1 (L-01: ``action: call`` discards the
        method's return value). ``action_generate()`` returns an
        ``ir.actions.act_window`` dict that YAML has no way to assert on.
        """
        generator_type = self.env["va_generator_type"].create(
            {
                "name": "Sequence Based",
                "code": "/",
                "python_code": 'result = "U1"',
            }
        )
        biller = self.env["va_biller"].create({"name": "Biller A", "code": "/"})
        bank = self.env["res.bank"].create({"name": "Bank A"})
        partner = self.env["res.partner"].create({"name": "Test Partner"})
        wizard = (
            self.env["generate_va"]
            .with_context(active_model="res.partner", active_ids=partner.ids)
            .create(
                {
                    "type_id": generator_type.id,
                    "bank_id": bank.id,
                    "biller_id": biller.id,
                }
            )
        )

        action = wizard.action_generate()

        generator = self.env["va_generator"].search([("biller_id", "=", biller.id)])
        self.assertEqual(len(generator), 1)
        self.assertEqual(action["res_model"], "va_generator")
        self.assertEqual(action["res_id"], generator.id)
        self.assertEqual(action["target"], "current")
