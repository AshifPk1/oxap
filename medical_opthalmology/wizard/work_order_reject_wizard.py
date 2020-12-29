
from odoo import models, fields, api



class RegistrationWarningWizard(models.TransientModel):
    _name = 'work.order.reject.wizard'

    optics_id=fields.Many2one('medical.optics',string="Optics Id")
    reject_reason=fields.Many2one('work.order.reject.reason',string="Reason",required=True)
    sales_person_id = fields.Many2one('hr.employee', string='Sales Person',required=True)


    @api.multi
    def reject_work_order(self):

        if self.optics_id:
            self.optics_id.reject_reason=self.reject_reason.id
            self.optics_id.sales_person_id = self.sales_person_id.id
            self.optics_id.write({
                'state':'done'
            })

