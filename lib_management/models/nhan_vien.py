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
    gioi_tinh = fields.Selection([('nam', 'Nam'), ('nu', 'Nữ')], string='Giới tính')
    nam_sinh = fields.Date(string='Năm sinh')
    dia_chi = fields.Text(string='Địa chỉ')
    mobile = fields.Char(string='Điện thoại')
    note = fields.Html(string='Giới thiệu về nhân viên')
    phong_ban = fields.Many2one(comodel_name='phong.ban', string='Phòng ban',
                                domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
    truong_hoc = fields.Many2one(comodel_name='res.company',string='Thuộc trường', readonly=True,
                                 default=lambda self: self.env.user.company_id.id ,
                                 domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])


class PhongBan(models.Model):
    _name = 'phong.ban'
    _rec_name = 'name'
    _description = 'Phòng ban'

    name = fields.Char(string='Tên phòng ban')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
