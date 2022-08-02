# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class MuonTra(models.Model):
    _name = 'muon.tra'
    _rec_name = 'no'
    _description = 'Mượn trả sách'

    no = fields.Char(string='Mã phiếu', readonly=True, default=lambda self: 'New')
    nguoi_muon = fields.Many2one(comodel_name='doc.gia', string='Người mượn',
                                 domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    ma_doc_gia = fields.Char(string='Mã độc giả', related='nguoi_muon.ma_docgia')
    ngay_muon = fields.Datetime(string='Ngày mượn', default=datetime.today())
    ngay_tra = fields.Datetime(string='Hạn trả')
    state = fields.Selection([('new', 'Mới tạo'), ('1', 'Đang mượn'), ('2', 'Đã trả')], string='Trạng thái',
                             default='new')
    danh_sach_muon = fields.One2many(comodel_name='line.muon.tra', inverse_name='ref_muon_tra', string='Danh sách mượn')
    nhan_vien = fields.Many2one(comodel_name='nhan.vien', string='Nhân viên',
                                domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
    note = fields.Text(string='Ghi chú')

    @api.model
    def create(self, vals):
        global res
        if vals.get('no', 'New' == 'New'):
            vals['no'] = self.env['ir.sequence'].next_by_code('muontrasach.code') or 'New'
            res = super(MuonTra, self).create(vals)
        return res


class LineMuonTra(models.Model):
    _name = 'line.muon.tra'
    _rec_name = 'name'
    _description = 'Line Mượn trả sách'

    name = fields.Many2one(comodel_name='sach.doc', string='Tên sách',
                           domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    ma_sach = fields.Char(string='Mã sách')
    ke_sach = fields.Many2one(string='Kệ sách', related='name.ke_kho',
                              domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    ref_muon_tra = fields.Many2one(comodel_name='muon.tra', string='Mượn trả sách',
                                   domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
