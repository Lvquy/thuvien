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
    ngay_muon = fields.Date(string='Ngày mượn', default=datetime.today())
    han_tra = fields.Date(string='Hạn trả')
    ngay_tra = fields.Date(string='Ngày trả')
    type_phat = fields.Selection([('0', 'Quá hạn'), ('1', 'Hỏng/mất sách'), ('2', 'Khác')], string='Phạt tiền', )
    tien_phat = fields.Integer(string='Tiền phạt (VNĐ)')
    state = fields.Selection([('new', 'Mới tạo'), ('1', 'Đang mượn'), ('2', 'Đã trả')], string='Trạng thái',
                             default='new')
    ly_do_phat = fields.Char(string='Lý do phạt')
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

    def confirm(self):
        for rec in self:
            if rec.state == 'new' and rec.danh_sach_muon:
                rec.state = '1'
                rec.nguoi_muon.count_dang_muon += 1
                for l in rec.danh_sach_muon:
                    l.serial_no.nguoi_muon = rec.nguoi_muon
                    l.serial_no.state = '1'
                rec.env['sach.doc'].search(
                    [('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo().update_qty()
            else:
                raise UserError('Làm mới lại trình duyệt!')

    def return_sach(self):
        for rec in self:
            if rec.state == '1':
                rec.state = '2'
                rec.nguoi_muon.count_muon_sach += 1
                if rec.type_phat in ('0', '1', '2'):
                    rec.nguoi_muon.count_error += 1
                rec.ngay_tra = datetime.today()
                for l in rec.danh_sach_muon:
                    l.serial_no.nguoi_muon = False
                    l.serial_no.state = '0'
                rec.env['sach.doc'].search(
                    [('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo().update_qty()
            else:
                raise UserError('Làm mới trình duyệt!')


class LineMuonTra(models.Model):
    _name = 'line.muon.tra'
    _rec_name = 'serial_no'
    _description = 'Line Mượn trả sách'

    serial_no = fields.Many2one(comodel_name='serial', string='Mã sách', required=True,
                                domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    name = fields.Char(string='Tên sách', related='serial_no.ten_sach')
    ke_sach = fields.Many2one(string='Kệ sách', related='serial_no.ke_kho',
                              domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    ref_muon_tra = fields.Many2one(comodel_name='muon.tra', string='Mượn trả sách',
                                   domain=lambda self: [
                                       ('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
