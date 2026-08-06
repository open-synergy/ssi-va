# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiVAGeneratorOperatingUnit(HttpSavepointCase):
    """UI/UX tour tests for the ``va_generator`` delta work instructions.

    ``ssi_va_operating_unit`` is an extension module, so its IK files are
    delta IK files: they carry no Flow of their own, only an "Additional
    Fields" section on top of the Flow written in ``ssi_va``. The tour run
    here is delta-only accordingly -- it borrows the navigation of the
    base Flow and asserts only that the **Operating Unit** field is
    rendered in the **Generate VA** wizard.

    Pre-Condition data is prepared in Python -- never through UI steps --
    so that the tour walks the delta and nothing else.
    """

    #: The Contacts list and its search view are laid out for a wide
    #: viewport; the default 1366px one pushes part of the control panel
    #: into overflow, where a tour trigger would fail the implicit
    #: ``:visible`` check.
    browser_size = "1920x1080"

    @classmethod
    def setUpClass(cls):
        """Prepare the IK Pre-Conditions of the delta va_generator tour.

        Covers both Pre-Condition types the delta IK declares, plus what
        the base Flow it borrows needs to reach the wizard:

        * ``Module`` -- satisfied by the module being installed, which is
          what makes this test run at all.
        * ``Access`` -- the tour user is put in
          ``operating_unit.group_multi_operating_unit``, without which the
          **Operating Unit** field is not rendered at all and the tour
          would fail for the wrong reason. ``base.user_admin`` already
          holds it through ``group_manager_operating_unit``; it is written
          explicitly here so the Pre-Condition does not depend on that
          implication staying in place.
        * ``Access`` of the base Flow -- the same user is put in
          ``Virtual Account Generator / User``, the group the base IK
          names as actor and the only group granted access to the
          ``generate_va`` wizard model.
        * ``Data`` of the base Flow -- one ``res.partner`` to select in
          the Contacts list before opening the wizard.

        The ``Config`` Pre-Condition of the base Flow needs no setup: the
        **Generate VA** entry of the Action menu is bound to
        ``res.partner`` by ``ssi_va`` itself (``wizards/generate_va.xml``).
        The generator type and biller records that base Flow 4 would need
        are not created either -- this tour stops before that step, see
        :meth:`test_create`.
        """
        super().setUpClass()

        cls.user_admin = cls.env.ref("base.user_admin")
        groups = cls.env.ref("ssi_va.va_generator_user_group") + cls.env.ref(
            "operating_unit.group_multi_operating_unit"
        )
        groups.sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "TOUR VAGENOU Partner",
            }
        )

    def test_create(self):
        """Run the delta create tour for ``va_generator``.

        The tour is delta-only: it walks Flow 1 to Flow 3 of the base IK
        (``ssi_va/docs/va_generator/01-create.md``) to reach the
        **Generate VA** wizard, then asserts the **Operating Unit** field
        the delta IK adds to it.

        Three boundaries are deliberate and stated in the tour file as
        well, so that they are read as scope rather than as a hole:

        * Base Flow 4 ("fill in the fields") and base Flow 5 ("Click
          Generate VA") are not walked. The item's design decision scopes
          this tour to the field being rendered in the wizard, and a delta
          tour may not continue into the state actions of the base IK.
          Creating the document is covered by ``ssi_va``'s own create
          tour.
        * The delta IK also states the field appears on the
          ``va_generator`` document form. Only the wizard half is
          asserted, which is the half the design decision names; the
          document-form half belongs to the delta IK
          ``docs/va_generator/02-edit.md``, which the item excludes from
          its tour list.
        * The "Modified -- Record Visibility" section of the delta IK
          produces no step: the design decision rules it out, and which
          documents a record rule sees is a value fact covered by
          ``tests/test_data_va_generator_operating_unit.yaml``.

        IK: docs/va_generator/01-create.md
        """
        self.start_tour(
            "/web", "ssi_va_operating_unit_va_generator_create", login="admin"
        )
