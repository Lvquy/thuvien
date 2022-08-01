# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError

class TacGia(models.Model):
    _name = 'tac.gia'
    _rec_name = 'name'
    _description = 'Tác giả'


    name = fields.Char(stirng='Tên tác giả')
    gioi_tinh = fields.Selection([('nam','Nam'),('nu','Nữ')], string='Giới tính')
    img = fields.Binary(string='Hình ảnh')
    nam_sinh = fields.Date(string='Năm sinh')
    dia_chi = fields.Text(string='Địa chỉ')
    note = fields.Html(string='Giới thiệu về tác giả')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
