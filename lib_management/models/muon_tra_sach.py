# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class MuonTra(models.Model):
    _name = 'muon.tra'
    _rec_name = 'no'
    _description = 'Mượn trả sách'

    no = fields.Char(string='Mã phiếu', readonly=True, default=lambda self: 'New')
    nguoi_muon = fields.Many2one(comodel_name='doc.gia', string='Người mượn', required=True,
                                 domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    ma_doc_gia = fields.Char(string='Mã độc giả', related='nguoi_muon.ma_docgia')
    ngay_muon = fields.Date(string='Ngày mượn', default=datetime.today())
    han_tra = fields.Date(string='Hạn trả', required=True)
    ngay_tra = fields.Date(string='Ngày trả')
    type_phat = fields.Selection([('0', 'Quá hạn'), ('1', 'Hỏng/mất sách'), ('2', 'Khác')], string='Phạt tiền', )
    tien_phat = fields.Integer(string='Tiền phạt (VNĐ)')
    state = fields.Selection([('new', 'Mới tạo'), ('1', 'Đang mượn'), ('3', 'Trả 1 phần'), ('2', 'Đã trả')],
                             string='Trạng thái',
                             default='new')
    ly_do_phat = fields.Char(string='Lý do phạt')
    danh_sach_muon = fields.One2many(comodel_name='line.muon.tra', inverse_name='ref_muon_tra', string='Danh sách mượn')
    nhan_vien = fields.Many2one(comodel_name='nhan.vien', string='Nhân viên', required=True,
                                domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
    note = fields.Text(string='Ghi chú')
    total_qty = fields.Integer(string='Tổng số sách mượn', readonly=True, compute='onchange_qty')

    @api.onchange('danh_sach_muon')
    def onchange_qty(self):
        for rec in self:
            rec.total_qty = 0
            for line in rec.danh_sach_muon:
                rec.total_qty += 1

    @api.model
    def create(self, vals):
        global res
        if vals.get('no', 'New' == 'New'):
            vals['no'] = self.env['ir.sequence'].next_by_code('muontrasach.code') or 'New'
            res = super(MuonTra, self).create(vals)
        return res

    def update_count_dang_muon(self):
        for rec in self:
            res = 0
            for line in rec.danh_sach_muon:
                if line.is_datra == False:
                    res +=1
        return res

    def confirm(self):
        for rec in self:
            if rec.state == 'new' and rec.danh_sach_muon:
                rec.state = '1'
                rec.nguoi_muon.count_dang_muon += rec.update_count_dang_muon()
                for line in rec.danh_sach_muon:
                    line.serial_no.nguoi_muon = rec.nguoi_muon
                    line.serial_no.state = '1'
                rec.env['sach.doc'].search(
                    [('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo().update_qty()
                BaoCao = self.env['bao.cao'].search(
                    [('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo()
                BaoCao.update_bao_cao()
            else:
                raise UserError('Làm mới trình duyệt hoặc chọn sách cần mượn!')

    def return_sach(self):
        for rec in self:
            if rec.state == '1':
                rec.state = '2'
                rec.nguoi_muon.count_muon_sach += 1
                rec.nguoi_muon.count_dang_muon -= rec.update_count_dang_muon()
                if rec.type_phat in ('0', '1', '2'):
                    rec.nguoi_muon.count_error += 1
                rec.ngay_tra = datetime.today()
                for line in rec.danh_sach_muon:
                    line.serial_no.nguoi_muon = False
                    line.serial_no.state = '0'
                    line.is_datra = True
                rec.env['sach.doc'].search(
                    [('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo().update_qty()
                BaoCao = self.env['bao.cao'].search(
                    [('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo()
                BaoCao.update_bao_cao()
            else:
                raise UserError('Làm mới trình duyệt!')

    def check_return_done(self):
        for rec in self:
            return rec.update_count_dang_muon() == 0

class LineMuonTra(models.Model):
    _name = 'line.muon.tra'
    _rec_name = 'serial_no'
    _description = 'Line Mượn trả sách'

    serial_no = fields.Many2one(comodel_name='serial', string='Mã sách', required=True,
                                domain=lambda self: ['&', ('state', '=', '0'),
                                                     ('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    name = fields.Char(string='Tên sách', related='serial_no.ten_sach')
    ke_sach = fields.Many2one(string='Kệ sách', related='serial_no.ke_kho',
                              domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    ref_muon_tra = fields.Many2one(comodel_name='muon.tra', string='Mượn trả sách',
                                   domain=lambda self: [
                                       ('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
    state = fields.Selection([('0', 'Trong kho'), ('1', 'Cho mượn'), ('2', 'Phế phẩm')], string='Trạng thái',
                             related='serial_no.state')
    is_datra = fields.Boolean(string='Đã trả', default=False)

    def tra_1phan(self):
        for rec in self:
            if rec.ref_muon_tra.state in ('1','3'):
                rec.serial_no.state = '0'
                rec.serial_no.ma_sach.update_qty()
                rec.is_datra = True
                rec.ref_muon_tra.nguoi_muon.count_dang_muon -= 1
                if rec.ref_muon_tra.check_return_done() == True:
                    rec.ref_muon_tra.state = '2'
                    rec.ref_muon_tra.nguoi_muon.count_muon_sach +=1
                    rec.ref_muon_tra.ngay_tra = datetime.today()
                    if rec.ref_muon_tra.type_phat in ('0', '1', '2'):
                        rec.ref_muon_tra.nguoi_muon.count_error += 1
                else:
                    rec.ref_muon_tra.state = '3'
                BaoCao = self.env['bao.cao'].search(
                    [('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo()
                BaoCao.update_bao_cao()
            else: raise UserError("Phải xác nhận cho mượn trước!")
