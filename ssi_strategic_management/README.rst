.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================
Strategic Management
====================

Strategic management application for companies that run on Odoo: strategic
plans, Balanced Scorecard perspectives, OKR, KPI measures and initiatives.
This module provides the application skeleton, the security categories, the
main menu and the master data shared by the whole module family:
perspectives, the measure library, score categories and plan types. It
also provides the strategy plan, the parent document of every objective,
KPI and initiative, which can be nested into sub-plans and goes through
an approval workflow. Strategy objectives belong to a plan and are cascaded
to departments and, when the plan type allows it, to employees, from a
parent objective down to its children. Each objective is measured by KPIs
(including OKR key results) that have targets per period and manually
recorded measurements, and every target and KPI is scored according to the
score method of the KPI.


Work Instruction
================

Perspective
-----------

* `Create Perspective <docs/strategy_perspective/01-create.html>`_

Measure
-------

* `Create Measure <docs/strategy_measure/01-create.html>`_

Score Category
--------------

* `Create Score Category <docs/strategy_score_category/01-create.html>`_

Plan Type
---------

* `Create Plan Type <docs/strategy_plan_type/01-create.html>`_

Plan
----

* `Create Plan <docs/strategy_plan/01-create.html>`_
* `Confirm Plan <docs/strategy_plan/04-confirm.html>`_
* `Approve Plan <docs/strategy_plan/05-approve.html>`_
* `Reject Plan <docs/strategy_plan/06-reject.html>`_
* `Start Plan <docs/strategy_plan/07-start.html>`_
* `Finish Plan <docs/strategy_plan/09-finish.html>`_
* `Cancel Plan <docs/strategy_plan/10-cancel.html>`_
* `Restart Plan <docs/strategy_plan/12-restart.html>`_
* `Reset Plan Document Number <docs/strategy_plan/13-reset-number.html>`_
* `Restart Plan Approval Process <docs/strategy_plan/14-restart-approval.html>`_
* `Reload Plan Policy Template <docs/strategy_plan/15-reload-policy-template.html>`_

Objective
---------

* `Create Objective <docs/strategy_objective/01-create.html>`_
* `Edit Objective <docs/strategy_objective/02-edit.html>`_
* `Start Objective <docs/strategy_objective/07-start.html>`_
* `Finish Objective <docs/strategy_objective/09-finish.html>`_
* `Cancel Objective <docs/strategy_objective/10-cancel.html>`_
* `Restart Objective <docs/strategy_objective/12-restart.html>`_
* `Reset Objective Document Number <docs/strategy_objective/13-reset-number.html>`_
* `Reload Objective Policy Template <docs/strategy_objective/15-reload-policy-template.html>`_


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-strategic-management
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Strategic Management*
6.  Install the module


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/ssi-strategic-management/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Andhitia Rama <andhitia.r@gmail.com>
* Michael Viriyananda <viriyananda.michael@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
