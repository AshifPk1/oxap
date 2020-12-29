from odoo import models


class ResUsers(models.Model):
    _inherit = "res.users"

    def _get_group_access(self, uid):
        user = self.env['res.users'].sudo().browse(uid)
        access = "No Access"
        if user:
            if user.has_group('base.group_system'):
                access = "Manager"
            elif user.has_group('medical_opthalmology.group_doctor_access'):
                access = "Doctor"
            else:
                access = "No Access"
        return access