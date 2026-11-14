// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_strategic_management.strategy_review_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block -- corresponds to Flow 1 of every
    // strategy_review work instruction: "Open the Strategic Management >
    // Monitoring > Reviews menu."
    function openReviewList() {
        return [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: "Open the Strategic Management app",
                trigger:
                    '.o_app[data-menu-xmlid="ssi_strategic_management.menu_strategic_management_root"]',
            },
            {
                content: "Open the Monitoring menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_strategic_management.menu_strategic_management_monitoring"]',
            },
            {
                content: "Open the Reviews menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_strategic_management.strategy_review_menu"]',
            },
            {
                // Gate: wait until the TARGET action is mounted, not just
                // "a list is on screen".
                content: "Reviews list is displayed",
                trigger: ".o_control_panel .breadcrumb-item.active:contains(Reviews)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Opens the row identified by its Summary column text. Reviews that are
    // not finished yet all show a "*<id>" placeholder instead of a number,
    // so setUpClass gives every fixture review its own summary token and
    // that token is the only stable row key.
    function openReviewBySummary(summaryToken) {
        return [
            {
                content: "Open the review",
                trigger:
                    ".o_data_row:contains(" + summaryToken + ") .o_data_cell:first",
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

    // IK: docs/strategy_review/01-create.md
    tour.register(
        "ssi_strategic_management_strategy_review_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Strategic Management > Monitoring > Reviews menu.
            openReviewList(),
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
                // Date End. Responsible keeps its default value.
                {
                    content: "Fill in the Title",
                    trigger: ".o_field_widget[name='title']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Tour Review Title",
                },
                {
                    content: "Type the Plan",
                    trigger: ".o_field_many2one[name='plan_id'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Tour Review Plan",
                },
                {
                    content: "Pick the Plan from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(Tour Review Plan)",
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
                    run: "text 03/31/2026",
                },

                // Flow 4 (Department, Summary) is explicitly optional and
                // is skipped.

                // Flow 5 -- Click Save.
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

                // Flow 6 -- On the Snapshot tab, click Take Snapshot.
                {
                    content: "Open the Snapshot tab",
                    trigger: ".o_notebook .nav-link:contains(Snapshot)",
                    extra_trigger: ".o_form_view.o_form_readonly",
                },
                {
                    content: "Click the Take Snapshot button",
                    trigger: "button[name='action_take_snapshot']",
                    extra_trigger: ".o_form_view.o_form_readonly",
                },
                {
                    // Gate: the KPI line carries a token that cannot exist
                    // before the snapshot is taken (the record is new).
                    content: "The snapshot lines are listed",
                    trigger:
                        ".o_field_widget[name='line_ids'] .o_data_row:contains(Tour Review KPI)",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 7 (comment and corrective action) is explicitly
                // optional and is skipped.

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

    // IK: docs/strategy_review/04-confirm.md
    tour.register(
        "ssi_strategic_management_strategy_review_confirm",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openReviewList(),
            openReviewBySummary("TRV-CONFIRM"),
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

    // IK: docs/strategy_review/05-approve.md
    tour.register(
        "ssi_strategic_management_strategy_review_approve",
        {
            test: true,
            url: "/web",
        },
        [].concat(openReviewList(), openReviewBySummary("TRV-APPROVE"), [
            // Flow 3 -- Click the Approve button.
            {
                content: "Click the Approve button",
                trigger: ".o_statusbar_buttons button[name='action_approve_approval']",
                extra_trigger: ".o_form_view",
            },

            // Flow 4 -- Click OK on the confirmation dialog.
            {
                content: "Confirm the dialog",
                trigger: ".modal-footer button.btn-primary",
                in_modal: true,
            },

            // Post-Condition -- the standard approval.template has a single
            // level: the review stays Waiting for Approval, but the
            // Approve button is gone and the Done button appears.
            {
                content: "Done button is available",
                trigger: ".o_statusbar_buttons button[name='action_done']",
                extra_trigger: "body:not(:has(.modal))",
                run: function () {
                    // Assertion only.
                },
            },
        ])
    );

    // IK: docs/strategy_review/09-finish.md
    tour.register(
        "ssi_strategic_management_strategy_review_finish",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openReviewList(),
            openReviewBySummary("TRV-FINISH"),
            // Flow 3-4 -- Click Done, then OK on the dialog.
            // Post-Condition -- status changes to Done.
            pressAndConfirm("action_done", "Done", "done", "Done")
        )
    );

    // IK: docs/strategy_review/10-cancel.md
    tour.register(
        "ssi_strategic_management_strategy_review_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(openReviewList(), openReviewBySummary("TRV-CANCEL"), [
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
                    ".o_field_widget[name='cancel_reason_id'] label:contains(Tour Review Cancel Reason)",
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
        ])
    );
});
