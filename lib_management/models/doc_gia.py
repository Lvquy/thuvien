# -*- coding: utf-8 -*-
import random

from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class DocGia(models.Model):
    _name = 'doc.gia'
    _rec_name = 'ma_docgia'
    _description = 'Độc giả'
    _order = "id desc"

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
        'res.company', 'Trường học', readonly=True, index=1, default=lambda self: self.env.user.company_id.id)
    mobile = fields.Char(string='Số điện thoại')
    ngay_tao_the = fields.Date(string='Ngày tạo thẻ', default=datetime.today())
    kieu_the = fields.Selection([('hs', 'Học sinh'), ('gv', 'Giáo viên'), ('other', 'Khác')], string='Loại thẻ',
                                default='hs')
    ngay_het_han = fields.Date(string='Ngày hết hạn')
    count_muon_sach = fields.Integer(string='Số lần mượn sách')
    count_error = fields.Integer(string='Số lần quá hạn/hỏng sách',
                                 help='Là số lần độc giả trả sách quá hạn hoặc làm hỏng sách, mất sách...')
    count_dang_muon = fields.Integer(string='Sách đang mượn')
    count_checkin = fields.Integer(string='Số lần điểm danh', readonly=True, compute='_compute_checkin')
    diem_danh = fields.One2many(comodel_name='check.in', inverse_name='ma_docgia', string='Điểm danh')

    def compute_muon_sach(self):
        for rec in self:
            rec.count_muon_sach = 0
            rec.count_muon_sach = rec.env['muon.tra'].search_count(['&',('state','=','2'),('nguoi_muon','=',rec.id),('company_id', 'in', [a.id for a in self.env.user.company_ids])])

    def _compute_checkin(self):
        for rec in self:
            rec.count_checkin = 0
            for line in rec.diem_danh:
                if line.state == '1':
                    rec.count_checkin +=1

    def checkin_docgia(self):
        for rec in self:
            rec.write({
                'diem_danh':[(0, 0, {
                    'date_checkin' :datetime.today(),
                    'ma_docgia': rec.id
                })]
            })

    # tong so lan da muon
    def action_view_muon_sach(self, context=None):
        field_ids = self.env['muon.tra'].search(['&', ('state', '=', '2'), ('nguoi_muon', '=', self.id)]).ids
        domain = [('id', 'in', field_ids)]
        view_id_tree = self.env['ir.ui.view'].sudo().search([('name', '=', "muon.tra.tree")])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'muon.tra',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(view_id_tree[0].id, 'tree'), (False, 'form')],
            'target': 'current',
            'domain': domain,
            'name': 'Phiếu đã mượn sách'
        }

    def action_view_dang_muon_sach(self, context=None):
        field_ids = self.env['muon.tra'].search(['&', ('state', 'in', ('1','3')), ('nguoi_muon', '=', self.id)]).ids
        domain = [('id', 'in', field_ids)]
        view_id_tree = self.env['ir.ui.view'].sudo().search([('name', '=', "muon.tra.tree")])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'muon.tra',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(view_id_tree[0].id, 'tree'), (False, 'form')],
            'target': 'current',
            'domain': domain,
            'name': 'Phiếu đang mượn'
        }

    def action_view_error(self, context=None):
        field_ids = self.env['muon.tra'].search(
            ['&', ('state', '=', '2'), ('type_phat', 'in', ('0', '1', '2')), ('nguoi_muon', '=', self.id)]).ids
        domain = [('id', 'in', field_ids)]
        view_id_tree = self.env['ir.ui.view'].sudo().search([('name', '=', "muon.tra.tree")])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'muon.tra',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(view_id_tree[0].id, 'tree'), (False, 'form')],
            'target': 'current',
            'domain': domain,
            'name':'Số lần trả sách lỗi'
        }


    @api.model
    def create(self, vals):
        global res
        if vals.get('ma_docgia', 'New' == 'New'):
            vals['ma_docgia'] = self.env['ir.sequence'].next_by_code('docgia.code') or 'New'
            res = super(DocGia, self).create(vals)
            BaoCao = self.env['bao.cao'].search(
                [('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo()
            BaoCao.update_bao_cao()
        return res

    def unlink(self):
        res = super(DocGia, self).unlink()
        BaoCao = self.env['bao.cao'].search(
            [('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo()
        BaoCao.update_bao_cao()
        return res

    def write(self, vals):
        res = super(DocGia, self).write(vals)
        if vals.get('kieu_the'):
            BaoCao = self.env['bao.cao'].search(
                [('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo()
            BaoCao.update_bao_cao()
        return res

    @api.model
    def get_import_templates(self):
        return [{
            'label': ('Tải file mẫu'),
            'template': '/lib_management/static/xls/docgia_template_sample.xlsx'
        }]

class LopHoc(models.Model):
    _name = 'lop.hoc'
    _rec_name = 'name'
    _description = 'Lớp học'

    name = fields.Char(string='Tên lớp')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)

class Checkin(models.Model):
    _name = 'check.in'
    _rec_name = 'ma_docgia'
    _description = 'Điểm danh độc giả'
    _order = 'id desc'

    date_checkin = fields.Datetime(string='Ngày vào thư viện', default=datetime.today())
    ma_docgia = fields.Many2one(comodel_name='doc.gia', string='Mã độc giả', domain =lambda self:[('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
    state = fields.Selection([('0','Chưa xác nhận'),('1','Đã xác nhận')], string='Trạng thái', default='0')

    def confirm(self):
        for rec in self:
            rec.state = '1'