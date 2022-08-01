# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError

class MuonTra(models.Model):
    _name = 'muon.tra'
    _rec_name = 'no'
    _description = 'Mượn trả sách'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    no = fields.Char(string='Mã phiếu')
    nguoi_muon = fields.Many2one(comodel_name='doc.gia', string='Người mượn')
    ma_doc_gia = fields.Char(strig='Mã độc giả', related='nguoi_muon.ma_docgia')
    ngay_muon = fields.Datetime(string='Ngày mượn', default=datetime.today())
    ngay_tra = fields.Datetime(string='Hạn trả')
    state = fields.Selection([('new','Mới tạo'),('1','Đang mượn'),('2','Đã trả')],string='Trạng thái', default='new')
    danh_sach_muon = fields.One2many(comodel_name='line.muon.tra', inverse_name='ref_muon_tra', string='Danh sách mượn')
    nhan_vien = fields.Many2one(comodel_name='nhan.vien', string='Nhân viên')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
    note = fields.Text(string='Ghi chú')

class LineMuonTra(models.Model):
    _name = 'line.muon.tra'
    _rec_name = 'name'
    _description = 'Line Mượn trả sách'


    name = fields.Many2one(comodel_name='sach.doc', string='Tên sách')
    ma_sach = fields.Char(string='Mã sách')
    ke_sach = fields.Many2one(string='Kệ sách', related='name.ke_kho')
    ref_muon_tra = fields.Many2one(comodel_name='muon.tra', string='Mượn trả sách')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
