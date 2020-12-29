# -*- coding: utf-8 -*-

import html2text
from odoo import models, fields, _


class ConvertHtmlText(object):

    def convert_html_to_text(result_txt):
        capt = b'%s' % (result_txt)
        convert_byte_to_str = capt.decode('utf-8')
        return html2text.html2text(convert_byte_to_str)


class MedicalOptics(models.Model):
    _inherit = 'medical.optics'

    delivery_date = fields.Date('Delivery Date')


    def send_whatsapp_step_one(self):
        # record = self.with_context(proforma=True)
        message_txt = ''
        templates = self.env['whatsapp.default'].search([('active', '=', True), ('category', '=', 'optics')])
        if templates:
            message_txt = templates[0].default_messege

        # message_txt = ConvertHtmlText.convert_html_to_text(result_txt)

        return {'type': 'ir.actions.act_window',
                'name': _('Send Whatsapp'),
                'res_model': 'send.whatsapp',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_partner_id': self.patient_id.id, 'message_txt': message_txt,
                            'default_optics_id': self.id,
                            'format_invisible': True,'default_template_messege_id': templates.id},
                }
