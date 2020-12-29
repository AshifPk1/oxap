from odoo import api, models, fields, _


class IOLStage(models.Model):
    _inherit = 'medical.opthalmology'
    _order = 'id desc'

    @api.model
    def default_iol_le_values(self):
        iol_list = ['_', '_', '_', '_', '_', '_', '_']
        ids = []
        for item in iol_list:
            data = {
                'iol': item
            }
            ids.append((0, 0, data))
        return ids

    @api.model
    def default_iol_re_values(self):
        iol_list = ['_', '_', '_', '_', '_', '_', '_']
        ids = []
        for item in iol_list:
            data = {
                'iol': item
            }
            ids.append((0, 0, data))
        return ids

    @api.model
    def default_axl_values(self):
        axl_list = ['_']
        ids = []
        for item in axl_list:
            data = {
                'axl': item
            }
            ids.append((0, 0, data))
        return ids

    @api.model
    def default_axl_re_values(self):
        axl_list = ['_']
        ids = []
        for item in axl_list:
            data = {
                'axl': item
            }
            ids.append((0, 0, data))
        return ids

    iol_le_ids = fields.One2many('optical.iol', 'patient_visit_id', string='IOL', default=default_iol_le_values)
    iol_re_ids = fields.One2many('optical.iol', 'patient_visit_re_id', string='IOL', default=default_iol_re_values)

    calculated_power_le = fields.Char('Calculated Power')
    calculated_power_re = fields.Char('Calculated Power')

    iol_text = fields.Text('IOL TEXT')

    acd_le = fields.Char('ACD LE')
    acd_re = fields.Char('ACD RE')

    duct_le = fields.Char('Duct_le')
    duct_re = fields.Char('Duct_re')

    axl_le_ids = fields.One2many('optical.axl', 'patient_visit_id', string='Axl', default=default_axl_values)
    axl_re_ids = fields.One2many('optical.axl', 'patient_visit_re_id', string='Axl', default=default_axl_re_values)

    def confirm_iol(self):
        self.iol_status = True
        self.write({'state': 'counselling'})
        record = self.env['counselling.substate'].search([('name', '=', 'CS2')], limit=1)
        self.sub_state_id = record.id
        view = self.env.ref('medical_opthalmology.iol_confirming_tree')
        return {
            'name': _('Warning'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'medical.opthalmology',
            'views': [(view.id, 'tree')],
            'view_id': view.id,
            'target': 'current',
        }

    def print_iol_details(self):

        return self.env.ref('medical_opthalmology.iol_detail_template').report_action(self)
