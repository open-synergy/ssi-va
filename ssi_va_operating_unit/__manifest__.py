# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Virtual Account + Operating Unit Integration",
    "version": "14.0.1.2.2",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "category": "Accounting",
    "depends": [
        "web_tour",
        "ssi_va",
        "ssi_operating_unit_mixin",
    ],
    "data": [
        "security/res_group/va_generator.xml",
        "security/ir_rule/va_generator.xml",
        "views/assets.xml",
        "views/va_generator.xml",
        "views/generate_va.xml",
    ],
    "demo": [],
}
