# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestVAGeneratorExporter(YamlTransactionCase):
    """Cover CRUD and file generation scenarios for ``va_generator_exporter``."""

    def test_va_generator_exporter(self):
        """Run the master data YAML scenario."""
        self.run_yaml_scenario("test_data_va_generator_exporter.yaml")

    def test_generate_file_xlsx_returns_valid_bytes(self):
        """Python murni — pemicu P1 (L-01: action `call` membuang nilai
        balik method; YAML tidak bisa meng-assert isi bytes yang
        dikembalikan `generate_file()`).
        """
        exporter = self.env["va_generator_exporter"].create(
            {
                "name": "Bank ABC VA Export",
                "code": "/",
                "format": "xlsx",
                "python_code": 'result = [["VA", "Name"], ["B1U1", "A"]]',
            }
        )
        content = exporter.generate_file()
        self.assertTrue(content)
        self.assertEqual(content[:2], b"PK")

    def test_generate_file_csv_matches_xlsx_row_content(self):
        """Python murni — pemicu P1 (L-01: action `call` membuang nilai
        balik method; YAML tidak bisa meng-assert isi bytes yang
        dikembalikan `generate_file()`).

        Memakai ``python_code`` yang **identik** dengan skenario XLSX di
        atas untuk membuktikan satu snippet menghasilkan baris yang setara
        lintas format (Kriteria Penerimaan).
        """
        exporter = self.env["va_generator_exporter"].create(
            {
                "name": "Bank ABC VA Export",
                "code": "/",
                "format": "csv",
                "csv_delimiter": ",",
                "python_code": 'result = [["VA", "Name"], ["B1U1", "A"]]',
            }
        )
        content = exporter.generate_file()
        self.assertEqual(content.decode("utf-8"), "VA,Name\r\nB1U1,A\r\n")

    def test_generate_file_csv_uses_custom_delimiter(self):
        """Python murni — pemicu P1 (L-01: action `call` membuang nilai
        balik method; YAML tidak bisa meng-assert isi bytes yang
        dikembalikan `generate_file()`).
        """
        exporter = self.env["va_generator_exporter"].create(
            {
                "name": "Bank ABC VA Export",
                "code": "/",
                "format": "csv",
                "csv_delimiter": ";",
                "python_code": 'result = [["VA", "Name"], ["B1U1", "A"]]',
            }
        )
        content = exporter.generate_file()
        self.assertEqual(content.decode("utf-8"), "VA;Name\r\nB1U1;A\r\n")

    def test_get_file_extension_matches_format(self):
        """Python murni — pemicu P1 (L-01: action `call` membuang nilai
        balik method; YAML tidak bisa meng-assert nilai balik
        `get_file_extension()`).
        """
        exporter = self.env["va_generator_exporter"].create(
            {
                "name": "Bank ABC VA Export",
                "code": "/",
                "format": "csv",
                "python_code": "result = []",
            }
        )
        self.assertEqual(exporter.get_file_extension(), "csv")
        exporter.write({"format": "xlsx"})
        self.assertEqual(exporter.get_file_extension(), "xlsx")
