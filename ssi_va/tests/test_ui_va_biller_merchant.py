# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiVABillerMerchant(HttpSavepointCase):
    """UI/UX tour tests for the ``va_biller_merchant`` work instructions.

    Every ``test_*`` method runs the tour paired with the IK file named
    in its docstring (``docs/va_biller_merchant/NN-*.md``). Pre-Condition
    data of those IK files is prepared here in Python -- never through UI
    steps -- so that each tour only walks the click-flow the IK
    documents.
    """

    @classmethod
    def setUpClass(cls):
        """Prepare the IK Pre-Conditions of the merchant tours.

        Covers the three Pre-Condition types the IK files declare:
        ``Access`` (admin is put in the Virtual Account Biller Merchant
        group), ``Config`` (a ``sequence.template`` for
        ``va_biller_merchant``, without which the Generate Code button
        raises a ``UserError`` instead of assigning a code) and ``Data``
        (one ``va_biller`` carrying a bank code line, so that the Biller
        Bank Code field of the Biller Codes tab has an option to pick),
        plus the merchant records the edit, delete, deactivate and
        activate tours act on.
        """
        super().setUpClass()

        cls.user_admin = cls.env.ref("base.user_admin")
        cls.group_va_biller_merchant = cls.env.ref("ssi_va.va_biller_merchant_group")
        cls.group_va_biller_merchant.sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR VA Biller Merchant Code Sequence",
                "code": "ssi_va.tour.va_biller_merchant",
                "prefix": "TOURSEQVAM",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR VA Biller Merchant Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("va_biller_merchant"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("va_biller_merchant", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("va_biller_merchant", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        cls.bank = cls.env["res.bank"].create(
            {
                "name": "TOUR VA MERCHANT BANK",
            }
        )
        # The Biller Bank Code field of the Biller Codes tab points to a
        # va_biller.code line, whose name_get renders it as
        # "Biller - Bank (Code)". The tours pick it from the dropdown by
        # that rendered text.
        cls.biller = cls.env["va_biller"].create(
            {
                "name": "TOUR VA MERCHANT BILLER",
                "code": "/",
                "bank_code_ids": [
                    (
                        0,
                        0,
                        {
                            "bank_id": cls.bank.id,
                            "biller_code": "TOURVAMBC01",
                        },
                    )
                ],
            }
        )
        cls.biller_code = cls.biller.bank_code_ids[0]

        cls.merchant_edit = cls._create_merchant("TOUR VA MERCHANT Edit")
        cls.merchant_delete = cls._create_merchant(
            "TOUR VA MERCHANT Delete",
            merchant_code="TOURMCDELETE01",
        )
        cls.merchant_deactivate = cls._create_merchant("TOUR VA MERCHANT Deactivate")
        cls.merchant_activate = cls._create_merchant(
            "TOUR VA MERCHANT Activate",
            active=False,
        )

    @classmethod
    def _create_merchant(cls, name, active=True, merchant_code=False):
        """Create a ``va_biller_merchant`` record as tour Pre-Condition.

        ``code`` is left as ``"/"`` so several records can coexist
        (``mixin.master_data._check_duplicate_code`` skips ``"/"``) and
        so the Generate Code button of the edit tour actually assigns a
        value.

        :param str name: Name of the biller merchant record.
        :param bool active: Whether the record starts active.
        :param merchant_code: Merchant code of a single biller code
            line, or ``False`` to create the record without any line.
        :return: The created ``va_biller_merchant`` record.
        :rtype: :class:`odoo.models.Model`
        """
        values = {
            "name": name,
            "code": "/",
            "active": active,
        }
        if merchant_code:
            values["biller_code_ids"] = [
                (
                    0,
                    0,
                    {
                        "biller_id": cls.biller_code.id,
                        "merchant_code": merchant_code,
                    },
                )
            ]
        return cls.env["va_biller_merchant"].create(values)

    def test_create(self):
        """Run the create tour for ``va_biller_merchant``.

        IK: docs/va_biller_merchant/01-create.md
        """
        self.start_tour("/web", "ssi_va_va_biller_merchant_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``va_biller_merchant``.

        IK: docs/va_biller_merchant/02-edit.md
        """
        self.start_tour("/web", "ssi_va_va_biller_merchant_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``va_biller_merchant``.

        IK: docs/va_biller_merchant/03-delete.md
        """
        self.start_tour("/web", "ssi_va_va_biller_merchant_delete", login="admin")

    def test_deactivate(self):
        """Run the deactivate tour for ``va_biller_merchant``.

        IK: docs/va_biller_merchant/04-deactivate.md
        """
        self.start_tour("/web", "ssi_va_va_biller_merchant_deactivate", login="admin")

    def test_activate(self):
        """Run the activate tour for ``va_biller_merchant``.

        IK: docs/va_biller_merchant/05-activate.md
        """
        self.start_tour("/web", "ssi_va_va_biller_merchant_activate", login="admin")
