# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models


class Purchase(models.Model):
    _name = 'mua.sach'
    _rec_name = 'name'
    _description = 'Mua sách'

    name = fields.Char(string='Mã phiếu', readonly=True, default=lambda self: 'New')
    ngay_mua = fields.Date(string='Ngày mua', default=datetime.today())
    state = fields.Selection([('new', 'Nháp'), ('done', 'Xác nhận',)], string='Trạng thái', default='new')
    venders = fields.Char(string='Nhà cung cấp')
    note = fields.Text(string='Ghi chú')
    product_lines = fields.One2many(comodel_name='pur.lines', inverse_name='ref_mua_sach', string='Sách mua')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)

    def confirm(self):
        for rec in self:
            if rec.state == 'new':
                rec.state = 'done'

    @api.model
    def create(self, vals):
        global res
        if vals.get('name', 'New' == 'New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('muasach.code') or 'New'
            res = super(Purchase, self).create(vals)
        return res

class PurLines(models.Model):
    _name = 'pur.lines'
    _rec_name = 'ma_sach'
    _description = 'Purchase Lines'

    name = fields.Many2one(comodel_name='sach.doc', string='Tên sách')
    ma_sach = fields.Char(string='Mã sách')
    qty = fields.Integer(string='Số lượng')
    ref_mua_sach = fields.Many2one(comodel_name='mua.sach', string='Đơn mua sách')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)

    @api.onchange('ma_sach')
    def onchange_sach(self):
        for rec in self:
            SACH = rec.env['sach.doc'].search([('ma_sach','=',rec.ma_sach)],limit=1)
            rec.name = SACH.id

    @api.onchange('name')
    def onchange_name(self):
        for rec in self:
            rec.ma_sach = rec.name.ma_sach
