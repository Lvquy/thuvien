# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class BaoCao(models.Model):
    _name = 'bao.cao'
    _rec_name = 'name'
    _description = 'Báo cáo thống kê'

    name = fields.Char(string='Name')
    company_id = fields.Many2one(
        'res.company', 'Trường học', readonly=True, index=1, default=lambda self: self.env.user.company_id.id)
    total_sach = fields.Integer(string='Tổng số đầu sách')
    total_serial = fields.Integer(string='Tổng số sách')
    total_sach_muon = fields.Integer(string='Số sách đang cho mượn')
    total_sach_trong_kho = fields.Integer(string='Số sách đang trong kho')
    total_sach_phe = fields.Integer(string='Số sách đã báo phế')
    total_doc_gia = fields.Integer(string='Tổng số độc giả')
