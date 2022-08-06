# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class DocGia(models.Model):
    _name = 'doc.gia'
    _rec_name = 'name'
    _description = 'Độc giả'

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
        return res


class LopHoc(models.Model):
    _name = 'lop.hoc'
    _rec_name = 'name'
    _description = 'Lớp học'

    name = fields.Char(string='Tên lớp')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
