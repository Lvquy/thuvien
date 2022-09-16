# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError



class FormPrintReport(models.TransientModel):
    _name = 'print.report'

    company_id = fields.Many2one(comodel_name='res.company', readonly=True, default=lambda  self: self.env.user.company_id.id)

    def print_report(self):
        data = {
            'company_name': self.company_id.name,
            'company_dvcq': self.company_id.dv_chu_quan,
            'company_logo': self.company_id.logo,
        }
        all_serial = self.env['serial'].search([('company_id','=',self.company_id.id)])
        serial_list = []
        for app in all_serial:
            vals = {
                'ma_sach': app.ma_sach.ma_sach,
                'serial_no': app.serial_no,
                'ten_sach': app.ten_sach,
                'tac_gia': app.ma_sach.tac_gia.name,
                'so_trang': app.ma_sach.so_trang,
                'gia_sach': app.gia_sach,
                'nha_xb': app.ma_sach.nha_xb.name,
            }
            serial_list.append(vals)
        data['all_serial'] = serial_list
        return self.env.ref('lib_management.action_report_thongtin_sach_1').report_action(self,data=data)
