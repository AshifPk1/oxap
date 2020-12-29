from odoo import api, models, fields


class Refarction2(models.Model):
    _inherit = 'medical.opthalmology'

    @api.model
    def cyclo_l_values(self):
        cyclo_list_le = ['_', '_', '_']
        ids = []
        for item in cyclo_list_le:
            data = {
                'head': item
            }
            ids.append((0, 0, data))
        return ids

    cyclo_ar_l_ids = fields.One2many('cyclo.details', 'patient_visit_id', string='Cyclo Left', default=cyclo_l_values)

    @api.model
    def cyclo_r_values(self):
        cyclo_list_re = ['_', '_', '_']
        ids = []
        for item in cyclo_list_re:
            data = {
                'head': item
            }
            ids.append((0, 0, data))
        return ids

    cyclo_ar_r_ids = fields.One2many('cyclo.details', 'patient_visit_re_id', string='Cyclo Right',
                                     default=cyclo_r_values)

    @api.model
    def alternate_glass_l_values(self):
        cyclo_list_re = ['_', '_']
        ids = []
        for item in cyclo_list_re:
            data = {
                'head': item
            }
            ids.append((0, 0, data))
        return ids

    alternate_glass_l_ids = fields.One2many('alternate.glass', 'patient_visit_id', string='Alternate Glass Left',
                                            default=alternate_glass_l_values)

    @api.model
    def alternate_glass_r_values(self):
        cyclo_list_re = ['_', '_']
        ids = []
        for item in cyclo_list_re:
            data = {
                'head': item
            }
            ids.append((0, 0, data))
        return ids

    alternate_glass_r_ids = fields.One2many('alternate.glass', 'patient_visit_re_id', string='Alternate Glass Right',
                                            default=alternate_glass_r_values)

    text_box = fields.Text(default=' ')

    convergence = fields.Selection([
        ('full', 'Full'),
        ('adequate', 'Adequate'),
        ('decreased', 'Decreased')])
    npc = fields.Integer('NPC', default=0)
    dist = fields.Char('Dist', default=0)
    near = fields.Char('Near', default=0)
    mobility = fields.Char('Mobility', default=0)
    bsv = fields.Char('BSV', default=0)
    smp = fields.Text(string=' ')
    subjective = fields.Float('')
    objective = fields.Float('')
    selection_refraction_3 = fields.Selection([
        ('registration', 'Registration'),
        ('waiting', 'Waiting')], default='waiting')
    selection_refraction_4 = fields.Selection([
        ('registration', 'Registration'),
        ('waiting', 'Waiting')], default='waiting')
    steriopsis = fields.Selection([
        ('normal', 'Normal'),
        ('ab_normal', 'Abnormal'),
        ('gross', 'Gross')])
    range = fields.Float('')
    make_point = fields.Float('')
    make_point_2 = fields.Float('')
    break_point = fields.Float('')
    break_point_2 = fields.Float('')
