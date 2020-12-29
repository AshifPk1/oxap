from odoo import models, fields


class AccountJournal(models.Model):
    _inherit = "account.journal"

    default_journal = fields.Boolean('Default Journal', default=False)
