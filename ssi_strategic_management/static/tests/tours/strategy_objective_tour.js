// Copyright 2026 OpenSynergy Indonesia
// Copyright 2026 PT. Simetri Sinergi Indonesia
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

odoo.define("ssi_strategic_management.strategy_objective_tour", function (require) {
    "use strict";

    var tour = require("web_tour.tour");

    // Shared navigation block -- corresponds to Flow 1 of every
    // strategy_objective work instruction: "Open the Strategic Management >
    // Strategy > Objectives menu."
    //
    // The "Strategy" section sits at level 2 of the menu tree, so it is
    // rendered as a clickable section toggle (only level 3+ menus with
    // children degrade into a non-clickable dropdown header). "Objectives" is
    // the leaf under it.
    function openObjectiveList() {
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
                content: "Open the Objectives menu",
                trigger:
                    '.o_menu_sections [data-menu-xmlid="ssi_strategic_management.strategy_objective_menu"]',
            },
            {
                // Gate: wait until the TARGET action is mounted, not just
                // "a list is on screen".
                content: "Objectives list is displayed",
                trigger:
                    ".o_control_panel .breadcrumb-item.active:contains(Objectives)",
                extra_trigger: ".o_list_view",
                run: function () {
                    // Assertion only; do not trigger the default click action.
                },
            },
        ];
    }

    // Opens the row identified by its Department column text. Objectives
    // that are not started yet all show a "*<id>" placeholder instead of a
    // number, so setUpClass gives every fixture objective its own
    // department and that name is the only stable row key.
    function openObjectiveByDepartment(departmentName) {
        return [
            {
                content: "Open the objective",
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

    // Presses the primary button of the topmost dialog. Its label is
    // "Save & Close" for a new record and "Save" for an existing one
    // (14.0 view_dialogs.js), so both labels are accepted.
    function clickDialogSaveStep(content) {
        return {
            content: content,
            trigger: ".modal-footer button.btn-primary",
            run: function () {
                var $btn = $(".modal:visible")
                    .last()
                    .find(".modal-footer button.btn-primary")
                    .filter(function () {
                        var text = $(this).text().trim();
                        return text === "Save & Close" || text === "Save";
                    });
                $btn[0].click();
            },
        };
    }

    // IK: docs/strategy_objective/01-create.md
    tour.register(
        "ssi_strategic_management_strategy_objective_create",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1 -- Open the Strategic Management > Strategy > Objectives
            // menu.
            openObjectiveList(),
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

                // Flow 3 -- Fill in the required fields: Title, Plan, Department
                // and Perspective. Cascade Method and Responsible keep their
                // default values.
                {
                    content: "Fill in the Title",
                    trigger: ".o_field_widget[name='title']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Tour Objective Title",
                },
                {
                    content: "Type the Plan",
                    trigger: ".o_field_many2one[name='plan_id'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text SP/",
                },
                {
                    content: "Pick the Plan from the dropdown",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(SP/)",
                    in_modal: false,
                },
                {
                    content: "Type the Department",
                    trigger: ".o_field_many2one[name='department_id'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Tour Objective Dept Create",
                },
                {
                    content: "Pick the Department from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(Tour Objective Dept Create)",
                    in_modal: false,
                },
                {
                    content: "Type the Perspective",
                    trigger: ".o_field_many2one[name='perspective_id'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text Financial",
                },
                {
                    content: "Pick the Perspective from the dropdown",
                    trigger: ".ui-autocomplete .ui-menu-item a:contains(Financial)",
                    in_modal: false,
                },

                // Flow 4 (Employee, Owner, Parent Objective, contribution
                // fields and Influences) is explicitly optional and is
                // skipped.

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

                // Post-Condition -- a new record is created in Draft status.
                // The document number still being "/" is a field VALUE and
                // belongs to the unit test, not to this tour.
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

    // IK: docs/strategy_objective/02-edit.md
    tour.register(
        "ssi_strategic_management_strategy_objective_edit",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            // Flow 1-2 -- Open the menu, open the objective.
            openObjectiveList(),
            openObjectiveByDepartment("Tour Objective Dept Edit"),
            [
                // Flow 3 -- Click the Edit button.
                {
                    content: "Click Edit",
                    trigger: ".o_form_button_edit",
                    extra_trigger: ".o_form_view.o_form_readonly",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 4 -- Open the KPIs tab.
                {
                    content: "Open the KPIs page",
                    trigger: ".o_notebook .nav-link:contains(KPIs)",
                    extra_trigger: ".o_form_view.o_form_editable",
                },

                // Flow 5 -- Click Add a line and fill in the KPI: Measure,
                // Name, Weight (%) and Default Target. Key Result is
                // optional and is skipped. The measure is picked first so
                // that its onchange cannot overwrite the values typed after.
                {
                    content: "Add a KPI line",
                    trigger:
                        ".o_field_widget[name='kpi_ids'] .o_field_x2many_list_row_add a",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    content: "Type the Measure",
                    trigger: ".o_field_many2one[name='measure_id'] input",
                    run: "text Tour Edit Measure",
                },
                {
                    content: "Pick the Measure from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(Tour Edit Measure)",
                    in_modal: false,
                },
                {
                    content: "Type the KPI name",
                    trigger: ".o_field_widget[name='name']",
                    run: "text Tour Edit KPI",
                },
                {
                    content: "Type the Weight",
                    trigger: ".o_field_widget[name='weight']",
                    run: "text 100",
                },
                {
                    content: "Type the Default Target",
                    trigger: ".o_field_widget[name='target']",
                    run: "text 200",
                },

                // Flow 6 -- Open the Targets tab of the KPI.
                {
                    content: "Open the Targets page",
                    trigger: ".o_notebook .nav-link:contains(Targets)",
                },

                // Flow 7 -- Click Add a line and fill in the target: Date
                // Start, Date End and Target. The optional Period is skipped.
                {
                    content: "Add a target line",
                    trigger:
                        ".o_field_widget[name='target_ids'] .o_field_x2many_list_row_add a",
                },
                {
                    content: "Type the Date Start",
                    trigger: ".o_field_widget[name='date_start'] input",
                    run: "text 01/01/2026",
                },
                {
                    content: "Type the Date End",
                    trigger: ".o_field_widget[name='date_end'] input",
                    run: "text 03/31/2026",
                },
                {
                    content: "Type the Target",
                    trigger: ".o_field_widget[name='target']",
                    run: "text 200",
                },

                // Flow 8 -- In the Measurements list click Add a line and
                // fill in the Date and Value. The optional Note is skipped.
                // The row is committed by the Save & Close click below.
                {
                    content: "Add a measurement line",
                    trigger:
                        ".o_field_widget[name='measurement_ids'] .o_field_x2many_list_row_add a",
                },
                {
                    content: "Type the measurement Date",
                    trigger: ".o_selected_row .o_field_widget[name='date'] input",
                    run: "text 02/15/2026",
                },
                {
                    content: "Type the measurement Value",
                    trigger: ".o_selected_row .o_field_widget[name='manual_value']",
                    run: "text 150",
                },

                // Flow 9 -- Save & Close the target dialog, then the KPI
                // dialog.
                {
                    content: "Save & Close the target dialog",
                    trigger: ".modal-footer .btn-primary:contains(Save & Close)",
                },
                {
                    // Gate: only matches once the target dialog is gone and
                    // the target row is listed in the KPI dialog.
                    content: "Target is listed in the KPI dialog",
                    trigger:
                        ".o_field_widget[name='target_ids'] .o_data_row:contains(01/01/2026)",
                    run: function () {
                        // Assertion only.
                    },
                },
                {
                    content: "Save & Close the KPI dialog",
                    trigger: ".modal-footer .btn-primary:contains(Save & Close)",
                },

                // Flow 10 -- Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                    extra_trigger: "body:not(:has(.modal))",
                },
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Post-Condition -- the KPI is listed on the KPIs tab.
                // Realization and scores are field VALUES and belong to
                // the unit test, not to this tour.
                {
                    content: "KPI is listed on the KPIs page",
                    trigger:
                        ".o_field_widget[name='kpi_ids'] .o_data_row:contains(Tour Edit KPI)",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 11 -- Click the Edit button again.
                {
                    content: "Click Edit again",
                    trigger: ".o_form_button_edit",
                    extra_trigger: ".o_form_view.o_form_readonly",
                },
                {
                    content: "Form is open in edit mode again",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 12 -- In the KPIs tab click the KPI that uses an
                // automatic measure, then click its target in the Targets
                // tab.
                {
                    content: "Open the KPIs page again",
                    trigger: ".o_notebook .nav-link:contains(KPIs)",
                    extra_trigger: ".o_form_view.o_form_editable",
                },
                {
                    content: "Open the automatic KPI",
                    trigger:
                        ".o_field_widget[name='kpi_ids'] .o_data_row:contains(Tour Compute KPI) .o_data_cell:first",
                },
                {
                    content: "Open the Targets page of the automatic KPI",
                    trigger: ".o_notebook .nav-link:contains(Targets)",
                },
                {
                    content: "Open the target to compute",
                    trigger:
                        ".o_field_widget[name='target_ids'] .o_data_row:contains(01/01/2026) .o_data_cell:first",
                },

                // Flow 13 -- Click the Compute button. The target had no
                // measurement, so any row in the Measurements list proves
                // that the automatic measurement was created.
                {
                    content: "Click Compute",
                    trigger: "button[name='action_compute_realization']",
                },
                {
                    content: "The automatic measurement is listed",
                    trigger: ".o_field_widget[name='measurement_ids'] .o_data_row",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 14 -- Override the automatic value: check Override
                // Automatic Value, type the Value and the Dissenting Note.
                {
                    content: "Select the automatic measurement",
                    trigger:
                        ".o_field_widget[name='measurement_ids'] .o_data_row .o_data_cell:first",
                },
                {
                    content: "Check Override Automatic Value",
                    trigger:
                        ".o_selected_row .o_field_widget[name='override_automatic'] input",
                },
                {
                    content: "Type the overriding Value",
                    trigger: ".o_selected_row .o_field_widget[name='manual_value']",
                    run: "text 5",
                },
                {
                    content: "Type the Dissenting Note",
                    trigger: ".o_selected_row .o_field_widget[name='dissenting_note']",
                    run: "text Known data error",
                },

                // Flow 15 -- Save & Close the target dialog, then the KPI
                // dialog.
                clickDialogSaveStep("Save & Close the target dialog again"),
                {
                    content: "Target is listed in the KPI dialog again",
                    trigger:
                        ".o_field_widget[name='target_ids'] .o_data_row:contains(01/01/2026)",
                    run: function () {
                        // Assertion only.
                    },
                },
                clickDialogSaveStep("Save & Close the KPI dialog again"),

                // Flow 16 -- Click Save.
                {
                    content: "Save the record again",
                    trigger: ".o_form_button_save",
                    extra_trigger: "body:not(:has(.modal))",
                },
                {
                    content: "Record is saved again",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only.
                    },
                },
            ]
        )
    );

    // IK: docs/strategy_objective/07-start.md
    tour.register(
        "ssi_strategic_management_strategy_objective_start",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openObjectiveList(),
            openObjectiveByDepartment("Tour Objective Dept Start"),
            // Pre-Condition -- the fixture objective has one KPI whose weight
            // is 100, so the KPI weight check of the Start action passes.
            // Flow 3-4 -- Click Start, then OK on the dialog.
            // Post-Condition -- status changes to On Progress. The document
            // number being assigned is a field VALUE and belongs to the unit
            // test, not to this tour.
            pressAndConfirm("action_open", "Start", "open", "On Progress")
        )
    );

    // IK: docs/strategy_objective/09-finish.md
    tour.register(
        "ssi_strategic_management_strategy_objective_finish",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openObjectiveList(),
            openObjectiveByDepartment("Tour Objective Dept Finish"),
            // Flow 3-4 -- Click Done, then OK on the dialog.
            // Post-Condition -- status changes to Done.
            pressAndConfirm("action_done", "Done", "done", "Done")
        )
    );

    // IK: docs/strategy_objective/10-cancel.md
    tour.register(
        "ssi_strategic_management_strategy_objective_cancel",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openObjectiveList(),
            openObjectiveByDepartment("Tour Objective Dept Cancel"),
            [
                // Flow 3 -- Click the Cancel button. The button is
                // type="action", so its name= is resolved to a numeric
                // window action id at render time and can never be matched
                // by [name='action_cancel'] -- the label is the only stable
                // handle here.
                {
                    content: "Click the Cancel button",
                    trigger: ".o_statusbar_buttons button:contains(Cancel)",
                    extra_trigger: ".o_form_view",
                },
                {
                    // Wizard gate. In 14.0 an in-modal trigger must NOT be
                    // prefixed with ".modal". Gating on the cancel_reason_id
                    // widget rather than on ".o_form_view" matters: the
                    // record's own form view sits behind the wizard.
                    content: "Wizard is open",
                    trigger: ".o_field_widget[name='cancel_reason_id']",
                    run: function () {
                        // Assertion only.
                    },
                },

                // Flow 4 -- Select the Cancellation Reason (radio widget:
                // click its label).
                {
                    content: "Select the cancellation reason",
                    trigger:
                        ".o_field_widget[name='cancel_reason_id'] label:contains(Tour Objective Cancel Reason)",
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

    // IK: docs/strategy_objective/12-restart.md
    tour.register(
        "ssi_strategic_management_strategy_objective_restart",
        {
            test: true,
            url: "/web",
        },
        [].concat(
            openObjectiveList(),
            openObjectiveByDepartment("Tour Objective Dept Reopen"),
            // Flow 3-4 -- Click Restart, then OK on the dialog.
            // Post-Condition -- status returns to Draft.
            pressAndConfirm("action_restart", "Restart", "draft", "Draft")
        )
    );
});
