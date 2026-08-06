# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiVAGenerator(HttpSavepointCase):
    """UI/UX tour tests for the ``va_generator`` work instructions.

    Every ``test_*`` method runs the tour paired with the IK file named
    in its docstring (``docs/va_generator/NN-*.md``). Pre-Condition data
    of those IK files is prepared here in Python -- never through UI
    steps -- because ``va_generator`` is a transactional document whose
    prerequisites (bank, biller with a bank code, merchant with a biller
    code, generator type, usage, exporter, source record) would
    otherwise take a whole tour of their own to build.
    """

    #: The Financial Accounting app exposes several menu sections and the
    #: va_generator statusbar carries five states; the default 1366px
    #: viewport pushes part of both into overflow, where a tour trigger
    #: would fail the implicit ``:visible`` check.
    browser_size = "1920x1080"

    @classmethod
    def setUpClass(cls):
        """Prepare the IK Pre-Conditions of the va_generator tours.

        Covers the Pre-Condition types the three IK files declare:

        * ``Access`` -- admin is put in ``Virtual Account Generator /
          User``, the group the IK names as actor. It is also put in
          ``Virtual Account Generator / All``, because the record rules
          of this model restrict a plain internal user to the documents
          they are responsible for, and the documents below are created
          by the test cursor's superuser rather than by admin.
        * ``Data`` -- generator types, banks, billers holding a bank
          code for those banks, merchants holding a biller code, bank
          account usages and exporters, so that every many2one of the
          Generate VA wizard and of the document form can be picked.
        * ``Record`` -- two draft ``va_generator`` documents, one for
          the edit tour and one for the delete tour. Each carries a
          Biller of its own: a draft document's number is still ``/``,
          so the Biller column of the tree view is what makes its row
          identifiable.

        The ``Config`` Pre-Condition of ``01-create`` -- a Generate VA
        entry in the source model's Action menu -- needs no setup: the
        binding for ``res.partner`` ships with the module
        (``wizards/generate_va.xml``).
        """
        super().setUpClass()

        cls.user_admin = cls.env.ref("base.user_admin")
        groups = cls.env.ref("ssi_va.va_generator_user_group") + cls.env.ref(
            "ssi_va.va_generator_all_group"
        )
        groups.sudo().write(
            {
                "users": [(4, cls.user_admin.id)],
            }
        )

        cls.model_res_partner = cls.env.ref("base.model_res_partner")
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "TOUR VAGEN Partner",
            }
        )

        cls.type_alpha = cls._create_generator_type("TOUR VAGEN Type Alpha")
        cls.type_beta = cls._create_generator_type("TOUR VAGEN Type Beta")

        cls.bank_alpha = cls.env["res.bank"].create(
            {
                "name": "TOUR VAGEN Bank Alpha",
            }
        )
        cls.bank_beta = cls.env["res.bank"].create(
            {
                "name": "TOUR VAGEN Bank Beta",
            }
        )

        cls.biller_create = cls._create_biller(
            "TOUR VAGEN Biller Create", cls.bank_alpha, "VAC01"
        )
        cls.biller_edit = cls._create_biller(
            "TOUR VAGEN Biller Edit", cls.bank_alpha, "VAE01"
        )
        cls.biller_delete = cls._create_biller(
            "TOUR VAGEN Biller Delete", cls.bank_alpha, "VAD01"
        )
        cls.biller_beta = cls._create_biller(
            "TOUR VAGEN Biller Beta", cls.bank_beta, "VAB01"
        )

        cls.merchant_create = cls._create_merchant(
            "TOUR VAGEN Merchant Create", cls.biller_create, "MC01"
        )
        cls.merchant_edit = cls._create_merchant(
            "TOUR VAGEN Merchant Edit", cls.biller_edit, "ME01"
        )

        cls.usage_alpha = cls._create_master_data(
            "res_partner_bank_usage", "TOUR VAGEN Usage Alpha"
        )
        cls.usage_beta = cls._create_master_data(
            "res_partner_bank_usage", "TOUR VAGEN Usage Beta"
        )
        cls.exporter_alpha = cls._create_master_data(
            "va_generator_exporter", "TOUR VAGEN Exporter Alpha"
        )
        cls.exporter_beta = cls._create_master_data(
            "va_generator_exporter", "TOUR VAGEN Exporter Beta"
        )

        cls.generator_edit = cls._create_generator(
            cls.biller_edit,
            merchant=cls.merchant_edit,
        )
        cls.generator_delete = cls._create_generator(cls.biller_delete)

    @classmethod
    def _create_master_data(cls, model_name, name):
        """Create a ``mixin.master_data`` record used as tour data.

        ``code`` is set to ``"/"`` so that several records can coexist:
        ``mixin.master_data._check_duplicate_code`` skips that value.

        :param str model_name: Technical name of the master data model.
        :param str name: Name of the record, matched by the tour in the
            many2one autocomplete dropdown.
        :return: The created record.
        :rtype: :class:`odoo.models.Model`
        """
        return cls.env[model_name].create(
            {
                "name": name,
                "code": "/",
            }
        )

    @classmethod
    def _create_generator_type(cls, name):
        """Create a ``va_generator_type`` used by the tours.

        ``model_id`` is left empty on purpose: a generator type
        restricted to another model is rejected by the Generate VA
        wizard when it is launched from ``res.partner``.

        :param str name: Name of the generator type record.
        :return: The created ``va_generator_type`` record.
        :rtype: :class:`odoo.models.Model`
        """
        return cls._create_master_data("va_generator_type", name)

    @classmethod
    def _create_biller(cls, name, bank, biller_code):
        """Create a ``va_biller`` holding a code for ``bank``.

        The bank code line is what makes the biller selectable: both
        the Generate VA wizard and the document form restrict Biller to
        those holding a Virtual Account code for the selected Bank.

        :param str name: Name of the biller record.
        :param bank: ``res.bank`` the Virtual Account code is issued by.
        :type bank: :class:`odoo.models.Model`
        :param str biller_code: Virtual Account code issued by the bank.
        :return: The created ``va_biller`` record.
        :rtype: :class:`odoo.models.Model`
        """
        return cls.env["va_biller"].create(
            {
                "name": name,
                "code": "/",
                "bank_code_ids": [
                    (
                        0,
                        0,
                        {
                            "bank_id": bank.id,
                            "biller_code": biller_code,
                        },
                    )
                ],
            }
        )

    @classmethod
    def _create_merchant(cls, name, biller, merchant_code):
        """Create a ``va_biller_merchant`` registered under ``biller``.

        The biller code line is what makes the merchant selectable in
        the Generate VA wizard, whose Merchant domain only offers
        merchants registered for the selected biller.

        :param str name: Name of the merchant record.
        :param biller: ``va_biller`` the merchant is registered under.
        :type biller: :class:`odoo.models.Model`
        :param str merchant_code: Merchant code for that biller-bank
            combination.
        :return: The created ``va_biller_merchant`` record.
        :rtype: :class:`odoo.models.Model`
        """
        return cls.env["va_biller_merchant"].create(
            {
                "name": name,
                "code": "/",
                "biller_code_ids": [
                    (
                        0,
                        0,
                        {
                            "biller_id": biller.bank_code_ids[0].id,
                            "merchant_code": merchant_code,
                        },
                    )
                ],
            }
        )

    @classmethod
    def _create_generator(cls, biller, merchant=None):
        """Create a draft ``va_generator`` acted on by a tour.

        The document is left in ``draft`` -- the state both the edit
        and the delete IK require -- and gets one source data line for
        the tour partner, mirroring what the Generate VA wizard would
        have produced.

        :param biller: ``va_biller`` of the document; its name is what
            identifies the document's row in the tree view.
        :type biller: :class:`odoo.models.Model`
        :param merchant: Optional ``va_biller_merchant`` of the
            document.
        :type merchant: :class:`odoo.models.Model` or None
        :return: The created ``va_generator`` record.
        :rtype: :class:`odoo.models.Model`
        """
        return cls.env["va_generator"].create(
            {
                "type_id": cls.type_alpha.id,
                "bank_id": biller.bank_code_ids[0].bank_id.id,
                "biller_id": biller.id,
                "merchant_id": merchant and merchant.id or False,
                "usage_id": cls.usage_alpha.id,
                "exporter_id": cls.exporter_alpha.id,
                "source_data_ids": [
                    (
                        0,
                        0,
                        {
                            "model_id": cls.model_res_partner.id,
                            "res_id": cls.partner.id,
                        },
                    )
                ],
            }
        )

    def test_create(self):
        """Run the create tour for ``va_generator``.

        The third Post-Condition bullet -- the document number is still
        ``/`` -- is not asserted by the tour: it is a field value, and
        reading values is outside the scope of a tour. The sequence
        behaviour behind it is covered by the unit tests in
        ``tests/test_data_va_generator.yaml``.

        IK: docs/va_generator/01-create.md
        """
        self.start_tour("/web", "ssi_va_va_generator_create", login="admin")

    def test_edit(self):
        """Run the edit tour for ``va_generator``.

        The tour changes Generator Type, Bank Account Usage and
        Exporter. It deliberately does not change Bank: the only thing
        that sub-bullet of Flow 3 produces on screen is Biller and
        Merchant becoming empty -- two field values, which belong to
        the unit tests. That effect is covered there by the "Changing
        bank_id on the form resets biller_id and merchant_id" scenario
        of ``tests/test_data_va_generator.yaml``.

        IK: docs/va_generator/02-edit.md
        """
        self.start_tour("/web", "ssi_va_va_generator_edit", login="admin")

    def test_delete(self):
        """Run the delete tour for ``va_generator``.

        IK: docs/va_generator/03-delete.md
        """
        self.start_tour("/web", "ssi_va_va_generator_delete", login="admin")
