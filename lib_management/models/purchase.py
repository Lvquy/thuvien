# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError


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
    auto_create_serial = fields.Boolean(string='Tự động tạo serial cho sách', default = True)
    total_qty = fields.Integer(string='Tổng số lượng sách', readonly=True)

    @api.onchange('product_lines')
    def onchange_total_qty(self):
        for rec in self:
            rec.total_qty = 0
            for line in rec.product_lines:
                rec.total_qty += line.qty

    def create_serial(self):
        for rec in self:
            SR = rec.env['serial'].sudo()
            for l in rec.product_lines:
                for num in range(0, l.qty):
                    SR.create({
                        'ma_sach': l.ma_sach.id,
                        'serial_no': str(l.ma_sach.ma_sach) + '-' + str(l.next_num + num),
                    })
            l.ma_sach.next_num += l.qty

    def confirm(self):
        for rec in self:
            if rec.state == 'new' and rec.product_lines:
                if rec.auto_create_serial is True:
                    rec.create_serial()
                rec.state = 'done'
                for line in rec.product_lines:
                    line.ma_sach.update_qty()
                BaoCao = self.env['bao.cao'].search(
                    [('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo()
                BaoCao.update_bao_cao()
            else: raise UserError("Làm mới trình duyệt hoặc chọn sách cần mua")

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

    ma_sach = fields.Many2one(comodel_name='sach.doc', string='Mã sách')
    name = fields.Char(string='Tên sách', related='ma_sach.name')
    next_num = fields.Integer(string='Số serial tiếp theo', related='ma_sach.next_num')
    qty = fields.Integer(string='Số lượng', default=1)
    ref_mua_sach = fields.Many2one(comodel_name='mua.sach', string='Đơn mua sách')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)