// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_va.va_biller_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- it corresponds to
    // Flow 1 of every va_biller IK: "Open the Financial Accounting >
    // Configuration > Virtual Account > Billers menu."
    //
    // The IK menu path has four levels but only three are clickable: the
    // "Virtual Account" level is a <menuitem> without an action that has
    // children, so 14.0 renders it as a .dropdown-header with no
    // data-menu-xmlid and its children are flattened into the same dropdown
    // (odoo-development-ui-test patterns.md §A). There is therefore no step
    // for it.
    function openVABillerList() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Financial Accounting app",
                trigger:
                    '.o_app[data-menu-xmlid="ssi_financial_accounting.menu_root_financial_accounting"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_financial_accounting.menu_financial_accounting_configuration"]',
            },
            {
                content: "Open the Billers menu",
                trigger: '.o_menu_sections [data-menu-xmlid="ssi_va.va_biller_menu"]',
            },
            {
                // Gate: wait for the TARGET action to be installed, not just
                // for "a list is on screen". Opening an app lands on its first
                // menu action, which is also a .o_list_view -- using that as a
                // gate would let the next steps act on the wrong view
                // (odoo-development-ui-test patterns.md §A).
                content: "Virtual Account Billers list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Virtual Account Billers)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/va_biller/01-create.md
    tour.register(
        "ssi_va_va_biller_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Financial Accounting > Configuration >
            // Virtual Account > Billers menu.
            openVABillerList(),
            [
                // ── Flow 2 — Click the Create button.
                {
                    content: "Click Create",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },

                // ── Flow 3 — Fill in the required fields (Name, Code). Code
                // is left as "/" so that the Generate Code button of Flow 4
                // actually assigns a value: the button only replaces a code
                // that is still "/".
                {
                    content: "Fill in Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR VA BILLER Create",
                },
                {
                    content: "Fill in Code",
                    trigger: ".o_field_widget[name='code']",
                    run: "text /",
                },

                // ── Flow 4 — Click Generate Code in the header. This is an
                // inline action of this IK (metadata "Inline Actions:
                // action_generate_code"), so it is a step here instead of a
                // tour of its own.
                {
                    content: "Click Generate Code",
                    trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    // The record has no id until this button auto-saves it, so
                    // the breadcrumb literal "New" going away is the
                    // data-independent proof that the save + reload completed
                    // (odoo-development-ui-test patterns.md §P). The generated
                    // Code value itself is not asserted -- that is a value
                    // check, which belongs to the unit tests.
                    content: "Record is saved by Generate Code",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:not(:contains(New))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },

                // ── Flow 5 — On the Bank Codes tab, add a line with Bank and
                // Biller Code. One line is enough: the IK repeats the same
                // three clicks for every extra bank.
                {
                    content: "Open the Bank Codes tab",
                    trigger: ".o_notebook .nav-link:contains(Bank Codes)",
                },
                {
                    content: "Add a line",
                    trigger:
                        ".o_field_widget[name='bank_code_ids'] " +
                        ".o_field_x2many_list_row_add a",
                },
                {
                    content: "Select the Bank",
                    trigger: ".o_selected_row .o_field_widget[name='bank_id'] input",
                    run: "text TOUR VA BILLER BANK",
                },
                {
                    content: "Pick the bank from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR VA BILLER BANK)",
                    in_modal: false,
                },
                {
                    content: "Fill in the Biller Code",
                    trigger: ".o_selected_row .o_field_widget[name='biller_code']",
                    run: "text TOURBCCREATE01",
                },
                {
                    // Commit the last edited cell before saving. Never
                    // `press Tab`: on an editable="bottom" list it opens a new
                    // empty row and leaves the form dirty
                    // (odoo-development-ui-test patterns.md §C). The <td> of an
                    // o2m cell carries no `name` attribute in 14.0, so the blur
                    // is done by clicking the always-visible Name field above
                    // the notebook -- a plain click does not change its text.
                    content: "Commit the bank code line",
                    trigger: ".o_field_widget[name='name']",
                    run: function () {
                        this.$anchor[0].click();
                    },
                },

                // ── Flow 6 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // ── Post-Condition — A new Virtual Account Biller record is
                // created; the Code now holds a generated value and the bank
                // code line is attached to it. Only what is visible is
                // asserted here: that the record is saved and displayed, and
                // that the bank code line is rendered on its tab. The
                // generated Code value and the existence of the underlying
                // va_biller.code row are value/database facts and belong to
                // the unit tests.
                {
                    content: "Record is saved and displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR VA BILLER Create)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    content: "Bank code line is shown on the Bank Codes tab",
                    trigger:
                        ".o_field_widget[name='bank_code_ids'] " +
                        ".o_data_row:contains(TOURBCCREATE01)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/va_biller/02-edit.md
    tour.register(
        "ssi_va_va_biller_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Billers menu.
            openVABillerList(),
            [
                // ── Flow 2 — Find and open the record to edit.
                {
                    content: "Open the biller record",
                    trigger:
                        ".o_data_row:contains(TOUR VA BILLER Edit) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open",
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

                // ── Flow 3 — Change the required fields.
                {
                    content: "Change the Name",
                    trigger: ".o_field_widget[name='name']",
                    run: "text TOUR VA BILLER Edit Changed",
                },

                // ── Flow 4 — Click Generate Code in the header. The record
                // was created with Code "/" by setUpClass, which is exactly
                // the state the IK describes ("only applies when Code is
                // still /").
                {
                    content: "Click Generate Code",
                    trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    // Gate for the auto-save + reload triggered by the object
                    // button (odoo-development-ui-test patterns.md §P). The
                    // record already exists here, so the "New" breadcrumb
                    // trick of the create tour would be a false gate; the
                    // breadcrumb carrying the NEW name instead is impossible
                    // before the save landed, because the title is read from
                    // display_name, which is only refreshed by the reload.
                    content: "Record is saved by Generate Code",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR VA BILLER Edit Changed)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },

                // ── Flow 5 — On the Bank Codes tab, add a line.
                {
                    content: "Open the Bank Codes tab",
                    trigger: ".o_notebook .nav-link:contains(Bank Codes)",
                },
                {
                    content: "Add a line",
                    trigger:
                        ".o_field_widget[name='bank_code_ids'] " +
                        ".o_field_x2many_list_row_add a",
                },
                {
                    content: "Select the Bank",
                    trigger: ".o_selected_row .o_field_widget[name='bank_id'] input",
                    run: "text TOUR VA BILLER BANK",
                },
                {
                    content: "Pick the bank from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR VA BILLER BANK)",
                    in_modal: false,
                },
                {
                    content: "Fill in the Biller Code",
                    trigger: ".o_selected_row .o_field_widget[name='biller_code']",
                    run: "text TOURBCEDIT01",
                },
                {
                    // Same blur-instead-of-Tab rule as in the create tour.
                    content: "Commit the bank code line",
                    trigger: ".o_field_widget[name='name']",
                    run: function () {
                        this.$anchor[0].click();
                    },
                },

                // ── Flow 6 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // ── Post-Condition — The record is updated with the new
                // values and the bank code line is reflected on the tab. The
                // stored field values themselves are unit test territory.
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
                {
                    content: "Bank code line is shown on the Bank Codes tab",
                    trigger:
                        ".o_field_widget[name='bank_code_ids'] " +
                        ".o_data_row:contains(TOURBCEDIT01)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/va_biller/03-delete.md
    tour.register(
        "ssi_va_va_biller_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Billers menu.
            openVABillerList(),
            [
                // ── Flow 2 — Select the record to delete (checkbox).
                {
                    content: "Select the record to delete",
                    trigger:
                        ".o_data_row:contains(TOUR VA BILLER Delete) " +
                        ".o_list_record_selector input",
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

                // ── Post-Condition — The selected record is permanently
                // removed and no longer appears in the list. That its Bank
                // Codes lines are removed together with it is a database
                // fact, verified by the unit tests, not by the tour.
                {
                    content: "Record no longer appears in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR VA BILLER Delete)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/va_biller/04-deactivate.md
    tour.register(
        "ssi_va_va_biller_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Billers menu.
            openVABillerList(),
            [
                // ── Flow 2 — Select the record to deactivate (checkbox).
                {
                    content: "Select the record to deactivate",
                    trigger:
                        ".o_data_row:contains(TOUR VA BILLER Deactivate) " +
                        ".o_list_record_selector input",
                    run: "click",
                },

                // ── Flow 3 — Click Action > Archive.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Archive",
                    trigger: ".o_cp_action_menus .o_menu_item a",
                    run: function () {
                        var $archive = $(".o_cp_action_menus .o_menu_item a").filter(
                            function () {
                                return $(this).text().trim() === "Archive";
                            }
                        );
                        $archive[0].click();
                    },
                },

                // ── Flow 4 — Click OK to confirm.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // ── Post-Condition — The record is archived and no longer
                // appears in the default list view. The other two bullets of
                // the IK Post-Condition (an archived biller can no longer be
                // picked when generating Virtual Accounts, while existing
                // data keeps referencing it) are not visible facts of this
                // screen and belong to the unit tests.
                {
                    content: "Record no longer appears in the active list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR VA BILLER Deactivate)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/va_biller/05-activate.md
    tour.register(
        "ssi_va_va_biller_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Billers menu.
            openVABillerList(),
            [
                // ── Flow 2 — Enable the Archived filter in the search bar.
                {
                    content: "Open the Filters menu",
                    // 14.0: the Filters dropdown is an Owl component whose
                    // open state does not always flip on the synthetic mouse
                    // event sequence -- use a real browser click
                    // (odoo-development-ui-test patterns.md §I/§J).
                    trigger: ".o_filter_menu .o_dropdown_toggler_btn",
                    run: function () {
                        this.$anchor[0].click();
                    },
                },
                {
                    content: "Enable the Archived filter",
                    trigger: ".o_filter_menu .o_menu_item a:contains(Archived)",
                    run: function () {
                        this.$anchor[0].click();
                    },
                },

                // ── Flow 3 — Select the record to reactivate (checkbox).
                {
                    content: "Select the record to reactivate",
                    trigger:
                        ".o_data_row:contains(TOUR VA BILLER Activate) " +
                        ".o_list_record_selector input",
                    run: "click",
                },

                // ── Flow 4 — Click Action > Unarchive.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Unarchive",
                    trigger: ".o_cp_action_menus .o_menu_item a",
                    run: function () {
                        var $unarchive = $(".o_cp_action_menus .o_menu_item a").filter(
                            function () {
                                return $(this).text().trim() === "Unarchive";
                            }
                        );
                        $unarchive[0].click();
                    },
                },

                // ── Post-Condition — The record is restored and belongs to
                // the default (active) list again. With the Archived filter
                // still on -- turning it off is not a step of this IK -- the
                // visible proof is that the row leaves the archived-only
                // list, which can only happen once its Active flag is back
                // to true.
                {
                    content: "Record leaves the archived list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR VA BILLER Activate)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );
});
