# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiVABiller(HttpSavepointCase):
    """UI/UX tour tests for the ``va_biller`` work instructions.

    Every ``test_*`` method runs the tour paired with the IK file named
    in its docstring (``docs/va_biller/NN-*.md``). Pre-Condition data of
    those IK files is prepared here in Python -- never through UI steps
    -- so that each tour only walks the click-flow the IK documents.
    """

    @classmethod
    def setUpClass(cls):
        """Prepare the IK Pre-Conditions shared by the va_biller tours.

        Covers the three Pre-Condition types the IK files declare:
        ``Access`` (admin is put in the Virtual Account Biller group),
        ``Config`` (a ``sequence.template`` for ``va_biller``, without
        which the Generate Code button raises a ``UserError`` instead of
        assigning a code) and ``Data`` (one ``res.bank`` to pick on the
        Bank Codes tab), plus the biller records the edit, delete,
        deactivate and activate tours act on.
        """
        super().setUpClass()

        cls.user_admin = cls.env.ref("base.user_admin")
        cls.group_va_biller = cls.env.ref("ssi_va.va_biller_group")
        cls.group_va_biller.sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR VA Biller Code Sequence",
                "code": "ssi_va.tour.va_biller",
                "prefix": "TOURSEQVAB",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR VA Biller Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("va_biller"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("va_biller", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("va_biller", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        cls.bank = cls.env["res.bank"].create(
            {
                "name": "TOUR VA BILLER BANK",
            }
        )

        cls.biller_edit = cls._create_biller("TOUR VA BILLER Edit")
        cls.biller_delete = cls._create_biller(
            "TOUR VA BILLER Delete",
            bank_code="TOURBCDELETE01",
        )
        cls.biller_deactivate = cls._create_biller("TOUR VA BILLER Deactivate")
        cls.biller_activate = cls._create_biller(
            "TOUR VA BILLER Activate",
            active=False,
        )

    @classmethod
    def _create_biller(cls, name, active=True, bank_code=False):
        """Create a ``va_biller`` record used as tour Pre-Condition.

        ``code`` is left as ``"/"`` so several records can coexist
        (``mixin.master_data._check_duplicate_code`` skips ``"/"``) and
        so the Generate Code button of the edit tour actually assigns a
        value.

        :param str name: Name of the biller record.
        :param bool active: Whether the record starts active.
        :param bank_code: Biller code of a single bank code line, or
            ``False`` to create the record without any line.
        :return: The created ``va_biller`` record.
        :rtype: :class:`odoo.models.Model`
        """
        values = {
            "name": name,
            "code": "/",
            "active": active,
        }
        if bank_code:
            values["bank_code_ids"] = [
                (
                    0,
                    0,
                    {
                        "bank_id": cls.bank.id,
                        "biller_code": bank_code,
                    },
                )
            ]
        return cls.env["va_biller"].create(values)

    def test_create(self):
        """Run the create tour for ``va_biller``.

        IK: docs/va_biller/01-create.md
        """
        self.start_tour("/web", "ssi_va_va_biller_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``va_biller``.

        IK: docs/va_biller/02-edit.md
        """
        self.start_tour("/web", "ssi_va_va_biller_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``va_biller``.

        IK: docs/va_biller/03-delete.md
        """
        self.start_tour("/web", "ssi_va_va_biller_delete", login="admin")

    def test_deactivate(self):
        """Run the deactivate tour for ``va_biller``.

        IK: docs/va_biller/04-deactivate.md
        """
        self.start_tour("/web", "ssi_va_va_biller_deactivate", login="admin")

    def test_activate(self):
        """Run the activate tour for ``va_biller``.

        The IK Flow ends with "Click OK to confirm", but 14.0 shows no
        confirmation dialog for Unarchive, so the tour has no step for
        it; see the comment in the tour file.

        IK: docs/va_biller/05-activate.md
        """
        self.start_tour("/web", "ssi_va_va_biller_activate", login="admin")
