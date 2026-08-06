// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_va_operating_unit.va_generator_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Created by tests/test_ui_va_generator.py. The name is the "glue"
    // between the Python Pre-Condition data and the UI steps: it is typed
    // into the search view and matched on the list row.
    var PARTNER = "TOUR VAGENOU Partner";

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
});
