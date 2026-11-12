// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_strategic_management.strategy_perspective_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // IK: docs/strategy_perspective/01-create.md
    tour.register(
        "ssi_strategic_management_strategy_perspective_create",
        {
            test: true,
            url: "/web",
        },
        [
            // ── Flow 1 — Open the Strategic Management > Configuration >
            // Perspectives menu.
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Strategic Management app",
                trigger:
                    '.o_app[data-menu-xmlid="ssi_strategic_management.menu_strategic_management_root"]',
            },
            {
                content: "Open the Configuration menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_strategic_management.menu_strategic_management_configuration"]',
            },
            {
                content: "Open the Perspectives menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_strategic_management.strategy_perspective_menu"]',
            },
            {
                // Gate: wait until the TARGET action is mounted, not just
                // "a list is on screen".
                content: "Perspectives list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Perspectives)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 2 — Click the New button. (14.0: "Create")
            {
                content: "Click New",
                trigger: ".o_list_button_add",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open in edit mode",
                trigger: ".o_form_view.o_form_editable",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 3 — Fill in the required fields: Name, Code. Every
            // other field keeps its default value.
            {
                content: "Fill in the Name",
                trigger: ".o_field_widget[name='name']",
                extra_trigger: ".o_form_view.o_form_editable",
                run: "text TOUR Perspective Create",
            },
            {
                content: "Fill in the Code",
                trigger: ".o_field_widget[name='code']",
                run: "text /",
            },

            // ── Flow 4 — Click Generate Code in the header to assign a
            // code from the configured sequence.template.
            {
                content: "Click Generate Code",
                trigger: ".o_statusbar_buttons button[name='action_generate_code']",
                extra_trigger: ".o_form_view.o_form_editable",
            },
            {
                content: "Record is saved by Generate Code",
                trigger: ".o_control_panel .breadcrumb-item.active:not(:contains(New))",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },

            // ── Flow 5 — Click Save.
            {
                content: "Save the record",
                trigger: ".o_form_button_save",
            },

            // ── Post-Condition — a new Perspective record is created and
            // active.
            {
                content: "Record is saved",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(TOUR Perspective Create)",
                extra_trigger: ".o_form_view.o_form_readonly",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ]
    );
});
