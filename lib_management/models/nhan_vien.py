# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class NhanVien(models.Model):
    _name = 'nhan.vien'
    _rec_name = 'name'
    _description = 'Nhân viên thư viện'


    name = fields.Char(string='Tên nhân viên')
    img = fields.Binary(string='Hình ảnh')
    gioi_tinh = fields.Selection([('nam','Nam'),('nu','Nữ')], string='Giới tính')
    nam_sinh = fields.Date(string='Năm sinh')
    dia_chi = fields.Text(string='Địa chỉ')
    note = fields.Html(string='Giới thiệu về nhân viên')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
