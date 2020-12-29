from odoo import models, api, fields


class DialataionWithTPlus(models.TransientModel):
    _name = 'dialataion.tplus.wizard'

    dialataion_tplus_id = fields.Many2one('dialataion.tplus', string='Dialatation Type', required=True)
    refracted_dialatation = fields.Boolean('Refracted Dialataion')

    @api.multi
    def confirm_sent_to_dialataion(self):
        if self.dialataion_tplus_id:
            patient_visit_id = self.env['medical.opthalmology'].search([('id', '=', self._context.get('active_id'))]
                                                                       , limit=1)
            if patient_visit_id:
                patient_visit_id.update({'dialataion_tplus_id': self.dialataion_tplus_id.id})
                if not self.refracted_dialatation:
                    return patient_visit_id.sent_to_dilation()
                else:
                    return patient_visit_id.sent_to_refractive_dilation()
