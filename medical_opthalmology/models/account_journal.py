from odoo import models, api,fields, _


class AccountJournal(models.Model):
    _inherit = "account.journal"

    default_journal=fields.Boolean('Default Journal',default=False)