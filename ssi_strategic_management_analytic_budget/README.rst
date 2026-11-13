.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==================================================
Strategic Management + Analytic Budget Integration
==================================================

Glue module between ``ssi_strategic_management`` and ``ssi_analytic_budget``.
A strategy initiative can be linked to an analytic account and then shows the
planned cost, the cost realization and the budget absorption of the open and
done analytic budgets of that account (child accounts included) whose period
overlaps the period of the initiative. No budget figure is stored on the
initiative: every figure is computed from the analytic budgets. While an
initiative is in progress, a budget absorption that is ahead of its progress
lowers its health. The analytic budget form lists the strategy initiatives that
use its analytic account.


Work Instruction
================

* `Create Initiative <docs/strategy_initiative/01-create.html>`_


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-strategic-management
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Strategic Management + Analytic Budget Integration*
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

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
