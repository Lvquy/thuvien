# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class DocGia(models.Model):
    _name = 'doc.gia'
    _rec_name = 'name'
    _description = 'Độc giả'
    # _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Tên độc giả')
    ma_docgia = fields.Char(string='Mã độc giả', readonly=True, default=lambda self: 'New')
    gioi_tinh = fields.Selection([('nam', 'Nam'), ('nu', 'Nữ')], string='Giới tính')
    img = fields.Binary(string='Hình ảnh')
    nam_sinh = fields.Date(string='Năm sinh')
    dia_chi = fields.Text(string='Địa chỉ')
    note = fields.Html(string='Ghi chú')
    lop_hoc = fields.Many2one(comodel_name='lop.hoc', string='Lớp học',
                              domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    company_id = fields.Many2one(
        'res.company', 'Trường học',readonly=True, index=1, default=lambda self: self.env.user.company_id.id)
    mobile = fields.Char(string='Số điện thoại')

    @api.model
    def create(self, vals):
        global res
        if vals.get('ma_docgia', 'New' == 'New'):
            vals['ma_docgia'] = self.env['ir.sequence'].next_by_code('docgia.code') or 'New'
            res = super(DocGia, self).create(vals)
        return res


class LopHoc(models.Model):
    _name = 'lop.hoc'
    _rec_name = 'name'
    _description = 'Lớp học'

    name = fields.Char(string='Tên lớp')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
