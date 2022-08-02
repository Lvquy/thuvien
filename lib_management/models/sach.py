# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class Sach(models.Model):
    _name = 'sach.doc'
    _rec_name = 'name'
    _order = 'id desc'
    _description = 'Sách thư viện'

    name = fields.Char(string='Tên sách')
    img = fields.Binary(string='Hình ảnh')
    state = fields.Selection([('0', 'new'), ('1', 'confirm')], string='Trạng thái')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
    tac_gia = fields.Many2one(string='Tác giả', comodel_name='tac.gia',
                              domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    the_loai_sach = fields.Many2one(string='Thể loại', comodel_name='the.loai',
                                    domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    nha_xb = fields.Many2one(string='Nhà xuất bản', comodel_name='nxb',
                             domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    ke_kho = fields.Many2one(string='Kệ kho', comodel_name='ke.kho',
                             domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    ngon_ngu = fields.Many2one(string='Ngôn ngữ', comodel_name='lang',
                               domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    note = fields.Html(string='Giới thiệu ngắn')
    tinh_trang = fields.Selection([('tot', 'Tốt'), ('hong', 'Hỏng'), ('cu', 'Cũ')], string='Tình trạng', default='tot')
    so_trang = fields.Integer(string='Số trang')
    nam_xb = fields.Integer(string='Năm xuất bản')
    danh_muc_sach = fields.Many2one(comodel_name='danh.muc', string='Tên tủ sách',
                                    domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    ma_sach = fields.Char(string='Mã sách', readonly=True, default=lambda self: 'New')

    @api.model
    def create(self, vals):
        global res
        if vals.get('ma_sach', 'New' == 'New'):
            vals['ma_sach'] = self.env['ir.sequence'].next_by_code('masach.code') or 'New'
            res = super(Sach, self).create(vals)
        return res


class Serial(models.Model):
    _name = 'serial'
    _rec_name = 'name'
    _description = 'Serial Sách'

    name = fields.Char(string='Mã Sách')
    for_sach = fields.Many2one(string='Cho sách', comodel_name='sach.doc')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)


class DanhMucSach(models.Model):
    _name = 'danh.muc'
    _rec_name = 'name'
    _description = 'Danh mục sách'

    name = fields.Char(string='Tên tủ sách')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
