// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define(
    "ssi_strategic_management_analytic_budget.strategy_initiative_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/strategy_initiative/01-create.md (E1 delta -- Additional
        // Fields)
        // Navigation (open menu -> New) is taken from the base IK
        // ssi_strategic_management/docs/strategy_initiative/01-create.md
        // Flow steps 1-2 -- see skill odoo-development-ui-test,
        // scope-and-boundaries.md §1 ("Backing dua file: tour extension =
        // base IK U delta IK"). The delta assertion comes from this
        // module's own IK: the Analytic Account field is on the create form.
        // The tour stops there; it does not fill, save, or confirm
        // (E1 delta-only).
        tour.register(
            "ssi_strategic_management_analytic_budget_strategy_initiative_create",
            {
                test: true,
                url: "/web",
            },
            [
                // -- Base Flow 1 -- Open the Strategic Management > Strategy >
                // Initiatives menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Strategic Management app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_strategic_management.menu_strategic_management_root"]',
                },
                {
                    content: "Open the Strategy menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_strategic_management.menu_strategic_management_strategy"]',
                },
                {
                    content: "Open the Initiatives menu",
                    trigger:
                        '.o_menu_sections [data-menu-xmlid="ssi_strategic_management.strategy_initiative_menu"]',
                },
                {
                    content: "Initiatives list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Initiatives)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },

                // -- Base Flow 2 -- Click the New button. (14.0: "Create")
                {
                    content: "Click New",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },

                // -- Delta assertion -- the Analytic Account field is on the
                // create form. The tour stops here (E1 delta-only).
                {
                    content: "Analytic Account field is visible on the form",
                    trigger:
                        ".o_form_view.o_form_editable .o_field_widget[name='analytic_account_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click.
                    },
                },
            ]
        );
    }
);
