from odoo import models, fields
import datetime
import io
import base64
import xlwt

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def excel_style(row, col):
    """ Convert given row and column number to an Excel-style cell name. """
    result = []
    while col:
        col, rem = divmod(col - 1, 26)
        result[:0] = LETTERS[rem]
    return ''.join(result) + str(row)


class InventoryValuationReport(models.AbstractModel):
    _name = 'report.inventory_valuation.report.report.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wiz):

        heading_format = workbook.add_format({'align': 'center',
                                              'valign': 'vcenter',
                                              'bold': True, 'size': 15,
                                              # 'bg_color': '#0077b3',
                                              })
        sub_heading_format = workbook.add_format({'align': 'center',
                                                  'valign': 'vcenter',
                                                  'bold': True, 'size': 11,
                                                  'bg_color': '#808080',
                                                  # 'font_color': '#808080'
                                                  'font_color': '#FFFFFF'
                                                  })

        col_format = workbook.add_format({'valign': 'left',
                                          'align': 'left',
                                          'bold': True,
                                          'size': 10,
                                          'font_color': '#000000'
                                          })
        data_format = workbook.add_format({'valign': 'center',
                                           'align': 'center',
                                           'size': 10,
                                           'font_color': '#000000'
                                           })

        col_format.set_text_wrap()
        worksheet = workbook.add_worksheet('Inventory Valuation')
        worksheet.set_column('A:A', 40)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 15)
        worksheet.set_column('G:G', 25)

        row = 1
        worksheet.set_row(1, 20)
        starting_col = excel_style(row, 1)
        ending_col = excel_style(row, 7)
        worksheet.merge_range('%s:%s' % (starting_col, ending_col),
                              'Inventory Valuation',
                              heading_format)
        row = row + 1
        if wiz.section:
            categories = []
            categories_wiz = wiz.section
            for categ in categories_wiz:
                if not categ.child_id:
                    if categ not in categories:
                        categories.append(categ)
                for child in categ.child_id:
                    if child not in categories:
                        categories.append(child)
        else:
            categories = self.env['product.category'].search([])
        for category in categories:
            products = self.env['product.product'].search(
                [('categ_id', '=', category.id)])
            if products:
                flag = False
                row = row + 1
                head = row
                row = row + 1
            for product in products:
                lots = self.env['stock.production.lot'].search(
                    [('product_id', '=', product.id)])
                if not lots and product.qty_available > 0:
                    flag = True
                    worksheet.write(row, 0, product.name, data_format)
                    worksheet.write(row, 2, product.qty_available, data_format)
                    worksheet.write(row, 3, product.standard_price, data_format)
                    worksheet.write(row, 4, product.list_price, data_format)
                    worksheet.write(row, 5, product.qty_available * product.standard_price, data_format)
                    worksheet.write(row, 6, product.qty_available * product.list_price, data_format)
                    row = row + 1
                for lot in lots:
                    if lot.product_qty > 0:
                        flag = True
                        worksheet.write(row, 0, product.name, data_format)
                        worksheet.write(row, 1, lot.name, data_format)
                        worksheet.write(row, 2, lot.product_qty, data_format)
                        worksheet.write(row, 3, product.standard_price, data_format)
                        worksheet.write(row, 4, lot.sale_price, data_format)
                        worksheet.write(row, 5, lot.product_qty * product.standard_price, data_format)
                        worksheet.write(row, 6, lot.product_qty * lot.sale_price, data_format)
                        row = row + 1
                if flag:
                    starting_col = excel_style(head, 1)
                    ending_col = excel_style(head, 7)
                    worksheet.merge_range('%s:%s' % (starting_col, ending_col),
                                          category.name,
                                          heading_format)
                    worksheet.write(head, 0, 'Products', sub_heading_format)
                    worksheet.write(head, 1, "Lots", sub_heading_format)
                    worksheet.write(head, 2, "Qty", sub_heading_format)
                    worksheet.write(head, 3, "Cost", sub_heading_format)
                    worksheet.write(head, 4, "Sale Price", sub_heading_format)
                    worksheet.write(head, 5, "Inventory Value", sub_heading_format)
                    worksheet.write(head, 6, "Sales Value", sub_heading_format)
