# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    sale_value = fields.Float("Sales Value", compute='compute_sales_value')

    @api.depends('qty_available', 'lst_price')
    def compute_sales_value(self):
        for rec in self:
            rec.sale_value = rec.qty_available * rec.lst_price

    @api.multi
    def _sales_count(self):
        r = {}
        if not self.user_has_groups('sales_team.group_sale_salesman'):
            return r
        domain = [
            ('state', 'in', ['sale', 'done', 'paid']),
            ('product_id', 'in', self.ids),
        ]
        for group in self.env['sale.report'].read_group(domain, ['product_id', 'product_uom_qty'], ['product_id']):
            r[group['product_id'][0]] = group['product_uom_qty']
        for product in self:
            product.sales_count = r.get(product.id, 0)
        return r

    sales_count = fields.Integer(compute='_sales_count', string='# Sales')

    def _get_invoice_policy(self):
        return self.invoice_policy


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_surgery_package = fields.Boolean('Surgery Packages')
    is_investigations = fields.Boolean('Investigations')
    is_surgery_lens = fields.Boolean('Surgery Lens')
    is_lens = fields.Boolean('Lens')
    is_frame = fields.Boolean('Frames')
    is_pharmacy = fields.Boolean('Pharmacy')
    is_registration_product = fields.Boolean(default=False, string='Registration Product')
    power = fields.Char('Power')
    item = fields.Char('Item')
    rate = fields.Float('Amount')
    generic_name_id = fields.Many2one('generic.name', "Generic Name")
    brand = fields.Char('Brand')

    @api.multi
    def action_view_sales(self):
        self.ensure_one()
        action = self.env.ref('sale.action_product_sale_list')
        product_ids = self.with_context(active_test=False).product_variant_ids.ids

        return {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'target': action.target,
            'context': "{'default_product_id': " + str(product_ids[0]) + "}",
            'res_model': action.res_model,
            'domain': [('state', 'in', ['sale', 'done', 'paid']), ('product_id.product_tmpl_id', '=', self.id)],
        }

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain_name = ['|', '|', ('name', 'ilike', name), ('default_code', 'ilike', name), ('generic_name_id', 'ilike', name)]
        recs = self.search(domain_name + args, limit=limit)
        return recs.name_get()
