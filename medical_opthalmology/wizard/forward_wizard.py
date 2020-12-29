from odoo import models, fields


class DoctorForwardWizard(models.TransientModel):
    _name = 'forward.wizard'

    forward_needed = fields.Boolean('Forward Needed')

    from_doctor_id = fields.Many2one('medical.practitioner', string='Forwarded From Doctor', ondelete='cascade')

    doctor_id = fields.Many2one('medical.practitioner', string='Forward To Doctor', required=True, ondelete='cascade')

    forward_text = fields.Text('Forward Note')

    def confirm_values(self):
        record = self.env['medical.opthalmology'].search([('id', '=', self._context['active_id'])])
        record.update(
            {
                'forward_needed': True,
                'forward_text': self.forward_text,
                'forwarded_doctor_id': self.doctor_id.id,
                'forward_status': 'forwarded',
                'doctor_id': self.doctor_id.id,
            }
        )
        view = self.env.ref('medical_opthalmology.doctor_checkup_tree').ids
        form_view_id = self.env.ref('medical_opthalmology.view_doctor_checking_form').ids

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'medical.opthalmology',
            'views': [[view, 'tree'], [form_view_id, 'form']],
            'target': 'current',
            'context': {'form_view_initial_mode': 'edit', 'create': False, 'search_default_state': 'consultation',
                        'search_default_date_today': 'date_today'},
        }
