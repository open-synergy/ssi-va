// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_va.ir_model_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // The model turned into a Virtual Account source by this tour. It is
    // prepared by tests/test_ui_ir_model.py, which also creates one record of
    // it so that the Action menu asserted by the Post-Condition can be opened
    // from both the list view and the form view of that model.
    //
    // "va_generator_exporter" is picked because its technical name is a unique
    // substring among every installed model, so the Flow 2 search leaves
    // exactly one row -- unlike "va_biller", which is also a prefix of
    // va_biller_code, va_biller_merchant and va_biller_merchant_code.
    var TARGET_MODEL = "va_generator_exporter";
    var TARGET_RECORD = "TOUR IRMODEL VA SOURCE";

    // IK: docs/ir_model/04-add-generate-va-wizard.md
    tour.register(
        "ssi_va_ir_model_add_generate_va_wizard",
        {
            test: true,
            // Developer mode is stated by Flow 1 as a condition for the
            // Technical menu to be visible, and it is not a click: the menu
            // (base.menu_custom) carries groups="base.group_no_one", and
            // ir.ui.menu._visible_menu_ids() subtracts that group from the
            // user's groups whenever request.session.debug is empty. The URL
            // parameter is what fills session.debug
            // (ir.http._handle_debug), so it is carried here as well as in the
            // start_tour() call -- tour_manager.run() reloads
            // window.location.origin + this url before the first step runs,
            // which would otherwise drop the parameter.
            url: "/web?debug=1",
        },
        [
            // ── Flow 1 — Open the Settings > Technical > Database Structure >
            // Models menu.
            //
            // The IK menu path has four levels but only three are clickable:
            // "Database Structure" (base.next_id_9) is a <menuitem> without an
            // action that has children, so 14.0 renders it as a
            // .dropdown-header with no data-menu-xmlid and its children are
            // flattened into the same dropdown (odoo-development-ui-test
            // patterns.md §A). There is therefore no step for it.
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Settings app",
                trigger: '.o_app[data-menu-xmlid="base.menu_administration"]',
            },
            {
                content: "Open the Technical menu",
                trigger: '.o_menu_sections [data-menu-xmlid="base.menu_custom"]',
            },
            {
                content: "Open the Models menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="base.ir_model_model_menu"]',
            },
            {
                // Gate: wait for the TARGET action to be installed, not just
                // for "a list is on screen". Opening an app lands on its first
                // menu action, which is also a .o_list_view -- using that as a
                // gate would let the next steps act on the wrong view
                // (odoo-development-ui-test patterns.md §A). The Settings app
                // lands on the Users action, whose title does not carry the
                // "Models" substring, so no negation is needed here.
                content: "Models list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Models)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 2 — Open the record of the model that should become a
            // Virtual Account source.
            //
            // The search bar is the mechanical means of "opening the record"
            // here, not an extra Flow step: ir.model is ordered by its
            // technical name (_order = "model") and holds far more than the 80
            // rows of the first page, so a model whose name starts with "v" is
            // never reachable by clicking a row of the unfiltered list.
            {
                content: "Search for the model to turn into a VA source",
                trigger: ".o_searchview_input",
                run: "text " + TARGET_MODEL,
            },
            {
                // The first autocomplete source is the "Model" field of
                // base.view_model_search, whose filter_domain matches either
                // the description or the technical name. Clicking the <li> is
                // what selects the source: the inner <a> only prevents the
                // default and lets the event bubble up to it.
                content: "Validate the search",
                trigger: ".o_searchview_autocomplete li.o_menu_item:first",
            },
            {
                content: "Open the model record",
                trigger:
                    ".o_data_row:contains(" + TARGET_MODEL + ") .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                // Gate: the technical name is only rendered on the form of the
                // record that was just opened, so this cannot match earlier.
                content: "Model form is displayed",
                trigger:
                    ".o_form_view .o_field_widget[name='model']:contains(" +
                    TARGET_MODEL +
                    ")",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — Click the Add Generate VA Wizard button
            // (action_create_va_wizard) in the header.
            //
            // The sub-bullet of this Flow step ("if the model is a transient
            // model, the action fails with a UserError") is a negative path.
            // Per the issue Test Scenario the tour only walks the successful
            // path; the rejection of transient models is covered by the unit
            // tests instead.
            {
                content: "Click Add Generate VA Wizard",
                trigger: ".o_statusbar_buttons button[name='action_create_va_wizard']",
                extra_trigger: ".o_form_view",
            },
            {
                // Gate for the object button. There is nothing on this screen
                // that the action changes -- the binding it creates is only
                // visible from the Action menu of the TARGET model, which is
                // the Post-Condition asserted at the end of this tour. What
                // must be waited for here is the click landing, and 14.0 gives
                // a signal for exactly that: form_renderer.disableButtons()
                // marks every .o_statusbar_buttons button as disabled for the
                // whole duration of the RPC and enableButtons() clears it
                // afterwards (web/static/src/js/views/form/form_renderer.js).
                // Without this gate the second press of Flow 4 would be
                // dispatched on a disabled button and silently swallowed.
                content: "Wait for the first press to complete",
                trigger:
                    ".o_statusbar_buttons " +
                    "button[name='action_create_va_wizard']:not([disabled])",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 4 — Optional: click Add Generate VA Wizard again on the
            // same record; pressing it repeatedly is allowed.
            //
            // Only the "it is accepted, not rejected" half of that Flow step is
            // walked. The IK describes the second press as producing a
            // separately numbered binding (Generate VA #2), but per the issue
            // Design Decision the tour neither counts nor inspects the names of
            // the ir.actions.act_window records that are created -- it stops at
            // a new entry showing up in the Action menu.
            {
                content: "Click Add Generate VA Wizard again",
                trigger: ".o_statusbar_buttons button[name='action_create_va_wizard']",
            },
            {
                // Same gate as above, for the same reason: the navigation of
                // the Post-Condition must not start while the second press is
                // still in flight.
                content: "Wait for the second press to complete",
                trigger:
                    ".o_statusbar_buttons " +
                    "button[name='action_create_va_wizard']:not([disabled])",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Post-Condition — A new entry appears in the model's Action
            // menu, visible from both the list view and the form view of that
            // model.
            //
            // Reaching that menu means navigating to the target model, which is
            // where its Action menu lives; the navigation itself is not an
            // assertion. This is also the first time the tour visits that
            // action, so its load_views call -- and with it the toolbar the
            // Action menu is built from -- is fetched after the bindings were
            // created, and not served from the client-side view cache.
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
                content: "Virtual Account Generator Exporters list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Virtual Account Generator Exporters)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                // 14.0 only renders the Action menu of a list view once at
                // least one record is selected (list_controller.js
                // _getActionMenuItems). Selecting the row is therefore a UI
                // mechanic of reading the menu, not a Flow step.
                content: "Select a record of the model",
                trigger:
                    ".o_data_row:contains(" +
                    TARGET_RECORD +
                    ") .o_list_record_selector input",
                run: "click",
            },
            {
                content: "Open the Action menu of the list view",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                // The Post-Condition, seen from the list view. Only the
                // presence of the entry is asserted: how many were created and
                // how they are named is explicitly out of scope per the issue
                // Design Decision.
                content: "Generate VA entry is offered in the list Action menu",
                trigger: ".o_cp_action_menus .o_menu_item a:contains(Generate VA)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                // Close the dropdown before leaving the list. 14.0 toggles it
                // on the same button, and leaving it open would make the row
                // click below race the document-level handler that closes it.
                content: "Close the Action menu",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                content: "Open the record of the model",
                trigger:
                    ".o_data_row:contains(" + TARGET_RECORD + ") .o_data_cell:first",
            },
            {
                content: "Record form is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(" +
                    TARGET_RECORD +
                    ")",
                extra_trigger: ".o_form_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
            {
                content: "Open the Action menu of the form view",
                trigger: ".o_cp_action_menus button:contains(Action)",
            },
            {
                // The same Post-Condition, seen from the form view. The IK
                // states both views explicitly, so both are walked.
                content: "Generate VA entry is offered in the form Action menu",
                trigger: ".o_cp_action_menus .o_menu_item a:contains(Generate VA)",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
