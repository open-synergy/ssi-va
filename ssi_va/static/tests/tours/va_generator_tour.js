// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_va.va_generator_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Every record below is created by tests/test_ui_va_generator.py. The
    // names are the "glue" between the Python Pre-Condition data and the UI
    // steps: they are typed into the many2one inputs and matched in the
    // autocomplete dropdowns.
    //
    // Each dropdown step types a STRICT PREFIX of the name it then matches.
    // That is deliberate: the "Create ..." entry of a 14.0 autocomplete
    // carries the typed text verbatim, so matching on the typed text itself
    // could quick-create a record instead of picking the intended one
    // whenever the domain leaves no match.
    var PARTNER = "TOUR VAGEN Partner";
    var TYPE_PREFIX = "TOUR VAGEN Type";
    var TYPE_ALPHA = "TOUR VAGEN Type Alpha";
    var TYPE_BETA = "TOUR VAGEN Type Beta";
    var BANK_PREFIX = "TOUR VAGEN Bank";
    var BANK_ALPHA = "TOUR VAGEN Bank Alpha";
    var BILLER_PREFIX = "TOUR VAGEN Biller";
    var BILLER_CREATE = "TOUR VAGEN Biller Create";
    var BILLER_EDIT = "TOUR VAGEN Biller Edit";
    var BILLER_DELETE = "TOUR VAGEN Biller Delete";
    var BILLER_CONFIRM = "TOUR VAGEN Biller Confirm";
    var BILLER_APPROVE = "TOUR VAGEN Biller Approve";
    var BILLER_REJECT = "TOUR VAGEN Biller Reject";
    var BILLER_RESTART = "TOUR VAGEN Biller Restart";
    var MERCHANT_PREFIX = "TOUR VAGEN Merchant";
    var MERCHANT_CREATE = "TOUR VAGEN Merchant Create";
    var USAGE_PREFIX = "TOUR VAGEN Usage";
    var USAGE_ALPHA = "TOUR VAGEN Usage Alpha";
    var USAGE_BETA = "TOUR VAGEN Usage Beta";
    var EXPORTER_PREFIX = "TOUR VAGEN Exporter";
    var EXPORTER_ALPHA = "TOUR VAGEN Exporter Alpha";
    var EXPORTER_BETA = "TOUR VAGEN Exporter Beta";

    // Shared navigation block for the edit and delete IK files -- it
    // corresponds to Flow 1 of both: "Open the Financial Accounting > Bank &
    // Cash > VA Generators menu."
    //
    // All three menu levels are clickable here: "Bank & Cash" is a level-2
    // section with children, which 14.0 renders as a .dropdown-toggle
    // carrying its own data-menu-xmlid (odoo-development-ui-test patterns.md
    // §A), unlike the level-3 grouping headers of the Configuration menus.
    function openVAGeneratorList() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Financial Accounting app",
                trigger:
                    '.o_app[data-menu-xmlid="ssi_financial_accounting.menu_root_financial_accounting"]',
            },
            {
                content: "Open the Bank & Cash menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_financial_accounting.menu_bank_cash"]',
            },
            {
                content: "Open the VA Generators menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_va.va_generator_menu"]',
            },
            {
                // Gate: wait for the TARGET action to be installed, not just
                // for "a list is on screen". Opening an app lands on its
                // first menu action, which is also a .o_list_view -- using
                // that as a gate would let the next steps act on the wrong
                // view (odoo-development-ui-test patterns.md §A).
                content: "Virtual Account Generators list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Virtual Account Generators)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ];
    }

    // Type into a many2one and pick an option from the autocomplete.
    // `typed` must be a strict prefix of `picked` -- see the comment on the
    // constants above.
    function selectMany2One(content, fieldName, typed, picked) {
        return [
            {
                content: content,
                trigger: ".o_field_widget[name='" + fieldName + "'] input",
                // Never touch a field before the form is actually rendered
                // editable (odoo-development-ui-test patterns.md §C). The
                // extra_trigger is not scoped to the dialog, so it matches
                // the wizard form of the create tour just as well as the
                // document form of the edit tour.
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text " + typed,
            },
            {
                // The autocomplete is appended to <body>, outside the modal,
                // so it must opt out of the modal scoping 14.0 applies to
                // every trigger while a dialog is displayed
                // (web_tour/tour_manager.js::_check_for_tooltip).
                content: "Pick " + picked + " from the dropdown",
                trigger: ".ui-autocomplete .ui-menu-item a:contains(" + picked + ")",
                in_modal: false,
            },
        ];
    }

    // Shared block for Flow 1 and Flow 2 of the four approval IK files
    // (04-confirm, 05-approve, 06-reject, 14-restart-approval): "Open the
    // Financial Accounting > Bank & Cash > VA Generators menu." followed
    // by "Open the record to <action>."
    //
    // As in the edit and delete tours, the row is identified by its
    // Biller. A va_generator keeps the document number "/" until it
    // reaches done (_create_sequence_state = "done"), so the number
    // column cannot tell two documents apart; setUpClass therefore gives
    // each document a Biller of its own.
    function openVAGeneratorRecord(billerName, action) {
        return [].concat(openVAGeneratorList(), [
            {
                content: "Open the record to " + action,
                trigger: ".o_data_row:contains(" + billerName + ") .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "The record form is displayed",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ]);
    }

    // Click a header button and acknowledge the dialog it raises.
    //
    // Both steps come from the Flow of the IK file being executed --
    // "Click the <X> button." and "Click OK on the confirmation dialog."
    // The dialog is not a tour-only detour: every approval button is
    // declared with a confirm="..." attribute in
    // ssi_transaction_confirm_mixin/templates/
    // mixin_transaction_confirm_templates.xml, so it always appears.
    function clickConfirmedButton(label, methodName) {
        return [
            {
                content: "Click the " + label + " button",
                trigger: ".o_statusbar_buttons button[name='" + methodName + "']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Click OK on the confirmation dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
        ];
    }

    // Post-Condition assertion shared by the confirm and the restart
    // approval IK files: approval records exist for the document's
    // approver levels.
    //
    // The approval_ids field is hidden while the document has no
    // approval record (attrs invisible in the multiple_approval template
    // of ssi_multiple_approval_mixin), so this assertion cannot pass
    // before the action under test actually ran -- it is a real gate,
    // not a selector that matches the previous screen as well.
    //
    // Opening the notebook page is a UI mechanic rather than a Flow
    // step. HOW MANY levels were created is a value fact and stays with
    // the unit tests (tests/test_data_va_generator.yaml).
    function assertApprovalRecords() {
        return [
            {
                content: "Open the Approvals tab",
                trigger: ".o_notebook .nav-link:contains(Approvals)",
            },
            {
                content: "The Approvals tab lists an approval record",
                trigger: ".o_field_widget[name='approval_ids'] .o_data_row",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ];
    }

    // Post-Condition assertion "Status changes to <label>." -- the
    // statusbar arrow of `stateValue` is the highlighted one.
    function assertStatus(label, stateValue) {
        return [
            {
                content: "Status is " + label,
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='" +
                    stateValue +
                    "'].btn-primary",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ];
    }

    // IK: docs/va_generator/01-create.md
    tour.register(
        "ssi_va_va_generator_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            [
                // ── Flow 1 — Open the Contacts menu.
                //
                // res.partner is the source model this IK uses, because the
                // Generate VA wizard binding is registered for it by default
                // (wizards/generate_va.xml). The Contacts app is entered
                // through its own app icon; the "Contacts" item below it is
                // the app's landing action.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Contacts app",
                    trigger: '.o_app[data-menu-xmlid="contacts.menu_contacts"]',
                },
                {
                    // Gate on the target action's title, not on a generic
                    // view class (odoo-development-ui-test patterns.md §A).
                    content: "Contacts action is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Contacts)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    // UI mechanic, not a Flow step: contacts.action_contacts
                    // opens in kanban, and 14.0 renders no row checkbox
                    // there. The checkbox Flow 2 asks for only exists in the
                    // list view.
                    content: "Switch to the list view",
                    trigger: "button.o_switch_view.o_list",
                },
                {
                    // The view switcher marks the active view with .active,
                    // which is the deterministic signal that the list is the
                    // one on screen now.
                    content: "The list view is displayed",
                    trigger: "button.o_switch_view.o_list.active",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    // UI mechanic, not a Flow step: res.partner holds far
                    // more records than a single list page, so the partner
                    // prepared by setUpClass is not reachable by scrolling.
                    // Searching is the mechanical means of "selecting the
                    // partner records", the same way the ir_model tour
                    // reaches its model record.
                    content: "Search for the partner to generate VA for",
                    trigger: ".o_searchview_input",
                    extra_trigger: ".o_list_view",
                    run: "text " + PARTNER,
                },
                {
                    content: "Validate the search",
                    trigger: ".o_searchview_autocomplete li.o_menu_item:first",
                },

                // ── Flow 2 — Select one or more partner records to generate
                // Virtual Accounts for (check the checkbox).
                {
                    content: "Select the partner record",
                    trigger:
                        ".o_data_row:contains(" +
                        PARTNER +
                        ") .o_list_record_selector input",
                    run: "click",
                },

                // ── Flow 3 — Click Action > Generate VA.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Generate VA",
                    trigger: ".o_cp_action_menus .o_menu_item a:contains(Generate VA)",
                },

                // ── Flow 4 — In the wizard that appears, fill in the fields.
                //
                // Every field of the wizard is filled, including the three
                // optional ones (Merchant, Bank Account Usage, Exporter), so
                // that the whole Flow step is proven usable. The Bank is
                // filled before Biller and Merchant on purpose: per the IK,
                // changing Bank clears both.
                {
                    content: "The Generate VA wizard is displayed",
                    trigger: ".o_field_widget[name='type_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ],
            selectMany2One(
                "Select the Generator Type",
                "type_id",
                TYPE_PREFIX,
                TYPE_ALPHA
            ),
            selectMany2One("Select the Bank", "bank_id", BANK_PREFIX, BANK_ALPHA),
            selectMany2One(
                "Select the Biller",
                "biller_id",
                BILLER_PREFIX,
                BILLER_CREATE
            ),
            selectMany2One(
                "Select the Merchant",
                "merchant_id",
                MERCHANT_PREFIX,
                MERCHANT_CREATE
            ),
            selectMany2One(
                "Select the Bank Account Usage",
                "usage_id",
                USAGE_PREFIX,
                USAGE_ALPHA
            ),
            selectMany2One(
                "Select the Exporter",
                "exporter_id",
                EXPORTER_PREFIX,
                EXPORTER_ALPHA
            ),
            [
                // ── Flow 5 — Click Generate VA.
                {
                    content: "Click the Generate VA button of the wizard",
                    trigger: ".modal-footer button:contains(Generate VA)",
                },

                // ── Post-Condition — A new va_generator document is created
                // and opened, in Draft status.
                //
                // While the wizard dialog is still on screen every trigger is
                // scoped inside it, so the statusbar of the document below
                // cannot match yet: this step is its own gate for the dialog
                // closing and the act_window landing.
                {
                    content: "The generated document is opened in Draft status",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },

                // ── Post-Condition — The Source Data tab is populated with
                // one line per selected source record.
                //
                // Only the presence of a line for the selected partner is
                // asserted. How many lines were created is a value fact,
                // which belongs to the unit tests
                // (tests/test_data_generate_va.yaml) rather than to a tour.
                {
                    content: "Open the Source Data tab",
                    trigger: ".o_notebook .nav-link:contains(Source Data)",
                },
                {
                    content: "The Source Data tab lists the selected partner",
                    trigger:
                        ".o_field_widget[name='source_data_ids'] " +
                        ".o_data_row:contains(" +
                        PARTNER +
                        ")",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },

                // The third Post-Condition bullet -- "the document number is
                // still /" -- is NOT asserted here. It is the value of the
                // name field, and reading field values is explicitly outside
                // the scope of a tour (odoo-development-ui-test, rule 2); the
                // sequence behaviour behind it is covered by the unit tests
                // in tests/test_data_va_generator.yaml.
            ]
        )
    );

    // IK: docs/va_generator/02-edit.md
    tour.register(
        "ssi_va_va_generator_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Financial Accounting > Bank & Cash > VA
            // Generators menu.
            openVAGeneratorList(),
            [
                // ── Flow 2 — Find and open the record to edit.
                //
                // The document number of every draft record is still "/", so
                // the row is identified by its Biller instead -- a column of
                // the va_generator tree view. The record is created by
                // setUpClass with a Biller of its own for exactly that
                // reason.
                {
                    content: "Open the record to edit",
                    trigger:
                        ".o_data_row:contains(" + BILLER_EDIT + ") .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "The record form is displayed",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    // 14.0 opens an existing record read-only, so the Edit
                    // button must be clicked before any field can be touched
                    // (odoo-development-ui-test patterns.md §E). This is a
                    // version mechanic of the 14.0 web client, not an extra
                    // Flow step: from 17.0 on the form is always editable.
                    content: "Click the Edit button",
                    trigger: ".o_form_button_edit",
                },
                {
                    content: "Form is now editable",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ],

            // ── Flow 3 — Change the required fields as needed.
            //
            // The record is in Draft, which is the state in which the IK
            // declares Generator Type, Bank, Biller, Merchant and Bank
            // Account Usage editable, and Exporter is editable there too.
            //
            // Three of them are changed here: Generator Type, Bank Account
            // Usage and Exporter. The Bank is deliberately NOT changed, and
            // that is a scope boundary rather than a skipped Flow step: the
            // only thing the Bank change produces on screen is the sub-bullet
            // effect "Biller and Merchant are cleared" -- i.e. two field
            // VALUES becoming empty, which odoo-development-ui-test rule 2
            // assigns to the unit tests. It is covered there, by the
            // "Changing bank_id on the form resets biller_id and merchant_id"
            // scenario of tests/test_data_va_generator.yaml.
            selectMany2One(
                "Change the Generator Type",
                "type_id",
                TYPE_PREFIX,
                TYPE_BETA
            ),
            selectMany2One(
                "Change the Bank Account Usage",
                "usage_id",
                USAGE_PREFIX,
                USAGE_BETA
            ),
            selectMany2One(
                "Change the Exporter",
                "exporter_id",
                EXPORTER_PREFIX,
                EXPORTER_BETA
            ),
            [
                // ── Flow 4 — The Source Data and Generated Bank Accounts
                // tabs cannot be edited from the form in any state.
                //
                // What the user sees of that is the absence of the "Add a
                // line" row, which the inner trees suppress with create="0".
                // The form is in edit mode at this point, so the assertion is
                // made in the state where the row would otherwise appear.
                {
                    content: "Open the Source Data tab",
                    trigger: ".o_notebook .nav-link:contains(Source Data)",
                },
                {
                    content: "The Source Data tab offers no Add a line row",
                    trigger:
                        ".o_field_widget[name='source_data_ids']" +
                        ":not(:has(.o_field_x2many_list_row_add))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    content: "Open the Generated Bank Accounts tab",
                    trigger: ".o_notebook .nav-link:contains(Generated Bank Accounts)",
                },
                {
                    content: "The Generated Bank Accounts tab offers no Add a line row",
                    trigger:
                        ".o_field_widget[name='bank_account_ids']" +
                        ":not(:has(.o_field_x2many_list_row_add))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },

                // ── Flow 5 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // ── Post-Condition — The record is updated with the new
                // values. The stored values themselves are unit test
                // territory; what is visible to the user is the form leaving
                // edit mode once the write landed.
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/va_generator/03-delete.md
    tour.register(
        "ssi_va_va_generator_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Financial Accounting > Bank & Cash > VA
            // Generators menu.
            openVAGeneratorList(),
            [
                // ── Flow 2 — Select one or more records to delete (check the
                // checkbox).
                //
                // As in the edit tour, the row is identified by its Biller:
                // the document number of a draft record is still "/", which
                // is the Pre-Condition this IK requires and which every draft
                // row shares.
                {
                    content: "Select the record to delete",
                    trigger:
                        ".o_data_row:contains(" +
                        BILLER_DELETE +
                        ") .o_list_record_selector input",
                    run: "click",
                },

                // ── Flow 3 — Click Action > Delete.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Delete",
                    // The Action menu items are Owl components; match the
                    // EXACT label instead of :contains(Delete), which could
                    // pick a different item as a substring
                    // (odoo-development-ui-test patterns.md §I).
                    trigger: ".o_cp_action_menus .o_menu_item a",
                    run: function () {
                        var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                            function () {
                                return $(this).text().trim() === "Delete";
                            }
                        );
                        $delete[0].click();
                    },
                },

                // ── Flow 4 — Click OK to confirm.
                {
                    content: "Confirm deletion",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — The selected records are permanently
                // removed from the system, so the row is gone from the list.
                {
                    content: "Record no longer appears in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(" +
                        BILLER_DELETE +
                        ")))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/va_generator/04-confirm.md
    tour.register(
        "ssi_va_va_generator_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Financial Accounting > Bank & Cash > VA
            // Generators menu.
            // ── Flow 2 — Open the record to confirm.
            openVAGeneratorRecord(BILLER_CONFIRM, "confirm"),

            // ── Flow 3 — Click the Confirm button.
            // ── Flow 4 — Click OK on the confirmation dialog.
            clickConfirmedButton("Confirm", "action_confirm"),

            // ── Post-Condition — Status changes to Waiting for Approval.
            assertStatus("Waiting for Approval", "confirm"),

            // ── Post-Condition — Approval records are created for each
            // approver level defined by the matching approval template.
            assertApprovalRecords()

            // The trailing paragraph of the IK -- the four Pre-Condition
            // checks that block Confirm with an error message when they
            // are not met -- is deliberately NOT covered here. Those are
            // negative paths ending in a UserError, which
            // odoo-development-ui-test assigns to the unit tests; they
            // are covered by the "Confirm ... raises" scenarios of
            // tests/test_data_va_generator.yaml.
        )
    );

    // IK: docs/va_generator/05-approve.md
    tour.register(
        "ssi_va_va_generator_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Financial Accounting > Bank & Cash > VA
            // Generators menu.
            // ── Flow 2 — Open the record to approve.
            openVAGeneratorRecord(BILLER_APPROVE, "approve"),

            // ── Flow 3 — Click the Approve button.
            // ── Flow 4 — Click OK on the confirmation dialog.
            clickConfirmedButton("Approve", "action_approve_approval"),

            // ── Post-Condition — the second branch of it. The approval
            // template shipped with the module (approval_template/
            // va_generator.xml) defines a single approver level, so this
            // approval IS the last pending one and the document
            // transitions to Done on its own -- there is no Done button
            // for this model. The first branch ("status remains Waiting
            // for Approval and the next level becomes pending") needs a
            // multi-level template, which no IK file describes.
            //
            // The two sub-bullets of that Post-Condition -- the document
            // number being issued and the Generated Bank Accounts tab
            // being populated -- are not asserted here: the issued number
            // and the generated Virtual Account records are values, and
            // the Keputusan Desain of this item keeps them with the unit
            // tests (tests/test_data_va_generator.yaml).
            assertStatus("Done", "done")
        )
    );

    // IK: docs/va_generator/06-reject.md
    tour.register(
        "ssi_va_va_generator_reject",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Financial Accounting > Bank & Cash > VA
            // Generators menu.
            // ── Flow 2 — Open the record to reject.
            openVAGeneratorRecord(BILLER_REJECT, "reject"),

            // ── Flow 3 — Click the Reject button.
            // ── Flow 4 — Click OK on the confirmation dialog.
            clickConfirmedButton("Reject", "action_reject_approval"),

            // ── Post-Condition — Status changes to Rejected.
            //
            // "reject" is not part of _statusbar_visible_label
            // ("draft,confirm,done"), but the web client always keeps the
            // CURRENT value in the statusbar (FieldStatus._setState in
            // web/static/src/js/fields/relational_fields.js), so the
            // arrow is on screen once the document reaches it.
            assertStatus("Rejected", "reject"),
            [
                // ── Post-Condition — A notification is posted on the
                // document's chatter.
                //
                // Only the presence of the message is asserted, not its
                // wording beyond the word the mixin composes it around
                // (_prepare_reject_action_notification).
                {
                    content: "The rejection notification is posted on the chatter",
                    trigger: ".o_Message_content:contains(rejected)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/va_generator/14-restart-approval.md
    tour.register(
        "ssi_va_va_generator_restart_approval",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Financial Accounting > Bank & Cash > VA
            // Generators menu.
            // ── Flow 2 — Open the record whose approval process is stuck.
            openVAGeneratorRecord(BILLER_RESTART, "restart the approval process of"),

            // ── Flow 3 — Click the Restart Approval Process button.
            // ── Flow 4 — Click OK on the confirmation dialog.
            //
            // The button only shows while the document has no approval
            // template resolved, which is the second Pre-Condition of
            // this IK; setUpClass puts the document in exactly that
            // state.
            clickConfirmedButton(
                "Restart Approval Process",
                "action_reload_approval_template"
            ),

            // ── Post-Condition — the branch where a matching
            // approval.template IS found: fresh approval records are
            // created for its approver levels, starting the approval
            // process from the first level. The module ships a template
            // matching every va_generator document
            // (approval_template/va_generator.xml), so this is the branch
            // the tour walks. The other branch ("still no template
            // matches") would need the module's own template removed,
            // which no IK file describes.
            assertApprovalRecords(),

            // ── Post-Condition — Status remains Waiting for Approval;
            // this action never changes the document's state.
            assertStatus("Waiting for Approval", "confirm")
        )
    );
});
