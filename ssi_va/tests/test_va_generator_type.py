# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestVAGeneratorType(YamlTransactionCase):
    def test_va_generator_type(self):
        self.run_yaml_scenario("test_data_va_generator_type.yaml")

    def test_generate_code_returns_result(self):
        """Python murni — pemicu P1 (L-01: action `call` membuang nilai balik
        method; YAML tidak bisa meng-assert nilai balik `generate_code()`).
        """
        generator_type = self.env["va_generator_type"].create(
            {
                "name": "Sequence Based",
                "code": "/",
                "python_code": 'result = "ABC123"',
            }
        )
        self.assertEqual(generator_type.generate_code(), "ABC123")

    def test_generate_code_uses_extra_localdict(self):
        """Python murni — pemicu P1 (L-01: action `call` membuang nilai balik
        method; YAML tidak bisa meng-assert nilai balik `generate_code()`).
        """
        generator_type = self.env["va_generator_type"].create(
            {
                "name": "Partner Based",
                "code": "/",
                "python_code": 'result = extra_var + "-XYZ"',
            }
        )
        result = generator_type.generate_code(extra_localdict={"extra_var": "PARTNER1"})
        self.assertEqual(result, "PARTNER1-XYZ")
