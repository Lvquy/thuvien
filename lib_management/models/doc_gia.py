# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class DocGia(models.Model):
    _name = 'doc.gia'
    _rec_name = 'name'
    _description = 'Độc giả'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Tên độc giả')
    ma_docgia = fields.Char(string='Mã độc giả')
    gioi_tinh = fields.Selection([('nam', 'Nam'), ('nu', 'Nữ')], string='Giới tính')
    img = fields.Binary(string='Hình ảnh')
    nam_sinh = fields.Date(string='Năm sinh')
    dia_chi = fields.Text(string='Địa chỉ')
    note = fields.Html(string='Ghi chú')
    lop_hoc = fields.Many2one(comodel_name='lop.hoc', string='Lớp học')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)


class LopHoc(models.Model):
    _name = 'lop.hoc'
    _rec_name = 'name'
    _description = 'Lớp học'

    name = fields.Char(string='Tên lớp')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
