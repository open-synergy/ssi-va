# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestVAGenerator(YamlTransactionCase):
    def test_va_generator(self):
        self.run_yaml_scenario("test_data_va_generator.yaml")

    def test_export_file_name_pattern(self):
        """Python murni - pemicu P4 (L-08: regex atas string tidak bisa
        diassert di YAML).

        Membuktikan bahwa "/" pada name dokumen diganti "-" dan bahwa
        timestamp berformat YYYYmmdd_HHMMSS benar-benar dipakai pada nama
        attachment hasil action_generate_export_file.
        """
        model_res_partner = self.env.ref("base.model_res_partner")
        partner = self.env["res.partner"].create({"name": "Test Partner Regex"})
        exporter = self.env["va_generator_exporter"].create(
            {
                "name": "CSV Exporter",
                "code": "/",
                "format": "csv",
                "python_code": 'result = [["VA"]]',
            }
        )
        generator_type = self.env["va_generator_type"].create(
            {
                "name": "Sequence Based",
                "code": "/",
                "python_code": 'result = "U9"',
            }
        )
        biller = self.env["va_biller"].create(
            {
                "name": "Biller Regex",
                "code": "/",
            }
        )
        generator = self.env["va_generator"].create(
            {
                "type_id": generator_type.id,
                "biller_id": biller.id,
                "exporter_id": exporter.id,
            }
        )
        self.env["va_generator.source_data"].create(
            {
                "va_generator_id": generator.id,
                "model_id": model_res_partner.id,
                "res_id": partner.id,
            }
        )
        generator.action_confirm()
        generator.action_approve_approval()
        self.assertEqual(generator.state, "done")

        generator.action_generate_export_file()

        attachment = self.env["ir.attachment"].search(
            [
                ("res_model", "=", "va_generator"),
                ("res_id", "=", generator.id),
            ]
        )
        self.assertEqual(len(attachment), 1)
        self.assertRegex(
            attachment.name,
            r"^VAG-\d{4}-\d{6}-\d{8}_\d{6}\.csv$",
        )
