// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_va_operating_unit.va_generator_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Created by tests/test_ui_va_generator.py. The names are the
    // "glue" between the Python Pre-Condition data and the UI steps:
    // they are typed into an input and matched on a list row or an
    // autocomplete dropdown entry.
    var PARTNER = "TOUR VAGENOU Partner";
    var BILLER_EDIT = "TOUR VAGENOU Biller Edit";
    var OPERATING_UNIT = "TOUR VAGENOU Operating Unit";

    // IK: docs/va_generator/01-create.md
    //
    // THIS IS A DELTA-ONLY TOUR (odoo-development-ui-test patterns.md §O).
    // ssi_va_operating_unit is an extension module and its IK file is a
    // delta IK: it carries no Flow of its own, only an "Additional Fields"
    // section on top of the Flow of ssi_va's own
    // docs/va_generator/01-create.md. The navigation below is therefore
    // taken from the base Flow (Flow 1 to Flow 3 of that file), and the
    // only thing this tour adds is the assertion that the Operating Unit
    // field is rendered in the Generate VA wizard.
    //
    // THREE DELIBERATE BOUNDARIES, stated here rather than silently
    // skipped:
    //
    // 1. Flow 4 ("fill in the fields") and Flow 5 ("Click Generate VA") of
    //    the base IK are NOT walked. The item's Keputusan Desain scopes
    //    this tour to "assertion bahwa field Operating Unit ter-render di
    //    wizard", and patterns.md §O forbids a delta tour from continuing
    //    into the state actions of the base IK. Creating the document
    //    itself is already covered by ssi_va's own create tour
    //    (ssi_va_va_generator_create).
    // 2. The "Additional Fields" section of the delta IK states that the
    //    field appears on the va_generator document form as well as on the
    //    wizard. Only the wizard half is asserted here, because that is
    //    the half the Keputusan Desain names. The document-form half has
    //    no tour of its own: the delta IK docs/va_generator/02-edit.md is
    //    outside the "### UI Test (tour)" list of the backlog item, which
    //    excludes it explicitly.
    // 3. The "Modified -- Record Visibility" section of the delta IK
    //    produces no step here. The Keputusan Desain of the item rules it
    //    out, and the IK itself says "This is not a Flow step"; which
    //    documents a record rule sees is a value fact covered by the unit
    //    tests in tests/test_data_va_generator_operating_unit.yaml.
    tour.register(
        "ssi_va_operating_unit_va_generator_create",
        {
            test: true,
            url: "/web",
        },
        [
            // -- Base Flow 1 -- Open the Contacts menu.
            //
            // res.partner is the source model the base IK uses, because
            // the Generate VA wizard binding is registered for it by
            // default (ssi_va/wizards/generate_va.xml).
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Contacts app",
                trigger: '.o_app[data-menu-xmlid="contacts.menu_contacts"]',
            },
            {
                // Gate on the target action's title, not on a generic view
                // class: opening an app lands on its first menu action,
                // which is also a list/kanban view, so a generic gate
                // would let the next steps act on the wrong view
                // (odoo-development-ui-test patterns.md §A).
                content: "Contacts action is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Contacts)",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                // UI mechanic, not a Flow step: contacts.action_contacts
                // opens in kanban, and 14.0 renders no row checkbox there.
                // The checkbox base Flow 2 asks for only exists in the
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
                // UI mechanic, not a Flow step: res.partner holds far more
                // records than a single list page, so the partner prepared
                // by setUpClass is not reachable by scrolling.
                content: "Search for the partner to generate VA for",
                trigger: ".o_searchview_input",
                extra_trigger: ".o_list_view",
                run: "text " + PARTNER,
            },
            {
                content: "Validate the search",
                trigger: ".o_searchview_autocomplete li.o_menu_item:first",
            },

            // -- Base Flow 2 -- Select one or more partner records to
            // generate Virtual Accounts for (check the checkbox).
            {
                content: "Select the partner record",
                trigger:
                    ".o_data_row:contains(" +
                    PARTNER +
                    ") .o_list_record_selector input",
                run: "click",
            },

            // -- Base Flow 3 -- Click Action > Generate VA.
            {
                content: "Open the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Click Generate VA",
                trigger: ".o_cp_action_menus .o_menu_item a:contains(Generate VA)",
            },
            {
                // Gate for the wizard dialog having been rendered, using a
                // field of the BASE wizard view. Keeping the gate and the
                // delta assertion apart makes a missing Operating Unit
                // field fail on its own step instead of being blamed on
                // the wizard not opening at all.
                content: "The Generate VA wizard is displayed",
                trigger: ".o_field_widget[name='type_id']",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },

            // -- DELTA (Additional Fields of
            // ssi_va_operating_unit/docs/va_generator/01-create.md) --
            // the Operating Unit field is available on the Generate VA
            // wizard.
            //
            // The wizard opens in edit mode, so the many2one renders its
            // <input>, which has real dimensions even while the field is
            // empty. That matters: a READONLY empty many2one in 14.0 is a
            // zero-pixel inline element that the tour's :visible filter
            // would never match (patterns.md §O). The field is not
            // required and its default comes from the user's default
            // operating unit, so it may well be empty here -- and this
            // assertion deliberately does not read its value, which is
            // unit test territory.
            //
            // The field is declared with
            // groups="operating_unit.group_multi_operating_unit" in
            // view/generate_va.xml, so it is only rendered for a member of
            // that group. setUpClass puts the tour user there, which is
            // the Access Pre-Condition of the delta IK.
            {
                content: "The Operating Unit field is displayed in the wizard",
                trigger: ".o_field_widget[name='operating_unit_id'] input",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ]
    );

    // IK: docs/va_generator/02-edit.md
    //
    // THIS IS A DELTA-ONLY TOUR (odoo-development-ui-test patterns.md §O).
    // ssi_va_operating_unit is an extension module and its IK file
    // docs/va_generator/02-edit.md is a delta IK: it carries no Flow of
    // its own, only an "Additional Fields" section on top of the Flow of
    // ssi_va's own docs/va_generator/02-edit.md. The navigation below is
    // therefore taken from the base Flow (Flow 1 and Flow 2 of that
    // file), plus the 14.0 Edit-button mechanic patterns.md §E requires
    // before any field on an already-existing record can be touched. The
    // only thing this tour adds is the assertion that the Operating Unit
    // field is rendered on the va_generator document form, and that it
    // can be changed.
    //
    // TWO DELIBERATE BOUNDARIES, stated here rather than silently
    // skipped:
    //
    // 1. Base Flow 3 ("change the required fields as needed") and any
    //    state action (confirm, approve, ...) are NOT walked. The item's
    //    Keputusan Desain scopes this tour to the Operating Unit field
    //    alone, and a delta tour may not continue into the state actions
    //    of the base IK -- those belong to ssi_va's own edit tour
    //    (ssi_va_va_generator_edit) and to the confirm/approve tours.
    // 2. The persisted value of Operating Unit after Save is NOT
    //    asserted. Reading a field's stored value is unit test territory
    //    (odoo-development-ui-test rule 2); this tour only proves the
    //    field is rendered and can be interacted with, which is what the
    //    delta IK's "Additional Fields" section documents. The value
    //    itself is covered by
    //    tests/test_data_va_generator_operating_unit.yaml.
    tour.register(
        "ssi_va_operating_unit_va_generator_edit",
        {
            test: true,
            url: "/web",
        },
        [
            // -- Base Flow 1 -- Open the Financial Accounting > Bank &
            // Cash > VA Generators menu.
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
                // Gate: wait for the TARGET action to be installed, not
                // just for "a list is on screen". Opening an app lands on
                // its first menu action, which is also a .o_list_view --
                // using that as a gate would let the next steps act on
                // the wrong view (odoo-development-ui-test patterns.md
                // §A).
                content: "Virtual Account Generators list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Virtual Account Generators)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },

            // -- Base Flow 2 -- Find and open the record to edit.
            //
            // The document number of a draft record stays "/", so the
            // row is identified by its Biller instead -- a column of the
            // va_generator tree view. setUpClass gives the record a
            // Biller of its own for exactly that reason.
            {
                content: "Open the record to edit",
                trigger: ".o_data_row:contains(" + BILLER_EDIT + ") .o_data_cell:first",
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
                // Flow step.
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

            // -- DELTA (Additional Fields of
            // ssi_va_operating_unit/docs/va_generator/02-edit.md) -- the
            // Operating Unit field is available on the va_generator
            // document form and can still be changed while editing (it
            // does not carry a per-state readonly restriction).
            //
            // The field is declared with
            // groups="operating_unit.group_multi_operating_unit" in
            // view/va_generator.xml, so it is only rendered for a member
            // of that group. setUpClass puts the tour user there, which
            // is the Access Pre-Condition of the delta IK.
            {
                content: "The Operating Unit field is displayed on the form",
                trigger: ".o_field_widget[name='operating_unit_id'] input",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
            {
                content: "Change the Operating Unit",
                trigger: ".o_field_widget[name='operating_unit_id'] input",
                run: "text " + OPERATING_UNIT,
            },
            {
                content: "Pick " + OPERATING_UNIT + " from the dropdown",
                trigger:
                    ".ui-autocomplete .ui-menu-item a:contains(" + OPERATING_UNIT + ")",
                in_modal: false,
            },

            // -- Flow 5 of the base IK -- Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },
            {
                content: "Record is saved",
                trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click
                    // action.
                },
            },
        ]
    );
});
