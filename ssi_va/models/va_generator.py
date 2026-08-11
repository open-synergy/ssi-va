# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.base.models.res_bank import sanitize_account_number
from odoo.addons.ssi_decorator import ssi_decorator


class VAGenerator(models.Model):
    """
    Represents a Virtual Account (VA) generation batch. Combines a biller
    (and, optionally, a merchant registered under that biller) with a
    generator type to compute unique VA codes for a set of source data
    records. When the document is set to done, it creates one
    ``res.partner.bank`` record (the generated Virtual Account) for
    every combination of source data and biller/merchant bank code.
    """

    _name = "va_generator"
    _description = "Virtual Account Generator"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_confirm",
    ]

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "done"
    _approval_state = "confirm"
    _after_approved_method = "action_done"

    # Attributes related to add element on view automatically.
    # Done is reached automatically once approval completes (see
    # _after_approved_method above), so no manual "Done" button/policy
    # field is inserted on the form.
    _automatically_insert_view_element = True
    _automatically_insert_done_policy_fields = False
    _automatically_insert_done_button = False

    _statusbar_visible_label = "draft,confirm,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute.
    # NOTE: intentionally "done" (not "confirm") — of the mixins inherited
    # here (transaction_cancel/transaction_done/transaction_confirm), only
    # mixin.transaction_done reads _create_sequence_state, and only for the
    # value "done" (see ssi_transaction_done_mixin/models/
    # mixin_transaction_done.py::_prepare_done_data). "name" therefore stays
    # "/" until the document reaches done, matching the sq_letter/
    # incoming_letter precedent (same mixin combination).
    _create_sequence_state = "done"

    type_id = fields.Many2one(
        string="Generator Type",
        comodel_name="va_generator_type",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Generator type whose python_code computes the unique VA "
        "code appended to the biller/merchant code for every generated "
        "Virtual Account number.",
    )
    bank_id = fields.Many2one(
        string="Bank",
        comodel_name="res.bank",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Bank this generation batch is for. Restricts the "
        "selectable Biller to those holding a Virtual Account code "
        "for this bank, and restricts generated Virtual Account bank "
        "accounts to this bank only, even when the biller/merchant "
        "also holds codes for other banks.",
    )
    biller_id = fields.Many2one(
        string="Biller",
        comodel_name="va_biller",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Biller this generation batch is for. Determines the "
        "biller code(s) used when composing generated Virtual Account "
        "numbers.",
    )
    merchant_id = fields.Many2one(
        string="Merchant",
        comodel_name="va_biller_merchant",
        required=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Optional merchant under the selected biller. When set, "
        "Virtual Account numbers are generated at merchant level using "
        "the merchant code registered for the selected biller. Left "
        "empty, Virtual Account numbers are generated at biller level.",
    )
    usage_id = fields.Many2one(
        string="Bank Account Usage",
        comodel_name="res_partner_bank_usage",
        required=False,
        ondelete="restrict",
        readonly=True,
        states={"draft": [("readonly", False)]},
        help="Usage/purpose copied to every res.partner.bank generated "
        "by this document. Optional - left empty, generated bank "
        "accounts are created with no usage set.",
    )
    source_data_ids = fields.One2many(
        string="Source Data",
        comodel_name="va_generator.source_data",
        inverse_name="va_generator_id",
        readonly=True,
        help="Source records (e.g. partners) that Virtual Account "
        "numbers are generated for. Populated through a dedicated "
        "wizard (implemented separately) or directly via ORM — not "
        "meant to be filled in manually by the user.",
    )
    bank_account_ids = fields.One2many(
        string="Generated Bank Accounts",
        comodel_name="res.partner.bank",
        inverse_name="va_generator_id",
        readonly=True,
        help="Virtual Account bank accounts generated by this document "
        "once it reaches the done state.",
    )
    num_of_skipped_source_data = fields.Integer(
        string="Number of Skipped Source Data",
        compute="_compute_num_of_skipped_source_data",
        store=True,
        compute_sudo=True,
        help="Number of source data lines whose Virtual Account "
        "number(s) already existed as a bank account, and were "
        "therefore skipped instead of generating a duplicate.",
    )
    exporter_id = fields.Many2one(
        string="Exporter",
        comodel_name="va_generator_exporter",
        required=False,
        readonly=True,
        states={
            "draft": [("readonly", False)],
            "done": [("readonly", False)],
        },
        help="Layout and file format used when generating the export "
        "file for this document. Left editable in the done state as "
        "well, so a document that already reached done without one "
        "set can still be fixed without cancelling it (cancelling "
        "would delete every generated Virtual Account).",
    )

    @api.model
    def _get_policy_field(self):
        res = super(VAGenerator, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @api.depends("source_data_ids.generation_state")
    def _compute_num_of_skipped_source_data(self):
        """Count source data lines currently marked as skipped.

        :return: nothing; assigns ``num_of_skipped_source_data``
        """
        for record in self:
            result = len(
                record.source_data_ids.filtered(
                    lambda line: line.generation_state == "skipped"
                )
            )
            record.num_of_skipped_source_data = result

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch

    @api.onchange("bank_id")
    def onchange_biller_id(self):
        self.biller_id = False

    @api.onchange("bank_id")
    def onchange_merchant_id(self):
        self.merchant_id = False

    @ssi_decorator.pre_confirm_check()
    def _10_check_source_data(self):
        self.ensure_one()
        if not self.source_data_ids:
            error_message = """
Document Type: %s
Context: Confirm document
Database ID: %s
Problem: No source data has been added
Solution: Add at least one source data line before confirming
""" % (
                self._description,
                self.id,
            )
            raise UserError(_(error_message))

    @ssi_decorator.pre_confirm_check()
    def _15_check_biller_bank_id(self):
        """Ensure the selected biller has a code for the selected bank.

        Raises ``UserError`` when ``biller_id.bank_code_ids`` has no
        line whose ``bank_id`` matches ``self.bank_id``, since without
        one no Virtual Account bank account could be generated for
        that bank when the document reaches done.
        """
        self.ensure_one()
        if not self.biller_id.bank_code_ids.filtered(
            lambda line: line.bank_id == self.bank_id
        ):
            error_message = """
Document Type: %s
Context: Confirm document
Database ID: %s
Problem: Biller %s has no Virtual Account code registered for bank %s
Solution: Register a bank code for the biller under the selected \
bank, or choose a different bank/biller combination
""" % (
                self._description,
                self.id,
                self.biller_id.name,
                self.bank_id.name,
            )
            raise UserError(_(error_message))

    @ssi_decorator.pre_confirm_check()
    def _20_check_merchant_biller_code(self):
        self.ensure_one()
        if not self.merchant_id:
            return
        if not self._get_merchant_biller_code_lines():
            error_message = """
Document Type: %s
Context: Confirm document
Database ID: %s
Problem: Merchant %s has no biller code registered for biller %s
Solution: Register a biller code for the merchant under the selected \
biller, or remove the merchant to generate Virtual Account numbers at \
biller level only
""" % (
                self._description,
                self.id,
                self.merchant_id.name,
                self.biller_id.name,
            )
            raise UserError(_(error_message))

    @ssi_decorator.pre_confirm_check()
    def _30_check_partner(self):
        self.ensure_one()
        for source in self.source_data_ids:
            try:
                self.type_id.generate_partner(
                    extra_localdict=self._get_partner_localdict(source)
                )
            except Exception as error:
                error_message = """
Document Type: %s
Context: Confirm document
Database ID: %s
Problem: Source data %s could not be resolved into a res.partner record: %s
Solution: Fix the generator type's partner resolution Python code so it \
resolves this source data line into a single res.partner record
""" % (
                    self._description,
                    self.id,
                    source.display_name,
                    error,
                )
                raise UserError(_(error_message))

    def _get_merchant_biller_code_lines(self):
        self.ensure_one()
        return self.merchant_id.biller_code_ids.filtered(
            lambda line: line.biller_id.va_biller_id == self.biller_id
            and line.biller_id.bank_id == self.bank_id
        )

    @ssi_decorator.post_confirm_action()
    def _10_evaluate_source_data(self):
        """Preview the VA number(s) and skip status per source line.

        Runs after the document reaches ``confirm`` (state already
        written). For every ``source_data_ids`` line, recomposes its
        Virtual Account number(s) via ``_get_va_number`` and checks
        each one against already-existing ``res.partner.bank``
        records (``_get_existing_bank_account``), writing
        ``acc_number``, ``existing_bank_account_ids`` and
        ``generation_state`` (``"skipped"`` only when every number
        computed for the line already exists, ``"to_generate"``
        otherwise).

        This is only a preview: it assumes
        ``va_generator_type.python_code`` is deterministic for the
        same (source data, schema) pair, but ``_done`` still
        recomputes and re-evaluates every line from scratch before
        creating bank accounts, since data can change between
        confirm and done (e.g. an approval delay, or another
        document generating a colliding number in the meantime).

        :return: nothing; writes every line in ``source_data_ids``
        """
        self.ensure_one()
        schema_lines = self._get_bank_schema_lines()
        for source in self.source_data_ids:
            self._evaluate_source_data(source, schema_lines)

    def _evaluate_source_data(self, source_data, schema_lines):
        """Write the confirm-time skip preview for one source line.

        :param source_data: a ``va_generator.source_data`` record
        :param schema_lines: list of schema dicts built by
            ``_get_bank_schema_lines``
        :return: nothing; writes ``source_data``
        """
        self.ensure_one()
        partner = self.type_id.generate_partner(
            extra_localdict=self._get_partner_localdict(source_data)
        )
        acc_numbers = []
        existing_bank_accounts = self.env["res.partner.bank"]
        conflict_flags = []
        for schema in schema_lines:
            acc_number = self._get_va_number(source_data, partner, schema)
            acc_numbers.append(acc_number)
            existing = self._get_existing_bank_account(acc_number)
            conflict_flags.append(bool(existing))
            if existing:
                existing_bank_accounts |= existing
        state = "to_generate"
        if conflict_flags and all(conflict_flags):
            state = "skipped"
        source_data.write(
            self._prepare_source_data_evaluation_data(
                acc_numbers, existing_bank_accounts, state
            )
        )

    def _prepare_source_data_evaluation_data(
        self, acc_numbers, existing_bank_accounts, state
    ):
        """Build the ``va_generator.source_data`` values to write.

        Shared by the confirm-time preview (``_evaluate_source_data``)
        and the final generation (``_generate_source_data``), so both
        write the same three fields the same way.

        Extension point: override to write additional fields when
        recording a line's evaluation outcome.

        :param acc_numbers: list of composed VA number strings
        :param existing_bank_accounts: ``res.partner.bank`` recordset
            of every collision found for ``acc_numbers``
        :param state: ``generation_state`` value to write
        :return: dict of ``va_generator.source_data`` values
        """
        return {
            "acc_number": ", ".join(acc_numbers),
            "existing_bank_account_ids": [(6, 0, existing_bank_accounts.ids)],
            "generation_state": state,
        }

    @ssi_decorator.post_done_action()
    def _10_generate_bank_account(self):
        self.ensure_one()
        self._done()

    @ssi_decorator.post_cancel_action()
    def _10_delete_bank_account(self):
        self.ensure_one()
        self.bank_account_ids.unlink()

    @ssi_decorator.post_restart_action()
    def _10_reset_source_data(self):
        """Reset every source data line back to its initial state.

        Runs after the document returns to ``draft`` (state already
        written). Clears the preview written by
        ``_10_evaluate_source_data`` (or the final result written by
        ``_done``), so a subsequent re-confirm starts from a clean
        slate rather than showing a stale evaluation.

        :return: nothing; writes every line in ``source_data_ids``
        """
        self.ensure_one()
        self.source_data_ids.write(
            {
                "generation_state": "pending",
                "acc_number": False,
                "existing_bank_account_ids": [(5, 0, 0)],
            }
        )

    def _done(self):
        self.ensure_one()
        schema_lines = self._get_bank_schema_lines()
        for source in self.source_data_ids:
            self._generate_source_data(source, schema_lines)

    def _generate_source_data(self, source_data, schema_lines):
        """Create the missing bank accounts for one source data line.

        Re-evaluates every schema line's VA number and skip status
        from scratch — does not trust the confirm-time preview
        written by ``_10_evaluate_source_data`` (see the determinism
        assumption documented there) — creates a ``res.partner.bank``
        via ``_create_bank_account`` for every number that does not
        already exist as of this evaluation, and writes the final
        ``acc_number``/``existing_bank_account_ids``/
        ``generation_state`` on ``source_data``: ``"generated"`` when
        at least one bank account was created for this line,
        ``"skipped"`` when every number already existed.

        :param source_data: a ``va_generator.source_data`` record
        :param schema_lines: list of schema dicts built by
            ``_get_bank_schema_lines``
        :return: nothing; creates ``res.partner.bank`` records and
            writes ``source_data``
        """
        self.ensure_one()
        partner = self.type_id.generate_partner(
            extra_localdict=self._get_partner_localdict(source_data)
        )
        acc_numbers = []
        existing_bank_accounts = self.env["res.partner.bank"]
        created = False
        for schema in schema_lines:
            acc_number = self._get_va_number(source_data, partner, schema)
            acc_numbers.append(acc_number)
            existing = self._get_existing_bank_account(acc_number)
            if existing:
                existing_bank_accounts |= existing
            else:
                self._create_bank_account(
                    source_data, partner, schema, acc_number=acc_number
                )
                created = True
        state = "generated" if created else "skipped"
        source_data.write(
            self._prepare_source_data_evaluation_data(
                acc_numbers, existing_bank_accounts, state
            )
        )

    def _get_partner_localdict(self, source):
        self.ensure_one()
        return {
            "generator": self,
            "source_data": source,
            "source_record": source.source_data_id,
            "biller": self.biller_id,
            "merchant": self.merchant_id,
        }

    def _get_bank_schema_lines(self):
        self.ensure_one()
        result = []
        if self.merchant_id:
            for line in self._get_merchant_biller_code_lines():
                result.append(
                    {
                        "bank": line.bank_id,
                        "biller_code_str": line.biller_id.biller_code,
                        "merchant_code_str": line.merchant_code,
                    }
                )
        else:
            bank_code_lines = self.biller_id.bank_code_ids.filtered(
                lambda code_line: code_line.bank_id == self.bank_id
            )
            for line in bank_code_lines:
                result.append(
                    {
                        "bank": line.bank_id,
                        "biller_code_str": line.biller_code,
                        "merchant_code_str": "",
                    }
                )
        return result

    def _create_bank_account(self, source_data, partner, schema, acc_number=None):
        """Create the ``res.partner.bank`` for one source/schema pair.

        :param source_data: a ``va_generator.source_data`` record
        :param partner: the resolved ``res.partner`` for this line
        :param schema: one dict from ``_get_bank_schema_lines``
        :param acc_number: pre-computed VA number string, so a caller
            that already evaluated it (e.g. ``_generate_source_data``,
            to check whether it already exists) does not have to
            trigger a second, possibly non-deterministic,
            ``type_id.generate_code`` call for the same pair; computed
            via ``_get_va_number`` when omitted
        :return: nothing; creates a ``res.partner.bank`` record
        """
        self.ensure_one()
        if acc_number is None:
            acc_number = self._get_va_number(source_data, partner, schema)
        self.env["res.partner.bank"].create(
            self._prepare_bank_account_data(partner, schema["bank"], acc_number)
        )

    def _get_va_number(self, source_data, partner, schema):
        """Compute the VA number for one source data / schema pair.

        Wraps ``type_id.generate_code`` and the shared number
        composition (``_compose_va_number``) so every code path —
        the confirm-time preview (``_evaluate_source_data``) and the
        final generation (``_create_bank_account``/
        ``_generate_source_data``) — composes the exact same number
        for the same inputs. Assumes ``va_generator_type.python_code``
        is deterministic for the same (source data, schema) pair.

        :param source_data: a ``va_generator.source_data`` record
        :param partner: the resolved ``res.partner`` for this line
        :param schema: one dict from ``_get_bank_schema_lines``
        :return: composed VA number string
        """
        self.ensure_one()
        unique_code = self.type_id.generate_code(
            extra_localdict={
                "biller": self.biller_id,
                "merchant": self.merchant_id,
                "bank": schema["bank"],
                "partner": partner,
                "source_data": source_data,
                "source_record": source_data.source_data_id,
            }
        )
        return self._compose_va_number(schema, unique_code)

    def _compose_va_number(self, schema, unique_code):
        """Compose the VA number string from a schema line and code.

        Split off from ``_create_bank_account`` so the confirm-time
        evaluation can compose the exact same number without
        creating a bank account.

        :param schema: one dict from ``_get_bank_schema_lines``
        :param unique_code: string returned by
            ``type_id.generate_code``
        :return: composed VA number string
        """
        return "%s%s%s" % (
            schema["biller_code_str"],
            schema["merchant_code_str"],
            unique_code,
        )

    def _get_existing_bank_account_criteria(self, acc_number):
        """Build the domain matching an existing colliding account.

        Mirrors the database-level uniqueness constraint on
        ``res.partner.bank`` (``sanitized_acc_number`` +
        ``company_id``; see ``unique_number`` in
        ``odoo.addons.base.models.res_bank``).

        Extension point: override to widen or narrow the collision
        criteria.

        :param acc_number: raw (unsanitized) VA number string
        :return: an Odoo search domain
        """
        self.ensure_one()
        return [
            ("sanitized_acc_number", "=", sanitize_account_number(acc_number)),
            ("company_id", "=", self.env.company.id),
        ]

    def _get_existing_bank_account(self, acc_number):
        """Find the existing bank account colliding with a VA number.

        Evaluated with ``sudo()`` since the uniqueness constraint
        this mirrors applies database-wide, independent of record
        rules — a colliding account hidden by a record rule from the
        current user must still be detected.

        :param acc_number: raw (unsanitized) VA number string
        :return: a ``res.partner.bank`` recordset, empty if no
            collision exists
        """
        self.ensure_one()
        return (
            self.env["res.partner.bank"]
            .sudo()
            .search(
                self._get_existing_bank_account_criteria(acc_number),
                limit=1,
            )
        )

    def _prepare_bank_account_data(self, partner, bank, acc_number):
        self.ensure_one()
        return {
            "partner_id": partner.id,
            "bank_id": bank.id,
            "acc_number": acc_number,
            "va_generator_id": self.id,
            "usage_id": self.usage_id.id,
        }

    def action_generate_export_file(self):
        for record in self.sudo():
            record._generate_export_file()

    def _generate_export_file(self):
        self.ensure_one()
        if self.state != "done":
            error_message = """
Document Type: %s
Context: Generate export file
Database ID: %s
Problem: Document is not in the done state
Solution: Generate the export file only after the document reaches done
""" % (
                self._description,
                self.id,
            )
            raise UserError(_(error_message))
        if not self.exporter_id:
            error_message = """
Document Type: %s
Context: Generate export file
Database ID: %s
Problem: No exporter has been selected
Solution: Select an exporter before generating the export file
""" % (
                self._description,
                self.id,
            )
            raise UserError(_(error_message))
        content = self.exporter_id.generate_file(
            extra_localdict=self._get_export_file_localdict()
        )
        self.env["ir.attachment"].create(
            self._prepare_export_file_attachment_data(content)
        )

    def _get_export_file_localdict(self):
        self.ensure_one()
        return {
            "generator": self,
            "biller": self.biller_id,
            "merchant": self.merchant_id,
            "bank_account_ids": self.bank_account_ids,
        }

    def _prepare_export_file_attachment_data(self, content):
        self.ensure_one()
        return {
            "name": self._get_export_file_name(),
            "res_model": self._name,
            "res_id": self.id,
            "type": "binary",
            "datas": base64.b64encode(content),
        }

    def _get_export_file_name(self):
        self.ensure_one()
        timestamp = fields.Datetime.now().strftime("%Y%m%d_%H%M%S")
        extension = self.exporter_id.get_file_extension()
        safe_name = (self.name or "").replace("/", "-")
        return "%s-%s.%s" % (safe_name, timestamp, extension)
