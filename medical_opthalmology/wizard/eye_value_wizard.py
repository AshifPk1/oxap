from odoo import models, api, fields


class EyeValueWizard(models.TransientModel):
    _name = 'eye.values.wizard'

    eye_value_ids_le = fields.Many2many('eye.value', string="Eye Values")

    eye_value_ids_me = fields.Many2many('eye.value_me', string="Eye Values")

    eye_value_ids_re = fields.Many2many('eye.value_re', string="Eye Values")

    eye_value_ids_re_2 = fields.Many2many('eye.value_re_2', string="Eye Values")

    sphere = fields.Boolean('SPH ACTIVE')

    cyl = fields.Boolean('CYL ACTIVE')

    va = fields.Boolean('VA ACTIVE')

    axis = fields.Boolean('AXIS ACTIVE')

    @api.multi
    def run(self):
        flag = 0
        line_rec = self.env[self._context['active_model']].search([('id', '=', self._context.get('active_id'))])
        for records in self.eye_value_ids_le:
            if records:
                flag = 1
                if self.sphere:
                    line_rec.sphere = records.name
                    break
                if self.cyl:
                    line_rec.cyl = records.name
                    break
                if self.va:
                    line_rec.va = records.name
                    break
                if self.axis:
                    line_rec.axis = records.name
                    break
        if flag == 0:
            for records in self.eye_value_ids_me:
                if records:
                    flag = 1
                    if self.sphere:
                        line_rec.sphere = records.name
                        break
                    if self.cyl:
                        line_rec.cyl = records.name
                        break
                    if self.va:
                        line_rec.va = records.name
                        break
                    if self.axis:
                        line_rec.axis = records.name
                        break
        if flag == 0:
            for records in self.eye_value_ids_re:
                if records:
                    flag = 1
                    if self.sphere:
                        line_rec.sphere = records.name
                        break
                    if self.cyl:
                        line_rec.cyl = records.name
                        break
                    if self.va:
                        line_rec.va = records.name
                        break
                    if self.axis:
                        line_rec.axis = records.name

        if flag == 0:
            for records in self.eye_value_ids_re_2:
                if records:
                    flag = 1
                    if self.sphere:
                        line_rec.sphere = records.name
                        break
                    if self.cyl:
                        line_rec.cyl = records.name
                        break
                    if self.va:
                        line_rec.va = records.name
                        break
                    if self.axis:
                        line_rec.axis = records.name
        return True


class EyeValueWizardAxis(models.TransientModel):
    _name = 'eye.values.wizard.axis'

    eye_value_ids_le = fields.Many2many('eye.value_axis', string="Eye Values")

    eye_value_ids_me = fields.Many2many('eye.value_axis_me', string="Eye Values")

    eye_value_ids_re = fields.Many2many('eye.value_axis_re', string="Eye Values")

    eye_value_ids_re_2 = fields.Many2many('eye.value_re_axis_2', string="Eye Values")

    axis = fields.Boolean('AXIS ACTIVE')

    @api.multi
    def run(self):
        flag = 0
        line_rec = self.env[self._context['active_model']].search([('id', '=', self._context.get('active_id'))])
        for records in self.eye_value_ids_le:
            if records:
                flag = 1
                if self.axis:
                    line_rec.axis = records.name
                    break
        if flag == 0:
            for records in self.eye_value_ids_me:
                if records:
                    if self.axis:
                        line_rec.axis = records.name
        if flag == 0:
            for records in self.eye_value_ids_re:
                if records:
                    flag = 1
                    if self.axis:
                        line_rec.axis = records.name

        if flag == 0:
            for records in self.eye_value_ids_re_2:
                if records:
                    flag = 1
                    if self.axis:
                        line_rec.axis = records.name
        return True


class EyeValueWizardVa(models.TransientModel):
    _name = 'eye.values.wizard.va'

    eye_value_ids_le = fields.Many2many('eye.value_va', string="Eye Values")

    eye_value_ids_me = fields.Many2many('eye.value_va_me', string="Eye Values")

    eye_value_ids_re = fields.Many2many('eye.value_va_re', string="Eye Values")

    eye_value_ids_re_2 = fields.Many2many('eye.value_re_va_2', string="Eye Values")

    eye_value_ids_nv_re = fields.Many2many('eye.value_va_nv_re', string="Eye Values")

    eye_value_ids_nv_re_2 = fields.Many2many('eye.value_nv_re_va_2', string="Eye Values")

    nv = fields.Boolean('NV')
    va = fields.Boolean('Va Active')
    le = fields.Boolean('Le ACTIVE')
    re = fields.Boolean('Re ACTIVE')

    @api.multi
    def run(self):
        flag = 0
        line_rec = self.env[self._context['active_model']].search([('id', '=', self._context.get('active_id'))])
        for records in self.eye_value_ids_le:
            if records:
                flag = 1
                if self.le:
                    line_rec.le = records.name
                    break
                if self.re:
                    line_rec.re = records.name
                    break
                if self.va:
                    line_rec.va = records.name
                    break
        if flag == 0:
            for records in self.eye_value_ids_me:
                if records:
                    if self.le:
                        line_rec.le = records.name
                        break
                    if self.re:
                        line_rec.re = records.name
                        break
                    if self.va:
                        line_rec.va = records.name
                        break
        if flag == 0:
            for records in self.eye_value_ids_re:
                if records:
                    flag = 1
                    if self.le:
                        line_rec.le = records.name
                        break
                    if self.re:
                        line_rec.re = records.name
                        break
                    if self.va:
                        line_rec.va = records.name
                        break

        if flag == 0:
            for records in self.eye_value_ids_re_2:
                if records:
                    flag = 1
                    if self.le:
                        line_rec.le = records.name
                        break
                    if self.re:
                        line_rec.re = records.name
                        break
                    if self.va:
                        line_rec.va = records.name
                        break
        return True

    @api.multi
    def run_nv(self):
        flag = 0
        line_rec = self.env[self._context['active_model']].search([('id', '=', self._context.get('active_id'))])
        for records in self.eye_value_ids_nv_re:
            if records:
                flag = 1
                if self.va:
                    print('hiii')
                    line_rec.va = records.name
                    break
        if flag == 0:
            for records in self.eye_value_ids_nv_re_2:
                if records:
                    if self.va:
                        line_rec.va = records.name
                        break

        return True
