# -*- coding: utf-8 -*-

import html2text
from odoo import models, _


class ConvertHtmlText(object):

    def convert_html_to_text(result_txt):
        capt = b'%s' % (result_txt)
        convert_byte_to_str = capt.decode('utf-8')
        return html2text.html2text(convert_byte_to_str)


class MedicalOpthalmology(models.Model):
    _inherit = 'medical.opthalmology'

    def send_whatsapp_step_one(self):
        message_txt = ''
        templates = self.env['whatsapp.default'].search([('active', '=', True), ('category', '=', 'registration')])
        ctx = {'default_partner_id': self.patient_id.id, 'message_txt': message_txt, 'default_opthalmology_id': self.id,
               'format_invisible': True}
        if templates:
            message_txt = templates[0].default_messege
            ctx['default_template_messege_id'] = templates[0].id
            ctx['message_txt'] = message_txt
        if self.patient_id:
            ctx['mobile'] = self.patient_id.phone or self.patient_id.mobile
        return {'type': 'ir.actions.act_window',
                'name': _('Send Whatsapp'),
                'res_model': 'send.whatsapp',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': ctx,
                }
