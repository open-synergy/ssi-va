# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiVAGeneratorExporter(HttpSavepointCase):
    """UI/UX tour tests for the ``va_generator_exporter`` work instructions.

    Every ``test_*`` method runs the tour paired with the IK file named
    in its docstring (``docs/va_generator_exporter/NN-*.md``).
    Pre-Condition data of those IK files is prepared here in Python --
    never through UI steps -- so that each tour only walks the
    click-flow the IK documents.
    """

    @classmethod
    def setUpClass(cls):
        """Prepare the IK Pre-Conditions shared by the exporter tours.

        Covers the two Pre-Condition types the IK files declare:
        ``Access`` (admin is put in the Virtual Account Generator
        Exporter group) and ``Config`` (a ``sequence.template`` for
        ``va_generator_exporter``, without which the Generate Code
        button raises a ``UserError`` instead of assigning a code), plus
        the exporter records the edit, delete, deactivate and activate
        tours act on.

        The sequence prefix ``TOURSEQVAGE`` is load-bearing: the edit
        tour uses it as the synchronisation gate proving that the save
        and reload triggered by Generate Code landed before the Export
        Configuration fields are touched.
        """
        super().setUpClass()

        cls.user_admin = cls.env.ref("base.user_admin")
        cls.group_va_generator_exporter = cls.env.ref(
            "ssi_va.va_generator_exporter_group"
        )
        cls.group_va_generator_exporter.sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR VA Generator Exporter Code Sequence",
                "code": "ssi_va.tour.va_generator_exporter",
                "prefix": "TOURSEQVAGE",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR VA Generator Exporter Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("va_generator_exporter"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("va_generator_exporter", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("va_generator_exporter", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        cls.exporter_edit = cls._create_exporter("TOUR VA EXPORTER Edit")
        cls.exporter_delete = cls._create_exporter("TOUR VA EXPORTER Delete")
        cls.exporter_deactivate = cls._create_exporter("TOUR VA EXPORTER Deactivate")
        cls.exporter_activate = cls._create_exporter(
            "TOUR VA EXPORTER Activate",
            active=False,
        )

    @classmethod
    def _create_exporter(cls, name, active=True):
        """Create a ``va_generator_exporter`` record used as tour setup.

        ``code`` is left as ``"/"`` so several records can coexist
        (``mixin.master_data._check_duplicate_code`` skips ``"/"``) and
        so the Generate Code button of the edit tour actually assigns a
        value. ``format`` and ``python_code`` are left to their model
        defaults (``xlsx`` and ``result = []``), which is the state the
        IK describes before the export layout is configured.

        :param str name: Name of the exporter record.
        :param bool active: Whether the record starts active.
        :return: The created ``va_generator_exporter`` record.
        :rtype: :class:`odoo.models.Model`
        """
        return cls.env["va_generator_exporter"].create(
            {
                "name": name,
                "code": "/",
                "active": active,
            }
        )

    def test_create(self):
        """Run the create tour for ``va_generator_exporter``.

        The Format step picks CSV because the IK describes CSV
        Delimiter as reachable only in that branch. The Python Code step
        is walked as review-only: per the issue Design Decision the tour
        proves the tab renders but neither runs nor inspects the
        exporter Python code, whose ``ace`` widget keeps its value
        outside the DOM.

        IK: docs/va_generator_exporter/01-create.md
        """
        self.start_tour("/web", "ssi_va_va_generator_exporter_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``va_generator_exporter``.

        The Python Code step is review-only, for the same reason as in
        :meth:`test_create`.

        IK: docs/va_generator_exporter/02-edit.md
        """
        self.start_tour("/web", "ssi_va_va_generator_exporter_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``va_generator_exporter``.

        IK: docs/va_generator_exporter/03-delete.md
        """
        self.start_tour("/web", "ssi_va_va_generator_exporter_delete", login="admin")

    def test_deactivate(self):
        """Run the deactivate tour for ``va_generator_exporter``.

        IK: docs/va_generator_exporter/04-deactivate.md
        """
        self.start_tour(
            "/web", "ssi_va_va_generator_exporter_deactivate", login="admin"
        )

    def test_activate(self):
        """Run the activate tour for ``va_generator_exporter``.

        The IK Flow ends with "Click OK to confirm", but 14.0 shows no
        confirmation dialog for Unarchive, so the tour has no step for
        it; see the comment in the tour file.

        IK: docs/va_generator_exporter/05-activate.md
        """
        self.start_tour("/web", "ssi_va_va_generator_exporter_activate", login="admin")
