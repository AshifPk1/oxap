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
    _name = 'report.patient_list.report.report.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wiz):

        heading_format = workbook.add_format({'align': 'center',
                                              'valign': 'vcenter',
                                              'bold': True, 'size': 15,
                                              # 'bg_color': '#0077b3',
                                              })
        sub_heading_format = workbook.add_format({'align': 'left',
                                                  'valign': 'vcenter',
                                                  'bold': False, 'size': 12,
                                                  # 'bg_color': '#808080',
                                                  # 'font_color': '#808080'
                                                  'font_color': '#000000'
                                                  })

        sub_heading_format_1 = workbook.add_format({'align': 'left',
                                                    'valign': 'vcenter',
                                                    'bold': True, 'size': 13,
                                                    # 'bg_color': '#E1F5FE',
                                                    'font_color': '#000000'
                                                    })

        col_format = workbook.add_format({'valign': 'left',
                                          'align': 'left',
                                          'bold': True,
                                          'size': 10,
                                          'font_color': '#000000'
                                          })
        doctor_id = wiz.doctor_id.id
        from_date = wiz.date_from + ' ' + '00:00:00'
        to_date = wiz.date_to + ' ' + '23:59:59'

        col_format.set_text_wrap()
        worksheet = workbook.add_worksheet('Patient List')
        worksheet.set_column('A:A', 40)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 25)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 15)

        row = 1
        worksheet.set_row(1, 20)
        starting_col = excel_style(row, 1)
        ending_col = excel_style(row, 6)
        worksheet.merge_range('%s:%s' % (starting_col, ending_col),
                              'PATIENT LIST',
                              heading_format)
        row = row + 1
        worksheet.write(row, 0, "Doctor", sub_heading_format_1)
        worksheet.write(row, 1, wiz.doctor_id.name, sub_heading_format_1)
        row = row + 1
        worksheet.write(row, 0, "Doctor CODE", sub_heading_format_1)
        worksheet.write(row, 1, wiz.doctor_id.code, sub_heading_format_1)
        row = row + 1

        worksheet.write(row, 0, "Date From", sub_heading_format_1)
        worksheet.write(row, 1, wiz.date_from, sub_heading_format_1)
        row = row + 1
        worksheet.write(row, 0, "Date To", sub_heading_format_1)
        worksheet.write(row, 1, wiz.date_to, sub_heading_format_1)
        row = row + 1
        new_patients = 0
        old_patients = 0
        patient_above_fifty = 0
        total_patients = self.env['medical.opthalmology'].search_count([('doctor_id', '=', doctor_id),
                                                                        ('date', '>=', from_date),
                                                                        ('date', '<=', to_date), ])

        records = self.env['medical.opthalmology'].search([('doctor_id', '=', doctor_id),
                                                           ('date', '>=', from_date),
                                                           ('date', '<=', to_date), ])

        for r in records:
            if (r.new_patient_is):
                new_patients = new_patients + 1

            else:
                old_patients = old_patients + 1

            if (r.age_in_float >= 50):
                patient_above_fifty = patient_above_fifty + 1

        referred_to_opticals = self.env['medical.opthalmology'].search_count(
            [('id', 'in', records.ids), ('send_to_optics', '=', True)])
        referred_to_counselling = self.env['medical.opthalmology'].search_count(
            [('id', 'in', records.ids), ('referred_to_surgery', '=', True)])

        work_orders = self.env['optics.work.order'].search_count([('doctor_id', '=', doctor_id),
                                                                  ('date', '>=', from_date),
                                                                  ('date', '<=', to_date),
                                                                  ])
        pharmacy_record = self.env['medical.pharmacy'].search_count([('doctor_id', '=', doctor_id),
                                                                     ('date', '>=', from_date),
                                                                     ('date', '<=', to_date),
                                                                     ])

        row = row + 1
        worksheet.write(row, 0, "NO OF PATIENTS", sub_heading_format)
        worksheet.write(row, 1, total_patients, sub_heading_format)
        row = row + 1
        worksheet.write(row, 0, "OLD PATIENTS", sub_heading_format)
        worksheet.write(row, 1, old_patients, sub_heading_format)
        row = row + 1
        worksheet.write(row, 0, "NEW PATIENTS", sub_heading_format)
        worksheet.write(row, 1, new_patients, sub_heading_format)
        row = row + 1
        worksheet.write(row, 0, "ABOVE  50+ ", sub_heading_format)
        worksheet.write(row, 1, patient_above_fifty, sub_heading_format)
        row = row + 1
        worksheet.write(row, 0, "REFERRED TO OPTICAL", sub_heading_format)
        worksheet.write(row, 1, referred_to_opticals, sub_heading_format)
        row = row + 1

        worksheet.write(row, 0, "WORK ORDER CREATED", sub_heading_format)
        worksheet.write(row, 1, work_orders, sub_heading_format)
        row = row + 1
        worksheet.write(row, 0, "PHARMACY PRESCRIBED ", sub_heading_format)
        worksheet.write(row, 1, pharmacy_record, sub_heading_format)
        row = row + 1
        worksheet.write(row, 0, "REFERRED TO COUNSELLING", sub_heading_format)
        worksheet.write(row, 1, referred_to_counselling, sub_heading_format)

        patients = self.env['medical.opthalmology'].search([('doctor_id', '=', doctor_id),
                                                            ('date', '>=', from_date),
                                                            ('date', '<=', to_date),
                                                            ])

        categories = self.env['patient.visit.tag'].search([])
        a = []
        b = []
        for i in categories:
            number = 0
            a.append(i.id)
        for patient in patients:
            for rec in patient.tag_ids:
                b.append(rec.name)
        my_dict = {i: b.count(i) for i in b}
        for i in my_dict:
            row = row + 1
            worksheet.write(row, 0, i, sub_heading_format)
            worksheet.write(row, 1, my_dict[i], sub_heading_format)
