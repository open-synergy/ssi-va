// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_va.va_generator_exporter_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block reused by every tour below -- it corresponds to
    // Flow 1 of every va_generator_exporter IK: "Open the Financial Accounting
    // > Configuration > Virtual Account > Generator Exporters menu."
    //
    // The IK menu path has four levels but only three are clickable: the
    // "Virtual Account" level is a <menuitem> without an action that has
    // children (see menu.xml), so 14.0 renders it as a .dropdown-header with
    // no data-menu-xmlid and its children are flattened into the same
    // dropdown (odoo-development-ui-test patterns.md §A). There is therefore
    // no step for it.
    function openVAGeneratorExporterList() {
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
                content: "Open the Generator Exporters menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_va.va_generator_exporter_menu"]',
            },
            {
                // Gate: wait for the TARGET action to be installed, not just
                // for "a list is on screen". Opening an app lands on its first
                // menu action, which is also a .o_list_view -- using that as a
                // gate would let the next steps act on the wrong view
                // (odoo-development-ui-test patterns.md §A).
                content: "Virtual Account Generator Exporters list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Virtual Account Generator Exporters)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Flow step "On the Export Configuration tab, fill in Format and CSV
    // Delimiter". CSV is picked on purpose: the IK describes CSV Delimiter as
    // applying only when Format is CSV (the field is hidden for XLSX), so
    // choosing CSV is the only branch in which both fields of the step are
    // reachable.
    function fillExportConfigurationTab(delimiter) {
        return [
            {
                content: "Open the Export Configuration tab",
                trigger: ".o_notebook .nav-link:contains(Export Configuration)",
            },
            {
                // 14.0 renders a selection field as a <select> that carries
                // .o_field_widget ITSELF; the descendant form
                // ".o_field_widget[name='format'] select" would look for a
                // <select> inside a <select> and time out
                // (odoo-development-ui-test patterns.md §Field selection).
                content: "Set the Format to CSV",
                trigger: "select.o_field_widget[name='format']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text CSV",
            },
            {
                // The field carries attrs invisible for a non-CSV format, so
                // the tour reaching it at all is the visible proof that the
                // Format change was applied -- no value is asserted.
                content: "Fill in the CSV Delimiter",
                trigger: ".o_field_widget[name='csv_delimiter']",
                run: "text " + delimiter,
            },
        ];
    }

    // Flow step "On the Python Code tab, review/edit the Python Code field".
    // Only the review half is walked: the field uses widget="ace", whose value
    // lives inside an Ace editor instance rather than in a DOM input, and its
    // content is a value fact that belongs to the unit tests. Per the issue
    // Design Decision the tour neither runs nor inspects the exporter Python
    // code -- it only proves the tab and the field render.
    function openPythonCodeTab() {
        return [
            {
                content: "Open the Python Code tab",
                trigger: ".o_notebook .nav-link:contains(Python Code)",
            },
            {
                content: "Python Code field is displayed",
                trigger: ".o_field_widget[name='python_code']",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // IK: docs/va_generator_exporter/01-create.md
    tour.register(
        "ssi_va_va_generator_exporter_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Financial Accounting > Configuration >
            // Virtual Account > Generator Exporters menu.
            openVAGeneratorExporterList(),
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
                // is entered as "/" -- the branch the IK spells out ("enter /
                // to leave it blank for now and assign it later with the
                // Generate Code button") -- so that Flow 4 actually assigns a
                // value: the button only replaces a code that is still "/".
                {
                    content: "Fill in Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR VA EXPORTER Create",
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
                    // (odoo-development-ui-test patterns.md §P). Without this
                    // gate the reload would silently discard the Export
                    // Configuration edits of Flow 5. The generated Code value
                    // itself is not asserted -- that is a value check, which
                    // belongs to the unit tests.
                    content: "Record is saved by Generate Code",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:not(:contains(New))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ],

            // ── Flow 5 — On the Export Configuration tab, fill in Format and
            // CSV Delimiter.
            fillExportConfigurationTab(";"),

            // ── Flow 6 — On the Python Code tab, review the Python Code
            // field.
            openPythonCodeTab(),

            [
                // ── Flow 7 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // ── Post-Condition — A new Virtual Account Generator Exporter
                // record is created and appears in the Generator Exporters
                // list, and the Code now holds a value from the sequence
                // template. Only what is visible is asserted here: that the
                // record left edit mode and is displayed. The generated Code
                // value itself is a value fact and belongs to the unit tests.
                {
                    content: "Record is saved and displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR VA EXPORTER Create)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/va_generator_exporter/02-edit.md
    tour.register(
        "ssi_va_va_generator_exporter_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Generator Exporters menu.
            openVAGeneratorExporterList(),
            [
                // ── Flow 2 — Find and open the record to edit.
                {
                    content: "Open the generator exporter record",
                    trigger:
                        ".o_data_row:contains(TOUR VA EXPORTER Edit) .o_data_cell:first",
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

                // ── Flow 3 — Click Generate Code in the header. The record
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
                    // button (odoo-development-ui-test patterns.md §P).
                    // Without it the reload would wipe the Export
                    // Configuration edits of Flow 4.
                    //
                    // The record already exists here, so the "New" breadcrumb
                    // trick of the create tour would be a false gate, and this
                    // IK -- unlike the create one -- never renames the record,
                    // so the breadcrumb text never changes either. What DOES
                    // change is the Code input, which setUpClass guarantees
                    // starts as "/" and which only the sequence template it
                    // installs can turn into a TOURSEQVAGE* value. This is a
                    // synchronisation gate on a token guaranteed by
                    // setUpClass, which is what §P prescribes -- not an
                    // assertion that the generated code is correct; that
                    // remains unit test territory. :propValueContains is
                    // needed because in edit mode Code is an <input>, whose
                    // value is a DOM property that :contains cannot see.
                    content: "Record is saved by Generate Code",
                    trigger:
                        ".o_field_widget[name='code']:propValueContains(TOURSEQVAGE)",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ],

            // ── Flow 4 — On the Export Configuration tab, change Format
            // and/or CSV Delimiter.
            fillExportConfigurationTab("|"),

            // ── Flow 5 — On the Python Code tab, edit the Python Code field.
            openPythonCodeTab(),

            [
                // ── Flow 6 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },

                // ── Post-Condition — The record is updated with the new
                // values and its Code holds a value from the sequence
                // template. The stored field values themselves are unit test
                // territory, so only the visible outcome is asserted: the
                // record left edit mode and is still displayed.
                {
                    content: "Record is saved",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(TOUR VA EXPORTER Edit)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/va_generator_exporter/03-delete.md
    tour.register(
        "ssi_va_va_generator_exporter_delete",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Generator Exporters menu.
            openVAGeneratorExporterList(),
            [
                // ── Flow 2 — Select the record to delete (checkbox).
                {
                    content: "Select the record to delete",
                    trigger:
                        ".o_data_row:contains(TOUR VA EXPORTER Delete) " +
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
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR VA EXPORTER Delete)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/va_generator_exporter/04-deactivate.md
    tour.register(
        "ssi_va_va_generator_exporter_deactivate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Generator Exporters menu.
            openVAGeneratorExporterList(),
            [
                // ── Flow 2 — Select the record to deactivate (checkbox).
                {
                    content: "Select the record to deactivate",
                    trigger:
                        ".o_data_row:contains(TOUR VA EXPORTER Deactivate) " +
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
                // the IK Post-Condition (an archived export layout can no
                // longer be picked as the exporter of a Virtual Account
                // generation document, while existing data keeps referencing
                // it) are not visible facts of this screen and belong to the
                // unit tests.
                {
                    content: "Record no longer appears in the active list",
                    trigger:
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR VA EXPORTER Deactivate)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );

    // IK: docs/va_generator_exporter/05-activate.md
    tour.register(
        "ssi_va_va_generator_exporter_activate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // ── Flow 1 — Open the Generator Exporters menu.
            openVAGeneratorExporterList(),
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
                        ".o_data_row:contains(TOUR VA EXPORTER Activate) " +
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
                        ".o_list_view:not(:has(.o_data_row:contains(TOUR VA EXPORTER Activate)))",
                    run: function () {
                        // Assertion only; do not trigger the default click
                        // action.
                    },
                },
            ]
        )
    );
});
