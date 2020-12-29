from odoo import models, fields, api, _


class CounsellingSubStates(models.Model):
    _name = 'counselling.substate'
    _rec_name = 'stage_name'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'stage_name' in vals:
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'counselling.substate') or _('New')
        return super(CounsellingSubStates, self).create(vals)

    name = fields.Char(string='Sub State No', required=True, copy=False, readonly=True, ondelete='cascade', index=True,
                       default=lambda self: _('New'))
    stage_name = fields.Char('Stage Name')
    requirements = fields.Text('Requirements', help="Enter here the internal requirements for this stage.")
    is_start = fields.Boolean('Starting Stage')
