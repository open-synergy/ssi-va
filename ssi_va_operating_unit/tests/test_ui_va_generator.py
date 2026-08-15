# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiVAGeneratorOperatingUnit(HttpSavepointCase):
    """UI/UX tour tests for the ``va_generator`` delta work instructions.

    ``ssi_va_operating_unit`` is an extension module, so its IK files are
    delta IK files: they carry no Flow of their own, only an "Additional
    Fields" section on top of the Flow written in ``ssi_va``. The tours
    run here are delta-only accordingly -- each borrows the navigation
    of its base Flow and asserts only that the **Operating Unit** field
    is rendered where the matching delta IK says it is: the **Generate
    VA** wizard for ``01-create.md``, the ``va_generator`` document form
    for ``02-edit.md``.

    Pre-Condition data is prepared in Python -- never through UI steps --
    so that each tour walks its own delta and nothing else.
    """

    #: The Contacts list and its search view are laid out for a wide
    #: viewport; the default 1366px one pushes part of the control panel
    #: into overflow, where a tour trigger would fail the implicit
    #: ``:visible`` check.
    browser_size = "1920x1080"

    @classmethod
    def setUpClass(cls):
        """Prepare the IK Pre-Conditions of the delta va_generator tours.

        Covers both Pre-Condition types the delta IK files declare, plus
        what the base Flow each tour borrows needs:

        * ``Module`` -- satisfied by the module being installed, which is
          what makes this test run at all.
        * ``Access`` -- the tour user is put in
          ``operating_unit.group_multi_operating_unit``, without which the
          **Operating Unit** field is not rendered at all and the tours
          would fail for the wrong reason. ``base.user_admin`` already
          holds it through ``group_manager_operating_unit``; it is written
          explicitly here so the Pre-Condition does not depend on that
          implication staying in place.
        * ``Access`` of the base Flow -- the same user is put in
          ``Virtual Account Generator / User``, the group the base IK
          names as actor for both ``01-create.md`` and ``02-edit.md``.
        * ``Data`` of the base Flow of ``01-create.md`` -- one
          ``res.partner`` to select in the Contacts list before opening
          the wizard.
        * ``Record`` of the base Flow of ``02-edit.md`` -- one draft
          ``va_generator`` document, carrying a Biller of its own since a
          draft document's number stays ``/`` and the tour has to
          identify its row some other way.
        * ``Data`` of the delta tour of ``02-edit.md`` -- one
          ``operating.unit`` record to pick from the **Operating Unit**
          dropdown, proving the field can be changed.

        The ``Config`` Pre-Condition of the base Flow of ``01-create.md``
        needs no setup: the **Generate VA** entry of the Action menu is
        bound to ``res.partner`` by ``ssi_va`` itself
        (``wizards/generate_va.xml``). The generator type and biller
        records base Flow 4 of that IK would need are not created either
        -- that tour stops before that step, see :meth:`test_create`.
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

        cls.bank = cls.env["res.bank"].create(
            {
                "name": "TOUR VAGENOU Bank",
            }
        )
        cls.biller_edit = cls.env["va_biller"].create(
            {
                "name": "TOUR VAGENOU Biller Edit",
                "code": "/",
            }
        )
        cls.generator_type = cls.env["va_generator_type"].create(
            {
                "name": "TOUR VAGENOU Type",
                "code": "/",
            }
        )
        cls.generator_edit = cls.env["va_generator"].create(
            {
                "type_id": cls.generator_type.id,
                "bank_id": cls.bank.id,
                "biller_id": cls.biller_edit.id,
            }
        )

        cls.operating_unit = cls.env["operating.unit"].create(
            {
                "name": "TOUR VAGENOU Operating Unit",
                "code": "VA-OU-EDIT",
                "partner_id": cls.env.ref("base.main_partner").id,
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
          asserted here, which is the half this IK's own Additional
          Fields section names; the document-form half is asserted by
          the delta IK ``docs/va_generator/02-edit.md``, covered by
          :meth:`test_edit`.
        * The "Modified -- Record Visibility" section of the delta IK
          produces no step: the design decision rules it out, and which
          documents a record rule sees is a value fact covered by
          ``tests/test_data_va_generator_operating_unit.yaml``.

        IK: docs/va_generator/01-create.md
        """
        self.start_tour(
            "/web", "ssi_va_operating_unit_va_generator_create", login="admin"
        )

    def test_edit(self):
        """Run the delta edit tour for ``va_generator``.

        The tour is delta-only: it walks Flow 1 and Flow 2 of the base
        IK (``ssi_va/docs/va_generator/02-edit.md``) to open the record
        in edit mode, then asserts the **Operating Unit** field the
        delta IK adds to the document form and changes it -- proving it
        "can still be changed while editing", as the delta IK states --
        before saving.

        Two boundaries are deliberate and stated in the tour file as
        well, so that they are read as scope rather than as a hole:

        * Base Flow 3 ("change the required fields") and any state
          action are not walked. The item's design decision scopes this
          tour to the Operating Unit field alone, and a delta tour may
          not continue into the confirm/approve actions of the base IK.
        * The persisted value of Operating Unit after Save is not
          asserted -- reading a field's stored value is unit test
          territory. It is covered by
          ``tests/test_data_va_generator_operating_unit.yaml``.

        IK: docs/va_generator/02-edit.md
        """
        self.start_tour(
            "/web", "ssi_va_operating_unit_va_generator_edit", login="admin"
        )
