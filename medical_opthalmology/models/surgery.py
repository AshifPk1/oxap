from odoo import models, fields


class Surgery(models.Model):
    _inherit = 'medical.opthalmology'

    surgery_items_ids = fields.One2many('surgery.items', 'patient_visit_id', string='Surgery Items')
    assistance = fields.Char('Assistance In Surgery')
    types_of_anesthesia = fields.Selection([('la', 'LA'), ('ga', 'GA')], string='Types Of Anesthesia')
    surgery_selection = fields.Selection([
        ('primary', 'Primary')
    ])
    eye_selection = fields.Selection([
        ('left', 'Left'),
        ('right', 'Right')
    ])
    surgery_done_date = fields.Date('Date')
    surgeon_ids = fields.Many2many('medical.practitioner', string='Surgeons')
    anesthesia = fields.Boolean('Anesthesia')
    anesthetist = fields.Many2one('medical.practitioner', string='Anesthetist')

    incision = fields.Selection([
        ('scelarel_tunnel', 'Scelaral Tunnel'),
        ('corneal', 'Corneal'),
        ('temporal', 'Temporal'),
        ('superior', 'Superior')
    ])
    incision_measure = fields.Float(' ')

    capsulorrhexis = fields.Selection([
        ('trypan_blue', 'Trypan Blue')
    ])
    instrument_used = fields.Text('Instrument used')

    hydroprocedures = fields.Selection([
        ('hydrodissection', 'Hydrodissection'),
        ('hydrodelamination', 'Hydrodelamination')
    ])
    nucleus_managment_technique = fields.Text()
    nucleus_managment_technique_selection = fields.Selection([
        ('phaco', 'Phaco'),
        ('sics', 'SICS')
    ])
    intracameral = fields.Selection([
        ('pilocarpine', 'Pilocarpine'),
        ('air', 'Air')
    ])
    cortical_aspiration = fields.Selection([
        ('automated', 'Automated'),
        ('simcoe', 'Simcoe')
    ])
    iol_sel = fields.Selection([
        ('rigid', 'Rigid'),
        ('foldable', 'Foldable'),
        ('bifocal', 'Bifocal'),
        ('multifocal', 'Multifocal')
    ])
    iol_details = fields.Text('IOL Details')
    summary = fields.Text('Summary')

    def confirm_surgery(self):
        self.write({'state': 'done'})

        view = self.env.ref('medical_opthalmology.surgery_tree').ids
        form_view_id = self.env.ref('medical_opthalmology.view_surgery_form').ids

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'medical.opthalmology',
            'views': [[view, 'tree'], [form_view_id, 'form']],
            'target': 'current',
        }
