.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

================
Virtual Account
================

Provides the ``va_biller`` master data — entities that receive payment
through a Virtual Account (VA), each with a list of bank-specific biller
codes (``va_biller.code``). This master data is the foundation used by
subsequent Virtual Account generation, export, and webhook delivery
features.


Work Instruction
================

* `Virtual Account Biller <docs/va_biller/index.html>`_
* `Virtual Account Biller Merchant <docs/va_biller_merchant/index.html>`_
* `Virtual Account Generator Type <docs/va_generator_type/index.html>`_
* `Virtual Account Generator Exporter <docs/va_generator_exporter/index.html>`_


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-va
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *Virtual Account*
6.  Install the module


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/ssi-va/issues>`_. In case of trouble, please
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
