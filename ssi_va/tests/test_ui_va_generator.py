# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiVAGenerator(HttpSavepointCase):
    """UI/UX tour tests for the ``va_generator`` work instructions.

    Every ``test_*`` method runs the tour paired with the IK file named
    in its docstring (``docs/va_generator/NN-*.md``). Pre-Condition data
    of those IK files is prepared here in Python -- never through UI
    steps -- because ``va_generator`` is a transactional document whose
    prerequisites (bank, biller with a bank code, merchant with a biller
    code, generator type, usage, exporter, source record) would
    otherwise take a whole tour of their own to build.
    """

    #: The Financial Accounting app exposes several menu sections and the
    #: va_generator statusbar carries five states; the default 1366px
    #: viewport pushes part of both into overflow, where a tour trigger
    #: would fail the implicit ``:visible`` check.
    browser_size = "1920x1080"

    @classmethod
    def setUpClass(cls):
        """Prepare the IK Pre-Conditions of the va_generator tours.

        Covers the Pre-Condition types the three IK files declare:

        * ``Access`` -- admin is put in ``Virtual Account Generator /
          User``, the group the IK names as actor. It is also put in
          ``Virtual Account Generator / All``, because the record rules
          of this model restrict a plain internal user to the documents
          they are responsible for, and the documents below are created
          by the test cursor's superuser rather than by admin.
        * ``Data`` -- generator types, banks, billers holding a bank
          code for those banks, merchants holding a biller code, bank
          account usages and exporters, so that every many2one of the
          Generate VA wizard and of the document form can be picked.
        * ``Record`` -- one ``va_generator`` document per tour that acts
          on an existing document: draft ones for the edit, delete and
          confirm tours, and documents already sitting in ``confirm``
          for the approve, reject and restart approval tours. Each
          carries a Biller of its own, because a document's number stays
          ``/`` until it reaches done, so the Biller column of the tree
          view is what makes its row identifiable.

        The ``Config`` Pre-Conditions need no setup either: the Generate
        VA entry in the source model's Action menu is bound to
        ``res.partner`` by the module (``wizards/generate_va.xml``), and
        the ``policy.template`` and ``approval.template`` the approval
        IK files require ship with it as well (``policy_template/`` and
        ``approval_template/``). The shipped approval template selects
        its approvers by group, and ``base.user_admin`` is a member of
        ``Virtual Account Generator / Validator`` out of the box, which
        is what puts the tour user on the pending approval level.
        """
        super().setUpClass()

        cls.user_admin = cls.env.ref("base.user_admin")
        groups = cls.env.ref("ssi_va.va_generator_user_group") + cls.env.ref(
            "ssi_va.va_generator_all_group"
        )
        groups.sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

        cls.model_res_partner = cls.env.ref("base.model_res_partner")
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "TOUR VAGEN Partner",
            }
        )

        #: ``Data`` Pre-Condition of the cancel IK: the Select Cancel
        #: Reason wizard only offers the reasons of
        #: ``ir.model.all_cancel_reason_ids``, which merges the reasons
        #: linked to the model with the globally usable ones. Creating it
        #: with ``global_use`` avoids having to link it to ``va_generator``
        #: through ``ir.model`` itself.
        cls.cancel_reason = cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR VAGEN Cancel Reason",
                "code": "TOURVAGENCR",
                "global_use": True,
            }
        )

        cls.type_alpha = cls._create_generator_type("TOUR VAGEN Type Alpha")
        cls.type_beta = cls._create_generator_type("TOUR VAGEN Type Beta")

        cls.bank_alpha = cls.env["res.bank"].create(
            {
                "name": "TOUR VAGEN Bank Alpha",
            }
        )
        cls.bank_beta = cls.env["res.bank"].create(
            {
                "name": "TOUR VAGEN Bank Beta",
            }
        )

        cls.biller_create = cls._create_biller(
            "TOUR VAGEN Biller Create", cls.bank_alpha, "VAC01"
        )
        cls.biller_edit = cls._create_biller(
            "TOUR VAGEN Biller Edit", cls.bank_alpha, "VAE01"
        )
        cls.biller_delete = cls._create_biller(
            "TOUR VAGEN Biller Delete", cls.bank_alpha, "VAD01"
        )
        cls.biller_beta = cls._create_biller(
            "TOUR VAGEN Biller Beta", cls.bank_beta, "VAB01"
        )
        cls.biller_confirm = cls._create_biller(
            "TOUR VAGEN Biller Confirm", cls.bank_alpha, "VACF1"
        )
        cls.biller_approve = cls._create_biller(
            "TOUR VAGEN Biller Approve", cls.bank_alpha, "VAAP1"
        )
        cls.biller_reject = cls._create_biller(
            "TOUR VAGEN Biller Reject", cls.bank_alpha, "VARJ1"
        )
        cls.biller_restart = cls._create_biller(
            "TOUR VAGEN Biller Restart", cls.bank_alpha, "VART1"
        )
        #: The tree row of a document is matched with ``:contains(...)`` on
        #: its Biller name, so no biller name below may be a substring of
        #: another one -- "TOUR VAGEN Biller Restart" already exists, hence
        #: "Redraft" rather than "Restart Document" for the restart IK.
        cls.biller_cancel = cls._create_biller(
            "TOUR VAGEN Biller Cancel", cls.bank_alpha, "VACN1"
        )
        cls.biller_redraft = cls._create_biller(
            "TOUR VAGEN Biller Redraft", cls.bank_alpha, "VARD1"
        )
        cls.biller_number = cls._create_biller(
            "TOUR VAGEN Biller Number", cls.bank_alpha, "VANM1"
        )
        cls.biller_export = cls._create_biller(
            "TOUR VAGEN Biller Export", cls.bank_alpha, "VAEX1"
        )

        cls.merchant_create = cls._create_merchant(
            "TOUR VAGEN Merchant Create", cls.biller_create, "MC01"
        )
        cls.merchant_edit = cls._create_merchant(
            "TOUR VAGEN Merchant Edit", cls.biller_edit, "ME01"
        )

        cls.usage_alpha = cls._create_master_data(
            "res_partner_bank_usage", "TOUR VAGEN Usage Alpha"
        )
        cls.usage_beta = cls._create_master_data(
            "res_partner_bank_usage", "TOUR VAGEN Usage Beta"
        )
        cls.exporter_alpha = cls._create_master_data(
            "va_generator_exporter", "TOUR VAGEN Exporter Alpha"
        )
        cls.exporter_beta = cls._create_master_data(
            "va_generator_exporter", "TOUR VAGEN Exporter Beta"
        )

        cls.generator_edit = cls._create_generator(
            cls.biller_edit,
            merchant=cls.merchant_edit,
        )
        cls.generator_delete = cls._create_generator(cls.biller_delete)
        cls.generator_confirm = cls._create_generator(cls.biller_confirm)
        cls.generator_approve = cls._create_confirmed_generator(cls.biller_approve)
        cls.generator_reject = cls._create_confirmed_generator(cls.biller_reject)
        cls.generator_restart = cls._create_stalled_generator(cls.biller_restart)
        cls.generator_cancel = cls._create_generator(cls.biller_cancel)
        cls.generator_redraft = cls._create_cancelled_generator(cls.biller_redraft)
        cls.generator_reset_number = cls._create_numbered_generator(cls.biller_number)
        cls.generator_export = cls._create_done_generator(cls.biller_export)

    @classmethod
    def _create_master_data(cls, model_name, name):
        """Create a ``mixin.master_data`` record used as tour data.

        ``code`` is set to ``"/"`` so that several records can coexist:
        ``mixin.master_data._check_duplicate_code`` skips that value.

        :param str model_name: Technical name of the master data model.
        :param str name: Name of the record, matched by the tour in the
            many2one autocomplete dropdown.
        :return: The created record.
        :rtype: :class:`odoo.models.Model`
        """
        return cls.env[model_name].create(
            {
                "name": name,
                "code": "/",
            }
        )

    @classmethod
    def _create_generator_type(cls, name):
        """Create a ``va_generator_type`` used by the tours.

        ``model_id`` is left empty on purpose: a generator type
        restricted to another model is rejected by the Generate VA
        wizard when it is launched from ``res.partner``.

        :param str name: Name of the generator type record.
        :return: The created ``va_generator_type`` record.
        :rtype: :class:`odoo.models.Model`
        """
        return cls._create_master_data("va_generator_type", name)

    @classmethod
    def _create_biller(cls, name, bank, biller_code):
        """Create a ``va_biller`` holding a code for ``bank``.

        The bank code line is what makes the biller selectable: both
        the Generate VA wizard and the document form restrict Biller to
        those holding a Virtual Account code for the selected Bank.

        :param str name: Name of the biller record.
        :param bank: ``res.bank`` the Virtual Account code is issued by.
        :type bank: :class:`odoo.models.Model`
        :param str biller_code: Virtual Account code issued by the bank.
        :return: The created ``va_biller`` record.
        :rtype: :class:`odoo.models.Model`
        """
        return cls.env["va_biller"].create(
            {
                "name": name,
                "code": "/",
                "bank_code_ids": [
                    (
                        0,
                        0,
                        {
                            "bank_id": bank.id,
                            "biller_code": biller_code,
                        },
                    )
                ],
            }
        )

    @classmethod
    def _create_merchant(cls, name, biller, merchant_code):
        """Create a ``va_biller_merchant`` registered under ``biller``.

        The biller code line is what makes the merchant selectable in
        the Generate VA wizard, whose Merchant domain only offers
        merchants registered for the selected biller.

        :param str name: Name of the merchant record.
        :param biller: ``va_biller`` the merchant is registered under.
        :type biller: :class:`odoo.models.Model`
        :param str merchant_code: Merchant code for that biller-bank
            combination.
        :return: The created ``va_biller_merchant`` record.
        :rtype: :class:`odoo.models.Model`
        """
        return cls.env["va_biller_merchant"].create(
            {
                "name": name,
                "code": "/",
                "biller_code_ids": [
                    (
                        0,
                        0,
                        {
                            "biller_id": biller.bank_code_ids[0].id,
                            "merchant_code": merchant_code,
                        },
                    )
                ],
            }
        )

    @classmethod
    def _create_generator(cls, biller, merchant=None):
        """Create a draft ``va_generator`` acted on by a tour.

        The document is left in ``draft`` -- the state both the edit
        and the delete IK require -- and gets one source data line for
        the tour partner, mirroring what the Generate VA wizard would
        have produced.

        :param biller: ``va_biller`` of the document; its name is what
            identifies the document's row in the tree view.
        :type biller: :class:`odoo.models.Model`
        :param merchant: Optional ``va_biller_merchant`` of the
            document.
        :type merchant: :class:`odoo.models.Model` or None
        :return: The created ``va_generator`` record.
        :rtype: :class:`odoo.models.Model`
        """
        return cls.env["va_generator"].create(
            {
                "type_id": cls.type_alpha.id,
                "bank_id": biller.bank_code_ids[0].bank_id.id,
                "biller_id": biller.id,
                "merchant_id": merchant and merchant.id or False,
                "usage_id": cls.usage_alpha.id,
                "exporter_id": cls.exporter_alpha.id,
                "source_data_ids": [
                    (
                        0,
                        0,
                        {
                            "model_id": cls.model_res_partner.id,
                            "res_id": cls.partner.id,
                        },
                    )
                ],
            }
        )

    @classmethod
    def _create_confirmed_generator(cls, biller):
        """Create a ``va_generator`` waiting for approval.

        Used for the approve and the reject IK files, whose Record
        Pre-Condition is a document in **Waiting for Approval**. The
        document is taken there through ``action_confirm`` so that the
        approval template is resolved and the approval records are
        created exactly as they would be for a user, which is what makes
        the tour user a pending approver.

        ``bypass_policy_check`` is set because the setup runs as the
        test cursor's superuser rather than as the actor of the IK; the
        policy itself is exercised by the confirm tour.

        :param biller: ``va_biller`` of the document; its name is what
            identifies the document's row in the tree view.
        :type biller: :class:`odoo.models.Model`
        :return: The created ``va_generator`` record, in ``confirm``.
        :rtype: :class:`odoo.models.Model`
        """
        generator = cls._create_generator(biller)
        generator.with_context(bypass_policy_check=True).action_confirm()
        return generator

    @classmethod
    def _create_stalled_generator(cls, biller):
        """Create a ``va_generator`` stuck without an approval template.

        This is the Record Pre-Condition of the restart approval IK:
        a document in **Waiting for Approval** whose **Approval
        Template** field is empty, which is what makes the **Restart
        Approval Process** button appear.

        ``state`` is written directly instead of calling
        ``action_confirm`` precisely because confirming resolves an
        approval template -- the module ships one matching every
        document. Writing the state reproduces the situation the IK
        describes, a document that reached Waiting for Approval without
        ever getting a template resolved.

        :param biller: ``va_biller`` of the document; its name is what
            identifies the document's row in the tree view.
        :type biller: :class:`odoo.models.Model`
        :return: The created ``va_generator`` record, in ``confirm``
            and without approver.
        :rtype: :class:`odoo.models.Model`
        """
        generator = cls._create_generator(biller)
        generator.write({"state": "confirm"})
        return generator

    @classmethod
    def _create_cancelled_generator(cls, biller):
        """Create a cancelled ``va_generator``.

        This is the Record Pre-Condition of the restart IK, whose first
        allowed starting state is **Cancelled**. The document is taken
        there through ``action_cancel`` so that the cancel reason is
        stored exactly as the Select Cancel Reason wizard would store
        it; the wizard itself is exercised by the cancel tour.

        ``bypass_policy_check`` is set because the setup runs as the test
        cursor's superuser rather than as the actor of the IK.

        :param biller: ``va_biller`` of the document; its name is what
            identifies the document's row in the tree view.
        :type biller: :class:`odoo.models.Model`
        :return: The created ``va_generator`` record, in ``cancel``.
        :rtype: :class:`odoo.models.Model`
        """
        generator = cls._create_generator(biller)
        generator.with_context(bypass_policy_check=True).action_cancel(
            cls.cancel_reason
        )
        return generator

    @classmethod
    def _create_numbered_generator(cls, biller):
        """Create a draft ``va_generator`` carrying a manual number.

        The reset number IK requires a document in **Draft** whose actor
        holds ``manual_number_ok``, i.e. a document whose number may be
        typed by hand. Giving this one such a number is what makes the
        reset observable at all: ``va_generator`` only receives an
        automatic number when it reaches done
        (``_create_sequence_state``), so an untouched draft already
        carries ``/`` and resetting it would change nothing on screen.

        :param biller: ``va_biller`` of the document; its name is what
            identifies the document's row in the tree view.
        :type biller: :class:`odoo.models.Model`
        :return: The created ``va_generator`` record, in ``draft``.
        :rtype: :class:`odoo.models.Model`
        """
        generator = cls._create_generator(biller)
        generator.write({"name": "TOURVAGEN-RESET-0001"})
        return generator

    @classmethod
    def _create_done_generator(cls, biller):
        """Create a ``va_generator`` in the done state.

        This is the Record Pre-Condition of the generate export file IK.
        The document is first confirmed and then taken to done through
        ``action_done`` -- the method the approval mixin itself calls
        once the last approval lands (``_after_approved_method``) --
        rather than through ``action_approve_approval``, because the
        approval path is what the approve tour exercises and repeating
        it here would tie this fixture to the shipped approval template.

        The exporter is already set by ``_create_generator``, which is
        the second Record Pre-Condition of that IK.

        :param biller: ``va_biller`` of the document; its name is what
            identifies the document's row in the tree view.
        :type biller: :class:`odoo.models.Model`
        :return: The created ``va_generator`` record, in ``done``.
        :rtype: :class:`odoo.models.Model`
        """
        generator = cls._create_confirmed_generator(biller)
        generator.with_context(bypass_policy_check=True).action_done()
        return generator

    def test_create(self):
        """Run the create tour for ``va_generator``.

        The third Post-Condition bullet -- the document number is still
        ``/`` -- is not asserted by the tour: it is a field value, and
        reading values is outside the scope of a tour. The sequence
        behaviour behind it is covered by the unit tests in
        ``tests/test_data_va_generator.yaml``.

        IK: docs/va_generator/01-create.md
        """
        self.start_tour("/web", "ssi_va_va_generator_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``va_generator``.

        The tour changes Generator Type, Bank Account Usage and
        Exporter. It deliberately does not change Bank: the only thing
        that sub-bullet of Flow 3 produces on screen is Biller and
        Merchant becoming empty -- two field values, which belong to
        the unit tests. That effect is covered there by the "Changing
        bank_id on the form resets biller_id and merchant_id" scenario
        of ``tests/test_data_va_generator.yaml``.

        IK: docs/va_generator/02-edit.md
        """
        self.start_tour("/web", "ssi_va_va_generator_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``va_generator``.

        IK: docs/va_generator/03-delete.md
        """
        self.start_tour("/web", "ssi_va_va_generator_delete", login="admin")

    def test_confirm(self):
        """Run the confirm tour for ``va_generator``.

        The trailing paragraph of the IK -- the Pre-Condition checks
        that block Confirm with an error message -- is not walked by the
        tour: those are negative paths ending in a ``UserError``, which
        belong to the unit tests and are covered by the "Confirm ...
        raises" scenarios of ``tests/test_data_va_generator.yaml``.

        IK: docs/va_generator/04-confirm.md
        """
        self.start_tour("/web", "ssi_va_va_generator_confirm", login="admin")

    def test_approve(self):
        """Run the approve tour for ``va_generator``.

        The approval template shipped with the module defines a single
        approver level, so the tour walks the second branch of the
        Post-Condition: this approval is the last pending one and the
        document transitions to Done on its own. Its two sub-bullets --
        the issued document number and the generated Virtual Account
        bank accounts -- are values, and stay with the unit tests in
        ``tests/test_data_va_generator.yaml``.

        IK: docs/va_generator/05-approve.md
        """
        self.start_tour("/web", "ssi_va_va_generator_approve", login="admin")

    def test_reject(self):
        """Run the reject tour for ``va_generator``.

        IK: docs/va_generator/06-reject.md
        """
        self.start_tour("/web", "ssi_va_va_generator_reject", login="admin")

    def test_restart_approval(self):
        """Run the restart approval tour for ``va_generator``.

        The tour walks the branch of the Post-Condition in which a
        matching ``approval.template`` is found, because the module
        ships one matching every document. The other branch -- still no
        template matches, so the button remains available -- would need
        that template removed, which no IK file describes.

        IK: docs/va_generator/14-restart-approval.md
        """
        self.start_tour("/web", "ssi_va_va_generator_restart_approval", login="admin")

    def test_cancel(self):
        """Run the cancel tour for ``va_generator``.

        The tour cancels a document sitting in **Draft**, the first of
        the three starting states the IK allows.

        The second Post-Condition bullet -- every Virtual Account bank
        account of the Generated Bank Accounts tab is deleted, so the tab
        becomes empty -- is not asserted by the tour: the item's design
        decision keeps it out, and an emptied one2many is a value fact
        anyway. It is covered by the "Cancelling from done deletes the
        generated bank account" scenario of
        ``tests/test_data_va_generator.yaml``.

        IK: docs/va_generator/10-cancel.md
        """
        self.start_tour("/web", "ssi_va_va_generator_cancel", login="admin")

    def test_restart(self):
        """Run the restart tour for ``va_generator``.

        The tour restarts a document sitting in **Cancelled**, the first
        of the two starting states the IK allows; the Rejected branch
        reaches the very same button through the very same policy field
        (``restart_ok``).

        IK: docs/va_generator/12-restart.md
        """
        self.start_tour("/web", "ssi_va_va_generator_restart", login="admin")

    def test_reset_number(self):
        """Run the reset document number tour for ``va_generator``.

        The second Post-Condition bullet -- the record receives an
        automatic number once it reaches Done -- is not walked by the
        tour: it describes what happens in a later IK, not an outcome of
        this Flow, and the issued number is a value. It stays with the
        unit tests in ``tests/test_data_va_generator.yaml``.

        IK: docs/va_generator/13-reset-number.md
        """
        self.start_tour("/web", "ssi_va_va_generator_reset_number", login="admin")

    def test_generate_export_file(self):
        """Run the generate export file tour for ``va_generator``.

        Two boundaries of this tour are deliberate and stated here as
        well as in the tour file itself, so that they are read as scope
        rather than as a hole:

        * The Post-Condition -- a new attachment is added to the
          document -- is not asserted. The attachment name pattern is
          excluded by the item's design decision, and the arrival of the
          attachment itself is invisible in 14.0: the chatter fetches
          its attachment list when it is mounted and is not refetched
          when a header button reloads the record, so the paperclip
          counter still reads what it read before the click. The
          attachment creation, its count per click and its extension are
          covered by the "Generate export file ..." scenarios of
          ``tests/test_data_va_generator.yaml``.
        * The trailing paragraph of the IK -- the two Pre-Condition
          checks that block the action with an error message -- is not
          walked: those are negative paths ending in a ``UserError``,
          which belong to the unit tests and are covered there by the
          "Generate export file is rejected ..." scenarios.

        Flow 3 ("If Exporter is not yet set, select one now") is a
        conditional step whose condition is false here: the Record
        Pre-Condition requires the Exporter to be filled in, and
        ``setUpClass`` fills it.

        IK: docs/va_generator/15-generate-export-file.md
        """
        self.start_tour(
            "/web", "ssi_va_va_generator_generate_export_file", login="admin"
        )
