from odoo import models, fields, api
from datetime import date


class Product(models.Model):
    _inherit = 'product.template'

    minimum_qty = fields.Integer(string='Minimum Quantity', default=10,
                                 help='When stock on hand falls below this number, it will be included in the low '
                                      'stock report. Set to -1 to exclude from the report.')
    is_stock_low = fields.Boolean(compute='_compute_is_stock_low')
    minimal_qty_notification = fields.Boolean('Minimal Quantity Notification')

    @api.multi
    @api.depends('minimum_qty', 'qty_available')
    def _compute_is_stock_low(self):
        for rec in self:
            if rec.qty_available <= rec.minimum_qty:
                rec.is_stock_low = True

    def send_low_stock_via_email(self):

        header_label_list = ["S.No:", "Name", "Qty On Hand ", "Minimum Quantity"]
        product_obj = self.env['product.product']
        product_ids = product_obj.search([('minimal_qty_notification','=',True)])
        print(product_ids,'product_idsproduct_ids')
        serial = 1
        # product_ids = product_ids.filtered(
        #     lambda r: r.qty_available <= r.minimum_qty and r.minimum_qty >= 0)
        product_category = self.env['product.category'].search([('child_id', '=', False), ('product_count', '!=', 0)])
        group = self.env.ref('stock.group_stock_manager')
        print(group)
        recipients = []
        body = ""
        for recipient in group.users:
            recipients.append((4, recipient.partner_id.id))
        # Notification message body

        for category in product_category:
            filtered_product_ids = product_ids.filtered(
                lambda r: r.qty_available <= r.minimum_qty and r.minimum_qty >= 0 and r.categ_id.id == category.id)

            if not filtered_product_ids:
                continue
            body += """ 
            
            <h2>%s<h2>
            <table class="table table-bordered">
                <tr style="font-size:14px; border: 1px solid black">
                    <th style="text-align:center; border: 1px solid black">%s</th>
                    <th style="text-align:center; border: 1px solid black">%s</th>
                    <th style="text-align:center; border: 1px solid black">%s</th>
                    <th style="text-align:center; border: 1px solid black">%s</th>
                    </tr>
                 """ % (category.display_name, header_label_list[0], header_label_list[1], header_label_list[2],
                        header_label_list[3])
            for product_id in filtered_product_ids:
                body += """ 
                    <tr style="font-size:14px; border: 1px solid black">
                        <td style="text-align:center; border: 1px solid black">%s</td>
                        <td style="text-align:center; border: 1px solid black">%s</td>
                        <td style="text-align:center; border: 1px solid black">%s</td>
                        <td style="text-align:center; border: 1px solid black">%s</td>
                    </tr>
                    """ % (serial, product_id.name, product_id.qty_available, product_id.minimum_qty)
                serial += 1
            body += """</table>"""
            serial = 1
        post_vars = {
            'body': body,
            'partner_ids': recipients,
            'subject': "Low stock notification",
            }

        partner_id = self.env.user.partner_id
        MailThread = self.env['mail.thread']
        thread_pool = self.env['mail.message'].create(post_vars)
        thread_pool.needaction_partner_ids = [(6, 0, [partner_id.id])]
        self.message_post(

            type="notification",
            subtype="mt_comment",
            **post_vars)
