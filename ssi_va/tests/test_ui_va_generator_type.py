# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiVAGeneratorType(HttpSavepointCase):
    """UI/UX tour tests for the ``va_generator_type`` work instructions.

    Every ``test_*`` method runs the tour paired with the IK file named
    in its docstring (``docs/va_generator_type/NN-*.md``). Pre-Condition
    data of those IK files is prepared here in Python -- never through UI
    steps -- so that each tour only walks the click-flow the IK
    documents.
    """

    @classmethod
    def setUpClass(cls):
        """Prepare the IK Pre-Conditions shared by the generator type tours.

        Covers the two Pre-Condition types the IK files declare:
        ``Access`` (admin is put in the Virtual Account Generator Type
        group) and ``Config`` (a ``sequence.template`` for
        ``va_generator_type``, without which the Generate Code button
        raises a ``UserError`` instead of assigning a code), plus the
        generator type records the edit, delete, deactivate and activate
        tours act on.
        """
        super().setUpClass()

        cls.user_admin = cls.env.ref("base.user_admin")
        cls.group_va_generator_type = cls.env.ref("ssi_va.va_generator_type_group")
        cls.group_va_generator_type.sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

        cls.code_sequence = cls.env["ir.sequence"].create(
            {
                "name": "TOUR VA Generator Type Code Sequence",
                "code": "ssi_va.tour.va_generator_type",
                "prefix": "TOURSEQVAGT",
                "padding": 4,
            }
        )
        cls.code_sequence_template = cls.env["sequence.template"].create(
            {
                "name": "TOUR VA Generator Type Sequence Template",
                "model_id": cls.env["ir.model"]._get_id("va_generator_type"),
                "sequence_field_id": cls.env["ir.model.fields"]
                ._get("va_generator_type", "code")
                .id,
                "date_field_id": cls.env["ir.model.fields"]
                ._get("va_generator_type", "create_date")
                .id,
                "sequence_selection_method": "use_sequence",
                "sequence_id": cls.code_sequence.id,
            }
        )

        cls.generator_type_edit = cls._create_generator_type("TOUR VA GENTYPE Edit")
        cls.generator_type_delete = cls._create_generator_type("TOUR VA GENTYPE Delete")
        cls.generator_type_deactivate = cls._create_generator_type(
            "TOUR VA GENTYPE Deactivate"
        )
        cls.generator_type_activate = cls._create_generator_type(
            "TOUR VA GENTYPE Activate",
            active=False,
        )

    @classmethod
    def _create_generator_type(cls, name, active=True):
        """Create a ``va_generator_type`` record used as tour Pre-Condition.

        ``code`` is left as ``"/"`` so several records can coexist
        (``mixin.master_data._check_duplicate_code`` skips ``"/"``) and
        so the Generate Code button of the edit tour actually assigns a
        value. ``python_code`` and ``partner_python_code`` are left to
        their model defaults, which is the state the IK describes.

        :param str name: Name of the generator type record.
        :param bool active: Whether the record starts active.
        :return: The created ``va_generator_type`` record.
        :rtype: :class:`odoo.models.Model`
        """
        return cls.env["va_generator_type"].create(
            {
                "name": name,
                "code": "/",
                "active": active,
            }
        )

    def test_create(self):
        """Run the create tour for ``va_generator_type``.

        The Python Code and Partner Resolution Python Code steps are
        walked as review-only: per the issue Design Decision the tour
        proves those tabs render but neither runs nor inspects the
        generator type Python code.

        IK: docs/va_generator_type/01-create.md
        """
        self.start_tour("/web", "ssi_va_va_generator_type_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``va_generator_type``.

        The two Python code steps are review-only, for the same reason
        as in :meth:`test_create`.

        IK: docs/va_generator_type/02-edit.md
        """
        self.start_tour("/web", "ssi_va_va_generator_type_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``va_generator_type``.

        IK: docs/va_generator_type/03-delete.md
        """
        self.start_tour("/web", "ssi_va_va_generator_type_delete", login="admin")

    def test_deactivate(self):
        """Run the deactivate tour for ``va_generator_type``.

        IK: docs/va_generator_type/04-deactivate.md
        """
        self.start_tour("/web", "ssi_va_va_generator_type_deactivate", login="admin")

    def test_activate(self):
        """Run the activate tour for ``va_generator_type``.

        IK: docs/va_generator_type/05-activate.md
        """
        self.start_tour("/web", "ssi_va_va_generator_type_activate", login="admin")
