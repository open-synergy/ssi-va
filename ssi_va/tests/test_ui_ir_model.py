# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiIrModel(HttpSavepointCase):
    """UI/UX tour tests for the ``ir.model`` work instructions.

    Every ``test_*`` method runs the tour paired with the IK file named
    in its docstring (``docs/ir_model/NN-*.md``). Pre-Condition data of
    those IK files is prepared here in Python -- never through UI steps
    -- so that each tour only walks the click-flow the IK documents.
    """

    #: The Settings app exposes five menu sections; the default 1366px
    #: viewport pushes the last ones into the overflow dropdown, where
    #: the Technical menu would fail the implicit ``:visible`` check of
    #: every tour trigger.
    browser_size = "1920x1080"

    @classmethod
    def setUpClass(cls):
        """Prepare the IK Pre-Conditions of the ir.model tours.

        Covers the two Pre-Condition types the IK file declares:
        ``Access`` (admin is put in ``base.group_system``, the group
        gating the Add Generate VA Wizard button) and ``Record`` (the
        model acted on is a non-transient one).

        ``va_generator_exporter`` is the model turned into a Virtual
        Account source. It is non-transient, its technical name is a
        unique substring among the installed models -- so the search of
        Flow 2 leaves exactly one row -- and it owns a menu of its own,
        which is where the Action menu of the Post-Condition is read
        from. Admin is granted the exporter group so that menu is
        rendered, and one exporter record is created because 14.0 only
        renders the Action menu of a list view once a row is selected.
        """
        super().setUpClass()

        cls.user_admin = cls.env.ref("base.user_admin")
        cls.group_system = cls.env.ref("base.group_system")
        cls.group_va_generator_exporter = cls.env.ref(
            "ssi_va.va_generator_exporter_group"
        )
        (cls.group_system + cls.group_va_generator_exporter).sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

        cls.target_model = cls.env["ir.model"]._get("va_generator_exporter")
        cls.target_record = cls.env["va_generator_exporter"].create(
            {
                "name": "TOUR IRMODEL VA SOURCE",
                "code": "/",
            }
        )

    def test_add_generate_va_wizard(self):
        """Run the Add Generate VA Wizard tour for ``ir.model``.

        The tour starts on ``/web?debug=1`` because the Technical menu
        of Flow 1 is gated by ``base.group_no_one``, which
        ``ir.ui.menu._visible_menu_ids()`` withholds while the session
        is not in developer mode.

        Two parts of the IK are deliberately not walked. The UserError
        branch of Flow 3 is a negative path, which the issue Test
        Scenario assigns to the unit tests. The numbering of the
        binding created by the repeated press of Flow 4 is not read
        either: per the issue Design Decision the tour stops at a new
        entry showing up in the Action menu and never counts or names
        the ``ir.actions.act_window`` records behind it.

        IK: docs/ir_model/04-add-generate-va-wizard.md
        """
        self.start_tour(
            "/web?debug=1",
            "ssi_va_ir_model_add_generate_va_wizard",
            login="admin",
        )
