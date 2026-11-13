// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_strategic_management.strategy_initiative_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block -- corresponds to Flow 1 of every
    // strategy_initiative work instruction: "Open the Strategic Management >
    // Strategy > Initiatives menu."
    function openInitiativeList() {
        return [
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
                // Gate: wait until the TARGET action is mounted, not just
                // "a list is on screen".
                content: "Initiatives list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Initiatives)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Opens the row identified by its Department column text. Initiatives
    // that are not started yet all show a "*<id>" placeholder instead of a
    // number, so setUpClass gives every fixture initiative its own department
    // and that name is the only stable row key.
    function openInitiativeByDepartment(departmentName) {
        return [
            {
                content: "Open the initiative",
                trigger:
                    ".o_data_row:contains(" + departmentName + ") .o_data_cell:first",
                extra_trigger: ".o_list_view",
            },
            {
                content: "Form is open",
                trigger: ".o_form_view",
                run: function () {
                    // Assertion only.
                },
            },
        ];
    }

    // Clicks a statusbar button and accepts the confirmation dialog, then
    // asserts the statusbar highlights the expected state.
    function pressAndConfirm(buttonName, buttonLabel, expectedState, stateLabel) {
        return [
            {
                content: "Click the " + buttonLabel + " button",
                trigger: ".o_statusbar_buttons button[name='" + buttonName + "']",
                extra_trigger: ".o_form_view",
            },
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },
            {
                content: "Status is " + stateLabel,
                trigger:
                    ".o_statusbar_status .o_arrow_button[data-value='" +
                    expectedState +
                    "'].btn-primary",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only.
                },
            },
        ];
    }

    // IK: docs/strategy_initiative/01-create.md
    tour.register(
        "ssi_strategic_management_strategy_initiative_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Strategic Management > Strategy > Initiatives menu.
            openInitiativeList(),
            [
                // Flow 2 -- Click the New button. (14.0: "Create")
                {
                    content: "Click New",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 3 -- Fill in the required fields: Title, Plan, Date Start,
                // Date End. Responsible and Progress Method keep their
                // default values.
                {
                    content: "Fill in the Title",
                    trigger: ".o_field_widget[name='title'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Tour Initiative Title",
                },
                {
                    content: "Type the Plan",
                    trigger: ".o_field_many2one[name='plan_id'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Tour Initiative Plan",
                },
                {
                    content: "Pick the Plan from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(Tour Initiative Plan)",
                    in_modal: false,
                },
                {
                    content: "Fill in Date Start",
                    trigger: ".o_field_widget[name='date_start'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 01/01/2026",
                },
                {
                    content: "Fill in Date End",
                    trigger: ".o_field_widget[name='date_end'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 12/31/2026",
                },

                // Flow 4 (Owner, Department, Scope) and Flow 5 (milestones,
                // manual figure, progress code) are explicitly optional and
                // are skipped.

                // Flow 6 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Post-Condition -- a new record is created in Draft status.
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/strategy_initiative/04-confirm.md
    tour.register(
        "ssi_strategic_management_strategy_initiative_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openInitiativeList(),
            openInitiativeByDepartment("Tour Init Dept Confirm"),
            // Flow 3-4 -- Click Confirm, then OK on the dialog.
            // Post-Condition -- status changes to Waiting for Approval.
            pressAndConfirm(
                "action_confirm",
                "Confirm",
                "confirm",
                "Waiting for Approval"
            )
        )
    );

    // IK: docs/strategy_initiative/05-approve.md
    tour.register(
        "ssi_strategic_management_strategy_initiative_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openInitiativeList(),
            openInitiativeByDepartment("Tour Init Dept Approve"),
            [
                // Flow 3 -- Click the Approve button.
                {
                    content: "Click the Approve button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_approve_approval']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- the standard approval.template has a single
                // level: the initiative stays Waiting for Approval, but the
                // Approve button is gone and the Start button appears.
                {
                    content: "Start button is available",
                    trigger: ".o_statusbar_buttons button[name='action_open']",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/strategy_initiative/07-start.md
    tour.register(
        "ssi_strategic_management_strategy_initiative_start",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openInitiativeList(),
            openInitiativeByDepartment("Tour Init Dept Start"),
            // Flow 3-4 -- Click Start, then OK on the dialog.
            // Post-Condition -- status changes to On Progress.
            pressAndConfirm("action_open", "Start", "open", "On Progress")
        )
    );

    // IK: docs/strategy_initiative/09-finish.md
    tour.register(
        "ssi_strategic_management_strategy_initiative_finish",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openInitiativeList(),
            openInitiativeByDepartment("Tour Init Dept Finish"),
            // Flow 3-4 -- Click Done, then OK on the dialog.
            // Post-Condition -- status changes to Done.
            pressAndConfirm("action_done", "Done", "done", "Done")
        )
    );

    // IK: docs/strategy_initiative/12-restart.md
    tour.register(
        "ssi_strategic_management_strategy_initiative_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openInitiativeList(),
            openInitiativeByDepartment("Tour Init Dept Reopen"),
            // Flow 3-4 -- Click Restart, then OK on the dialog.
            // Post-Condition -- status changes to Draft.
            pressAndConfirm("action_restart", "Restart", "draft", "Draft")
        )
    );

    // IK: docs/strategy_initiative/10-cancel.md
    tour.register(
        "ssi_strategic_management_strategy_initiative_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openInitiativeList(),
            openInitiativeByDepartment("Tour Init Dept Cancel"),
            [
                // Flow 3 -- Click the Cancel button. The button is
                // type="action", so its name= is resolved to a numeric window
                // action id at render time -- the label is the only stable
                // handle here.
                {
                    content: "Click the Cancel button",
                    trigger: ".o_statusbar_buttons button:contains(Cancel)",
                    extra_trigger: ".o_form_view",
                },
                {
                    // Wizard gate. In 14.0 an in-modal trigger must NOT be
                    // prefixed with ".modal".
                    content: "Wizard is open",
                    trigger: ".o_field_widget[name='cancel_reason_id']",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 4 -- Select the reason (radio widget: click its label).
                {
                    content: "Select the reason",
                    trigger:
                        ".o_field_widget[name='cancel_reason_id'] label:contains(Tour Initiative Cancel Reason)",
                },

                // Flow 5 -- Click Confirm.
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },

                // Flow 6 -- Click OK on the stacked confirmation dialog.
                {
                    content: "Confirm the stacked dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Cancelled.
                {
                    content: "Status is Cancelled",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/strategy_initiative/11-terminate.md
    tour.register(
        "ssi_strategic_management_strategy_initiative_terminate",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openInitiativeList(),
            openInitiativeByDepartment("Tour Init Dept Terminate"),
            [
                // Flow 3 -- Click the Terminate button. The button is
                // type="action", so its name= is resolved to a numeric window
                // action id at render time -- the label is the only stable
                // handle here.
                {
                    content: "Click the Terminate button",
                    trigger: ".o_statusbar_buttons button:contains(Terminate)",
                    extra_trigger: ".o_form_view",
                },
                {
                    // Wizard gate. In 14.0 an in-modal trigger must NOT be
                    // prefixed with ".modal".
                    content: "Wizard is open",
                    trigger: ".o_field_widget[name='terminate_reason_id']",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 4 -- Select the reason (radio widget: click its label).
                {
                    content: "Select the reason",
                    trigger:
                        ".o_field_widget[name='terminate_reason_id'] label:contains(Tour Initiative Terminate Reason)",
                },

                // Flow 5 -- Click Confirm.
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },

                // Flow 6 -- Click OK on the stacked confirmation dialog.
                {
                    content: "Confirm the stacked dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- status changes to Terminated.
                {
                    content: "Status is Terminated",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='terminate'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/strategy_initiative/14-restart-approval.md
    tour.register(
        "ssi_strategic_management_strategy_initiative_restart_approval",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openInitiativeList(),
            openInitiativeByDepartment("Tour Init Dept Restart Approval"),
            [
                // Flow 3 -- Click the Restart Approval Process button.
                {
                    content: "Click the Restart Approval Process button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reload_approval_template']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 -- Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },

                // Post-Condition -- the approval records are rebuilt without
                // changing the status: the Approve button shows up for the
                // active approver, and the Restart Approval Process button
                // is gone because a template is assigned again.
                {
                    content: "Approve button is available",
                    trigger:
                        ".o_statusbar_buttons button[name='action_approve_approval']",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Status is still Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );
});
