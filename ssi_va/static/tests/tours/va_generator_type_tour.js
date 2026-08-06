// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_va.va_generator_type_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- it corresponds to
    // Flow 1 of every va_generator_type IK: "Open the Financial Accounting >
    // Configuration > Virtual Account > Generator Types menu."
    //
    // The IK menu path has four levels but only three are clickable: the
    // "Virtual Account" level is a <menuitem> without an action that has
    // children (see menu.xml), so 14.0 renders it as a .dropdown-header with
    // no data-menu-xmlid and its children are flattened into the same
    // dropdown (odoo-development-ui-test patterns.md §A). There is therefore
    // no step for it.
    function openVAGeneratorTypeList() {
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
                content: "Open the Generator Types menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_va.va_generator_type_menu"]',
            },
            {
                // Gate: wait for the TARGET action to be installed, not just
                // for "a list is on screen". Opening an app lands on its first
                // menu action, which is also a .o_list_view -- using that as a
                // gate would let the next steps act on the wrong view
                // (odoo-development-ui-test patterns.md §A).
                content: "Virtual Account Generator Types list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Virtual Account Generator Types)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Click the notebook tab whose label is EXACTLY "Python Code".
    // ":contains(Python Code)" alone would also match the "Partner Resolution
    // Python Code" tab, whose label carries the same substring
    // (odoo-development-ui-test patterns.md §I).
    function openPythonCodeTab() {
        return [
            {
                content: "Open the Python Code tab",
                trigger: ".o_notebook .nav-link:contains(Python Code)",
                run: function () {
                    var $tab = $(".o_notebook .nav-link").filter(function () {
                        return $(this).text().trim() === "Python Code";
                    });
                    $tab[0].click();
                },
            },
            {
                // The IK step is "review/edit the Python Code field". Only the
                // review half is walked here: per the issue Design Decision
                // the tour neither runs nor inspects the generator type Python
                // code, it only proves the Python Code tab renders. The field
                // uses widget="ace", whose value lives in an Ace editor
                // instance rather than in a DOM input, and its content is a
                // value fact that belongs to the unit tests.
                content: "Python Code field is displayed",
                trigger: ".o_field_widget[name='python_code']",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Same as above for the "Partner Resolution Python Code" tab. Its label is
    // unique, so a plain :contains is enough here.
    function openPartnerPythonCodeTab() {
        return [
            {
                content: "Open the Partner Resolution Python Code tab",
                trigger:
                    ".o_notebook .nav-link:contains(Partner Resolution Python Code)",
            },
            {
                // Review-only, for the same reason as the Python Code tab
                // above.
                content: "Partner Resolution Python Code field is displayed",
                trigger: ".o_field_widget[name='partner_python_code']",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/va_generator_type/01-create.md
    tour.register(
        "ssi_va_va_generator_type_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Financial Accounting > Configuration >
            // Virtual Account > Generator Types menu.
            openVAGeneratorTypeList(),
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
                // is left as "/" so that the Generate Code button of Flow 5
                // actually assigns a value: the button only replaces a code
                // that is still "/".
                {
                    content: "Fill in Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR VA GENTYPE Create",
                },
                {
                    content: "Fill in Code",
                    trigger: ".o_field_widget[name='code']",
                    run: "text /",
                },

                // ── Flow 4 — Optionally, fill in the Restrict to Model field.
                // The option is exercised here so the field is proven usable.
                {
                    content: "Select the Restrict to Model value",
                    trigger: ".o_field_widget[name='model_id'] input",
                    run: "text Virtual Account Generator",
                },
                {
                    // Match the full model name. The typed text is shorter on
                    // purpose: the "Create ..." entry of the dropdown carries
                    // the typed text verbatim, so matching on it would risk
                    // picking the quick-create entry instead of the record.
                    content: "Pick the model from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item " +
                        "a:contains(Virtual Account Generator Type)",
                    in_modal: false,
                },

                // ── Flow 5 — Click Generate Code in the header. This is an
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
            ],

            // ── Flow 6 — On the Python Code tab, review the Python Code
            // field.
            openPythonCodeTab(),

            // ── Flow 7 — On the Partner Resolution Python Code tab, review
            // the Partner Resolution Python Code field.
            openPartnerPythonCodeTab(),

            [
                // ── Flow 8 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // ── Post-Condition — A new Virtual Account Generator Type
                // record is created and appears in the Generator Types list,
                // and the Code now holds a value coming from the sequence
                // template. Only what is visible is asserted here: that the
                // record is saved and displayed. The generated Code value
                // itself is a value fact and belongs to the unit tests.
                {
                    content: "Record is saved and displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR VA GENTYPE Create)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/va_generator_type/02-edit.md
    tour.register(
        "ssi_va_va_generator_type_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Generator Types menu.
            openVAGeneratorTypeList(),
            [
                // ── Flow 2 — Find and open the record to edit.
                {
                    content: "Open the generator type record",
                    trigger:
                        ".o_data_row:contains(TOUR VA GENTYPE Edit) .o_data_cell:first",
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

                // ── Flow 3 — Change the required fields, including the
                // Restrict to Model field.
                {
                    content: "Change the Name",
                    trigger: ".o_field_widget[name='name']",
                    run: "text TOUR VA GENTYPE Edit Changed",
                },
                {
                    content: "Change the Restrict to Model value",
                    trigger: ".o_field_widget[name='model_id'] input",
                    run: "text Virtual Account Generator",
                },
                {
                    // Same shorter-typed-text rule as in the create tour.
                    content: "Pick the model from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item " +
                        "a:contains(Virtual Account Generator Type)",
                    in_modal: false,
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
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR VA GENTYPE Edit Changed)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ],

            // ── Flow 5 — On the Python Code tab, edit the Python Code field.
            openPythonCodeTab(),

            // ── Flow 6 — On the Partner Resolution Python Code tab, edit the
            // Partner Resolution Python Code field.
            openPartnerPythonCodeTab(),

            [
                // ── Flow 7 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // ── Post-Condition — The record is updated with the new
                // values and its Code holds a value from the sequence
                // template. The stored field values themselves are unit test
                // territory, so only the visible outcome is asserted: the
                // record left edit mode and is displayed under its new name.
                {
                    content: "Record is saved",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR VA GENTYPE Edit Changed)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/va_generator_type/03-delete.md
    tour.register(
        "ssi_va_va_generator_type_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Generator Types menu.
            openVAGeneratorTypeList(),
            [
                // ── Flow 2 — Select the record to delete (checkbox).
                {
                    content: "Select the record to delete",
                    trigger:
                        ".o_data_row:contains(TOUR VA GENTYPE Delete) " +
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
                // removed and no longer appears in the list.
                {
                    content: "Record no longer appears in the list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR VA GENTYPE Delete)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/va_generator_type/04-deactivate.md
    tour.register(
        "ssi_va_va_generator_type_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Generator Types menu.
            openVAGeneratorTypeList(),
            [
                // ── Flow 2 — Select the record to deactivate (checkbox).
                {
                    content: "Select the record to deactivate",
                    trigger:
                        ".o_data_row:contains(TOUR VA GENTYPE Deactivate) " +
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
                // the IK Post-Condition (an archived generator type can no
                // longer be picked when generating Virtual Accounts, while
                // existing data keeps referencing it) are not visible facts of
                // this screen and belong to the unit tests.
                {
                    content: "Record no longer appears in the active list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR VA GENTYPE Deactivate)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/va_generator_type/05-activate.md
    tour.register(
        "ssi_va_va_generator_type_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Generator Types menu.
            openVAGeneratorTypeList(),
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
                        ".o_data_row:contains(TOUR VA GENTYPE Activate) " +
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

                // ── Flow 5 (IK text) — "Click OK to confirm." There is no
                // step for it because 14.0 shows no dialog for Unarchive:
                // in web/static/src/js/views/list/list_controller.js
                // (_getActionMenuItems) only "Archive" wraps its callback in
                // Dialog.confirm(...), while "Unarchive" calls
                // _toggleArchiveState(false) straight away. Adding a dialog
                // step here would hang the tour on a modal that never opens.
                // This is an inaccuracy in
                // docs/va_generator_type/05-activate.md; changing IK files is
                // explicitly out of scope for this change, so it is reported
                // on the IK issue instead of being patched here.

                // ── Post-Condition — The record is restored and belongs to
                // the default (active) list again. With the Archived filter
                // still on -- turning it off is not a step of this IK -- the
                // visible proof is that the row leaves the archived-only
                // list, which can only happen once its Active flag is back
                // to true.
                {
                    content: "Record leaves the archived list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR VA GENTYPE Activate)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );
});
