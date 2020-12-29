# -*- coding: utf-8 -*-

import logging
import re
import urllib

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class WhatsappDefault(models.Model):
    _name = 'whatsapp.default'
    _description = 'Message default in Whatsapp'

    name = fields.Char(string="Title Template")
    default_messege = fields.Text(string="Message Default")
    category = fields.Selection([('partner', 'Partner/Contact'),
                                 ('registration', 'Registration'),
                                 ('medication', 'Medication Details'),
                                 ('optics', 'Optics'),
                                 ('other', 'Other'), ], default='other', string="Category")
    active = fields.Boolean('Active')


class SendWhatsapp(models.TransientModel):
    _name = 'send.whatsapp'
    _description = 'Send Whatsapp'

    partner_id = fields.Many2one('medical.patient', 'Patient')
    template_messege_id = fields.Many2one('whatsapp.default',
                                          domain=[('active', '=', True), ('category', '=', 'registration')])

    name = fields.Char(related='partner_id.name', required=True, readonly=True)
    mobile = fields.Char(related='partner_id.phone', required=True, readonly=True,
                         help="use country mobile code without the + sign")
    format_message = fields.Selection([('txt', 'Text Plan'),
                                       ('link', 'Link Url'),
                                       ], default='txt', string="Format Message")
    message = fields.Text(string="Message", required=True)
    format_visible_context = fields.Boolean(default=False)
    opthalmology_id = fields.Many2one('medical.opthalmology', string='Opthalmology')
    optics_id = fields.Many2one('medical.optics', string='Opticals')

    @api.multi
    @api.onchange('partner_id')
    def __onchange_partner_id(self):
        self.format_visible_context = self.env.context.get('format_invisible', False)
        self.mobile = self.partner_id.phone or self.partner_id.mobile

    @api.onchange('format_message')
    def _onchange_type(self):

        if self.format_message == 'txt' or self.env.context.get('format_invisible'):
            self.message = self.env.context.get('message_txt', False)
        if self.format_message == 'link':
            self.message = self.env.context.get('message_link', False)

    @api.onchange('template_messege_id')
    def _onchange_message(self):

        message = self.template_messege_id.default_messege
        include_data = str(message).format(patient_name=self.partner_id.name,
                                           file_number=self.partner_id.identification_code,
                                           doctor_name=self.opthalmology_id.doctor_id.name,
                                           registration_amount=self.opthalmology_id.registration_amount,
                                           admission_date=self.opthalmology_id.date,
                                           patient_city=self.opthalmology_id.city)

        if message:
            self.message = include_data

    @api.multi
    def close_dialog(self):
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def send_dialog(self, whatsapp_url):
        action = {'type': 'ir.actions.act_url', 'url': whatsapp_url, 'target': 'new', 'res_id': self.id}

    def send_whatsapp(self):
        if not self.mobile:
            raise ValidationError(_("You must add mobil number or phone in the partner form"))
        else:
            movil = self.mobile
            array_int = re.findall("\d+", movil)
            whatsapp_number = ''.join(str(e) for e in array_int)
            if len(whatsapp_number) < 10:
                raise ValidationError(_("Please Check The Number"))
            if len(whatsapp_number) == 10:
                whatsapp_number = '91' + whatsapp_number
            messege_prepare = u'{}'.format(self.message)

            messege_encode = urllib.parse.quote(messege_prepare.encode('utf8'))
            # whatsapp_url = 'https://wa.me/{}?text={}'.format(whatsapp_number, messege_encode)
            whatsapp_url = 'https://web.whatsapp.com/send?phone={}&text={}&source&data&app_absent'.format(
                whatsapp_number, messege_encode)
            print(whatsapp_url)
            return {'type': 'ir.actions.act_url',
                    'url': whatsapp_url,
                    'nodestroy': True,
                    'target': 'new',
                    'res_id': self.id
                    }
