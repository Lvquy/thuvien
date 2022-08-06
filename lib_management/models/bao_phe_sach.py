# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class BaoPhe(models.Model):
    _name = 'bao.phe'
    _rec_name = 'name'
    _description = 'Báo phế sách'

    name = fields.Char(string='Mã phiếu', default=lambda self: 'New', readonly=True)
    company_id = fields.Many2one(
        'res.company', 'Trường học', readonly=True, index=1, default=lambda self: self.env.user.company_id.id)
    ngay_bao_phe = fields.Date(string='Ngày báo phế', default=datetime.today())
    ly_do = fields.Text(string='Lý do báo phế')
    danh_sach_phe = fields.Many2many(comodel_name='serial', string='List sách báo phế',
                                     domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])]
                                     )
    state = fields.Selection([('0', 'Nháp'), ('1', 'Đã xác nhận')], string='Trạng thái', default='0')

    def confirm(self):
        for rec in self:
            if rec.state == '0':
                rec.state = '1'
                for sach in rec.danh_sach_phe:
                    sach.state = '2'
                    sach.tinh_trang = 'hong'
            else:
                raise UserError('Làm mới trình duyệt!')

    @api.model
    def create(self, vals):
        global res
        if vals.get('name', 'New' == 'New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('baophe.code') or 'New'
            res = super(BaoPhe, self).create(vals)
        return res