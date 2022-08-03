# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class Sach(models.Model):
    _name = 'sach.doc'
    _rec_name = 'ma_sach'
    _order = 'id desc'
    _description = 'Sách thư viện'

    name = fields.Char(string='Tên sách')
    img = fields.Binary(string='Hình ảnh')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
    tac_gia = fields.Many2one(string='Tác giả', comodel_name='tac.gia',
                              domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    the_loai_sach = fields.Many2one(string='Thể loại', comodel_name='the.loai',
                                    domain=lambda self: [
                                        ('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    nha_xb = fields.Many2one(string='Nhà xuất bản', comodel_name='nxb',
                             domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    ke_kho = fields.Many2one(string='Kệ kho', comodel_name='ke.kho',
                             domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    ngon_ngu = fields.Many2one(string='Ngôn ngữ', comodel_name='lang',
                               domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    note = fields.Html(string='Giới thiệu ngắn')
    so_trang = fields.Integer(string='Số trang')
    nam_xb = fields.Integer(string='Năm xuất bản')
    danh_muc_sach = fields.Many2one(comodel_name='danh.muc', string='Tên tủ sách',
                                    domain=lambda self: [
                                        ('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    ma_sach = fields.Char(string='Mã sách', readonly=True, default=lambda self: 'New')
    next_num = fields.Integer(string='Số serial tiếp theo', default=1, readonly=True)

    @api.model
    def create(self, vals):
        global res
        if vals.get('ma_sach', 'New' == 'New'):
            vals['ma_sach'] = self.env['ir.sequence'].next_by_code('masach.code') or 'New'
            res = super(Sach, self).create(vals)
        return res

    def create_serial(self):
        return {
            'name': ('Tạo serial cho sách'),
            'type': 'ir.actions.act_window',
            'res_model': 'create.serial',
            'view_mode': 'form',
            'target': 'new',
            'context': "{'default_ma_sach': active_id, 'default_create_qty': 1}"
        }


class CreateSerial(models.Model):
    _name = 'create.serial'
    _rec_name = 'ma_sach'
    _description = 'Create serial for sach'

    ma_sach = fields.Many2one(string='Mã sách',
                              comodel_name='sach.doc',
                              required=True,
                              domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
    create_qty = fields.Integer(string='Số lượng tạo')
    next_num = fields.Integer(string='Số serial tiếp theo', related='ma_sach.next_num')
    ten_sach = fields.Char(string='Tên sách', related='ma_sach.name')

    def create_serial(self):
        for rec in self:
            SR = rec.env['serial']
            for i in range(0, rec.create_qty):
                SR.create({
                    'ma_sach': rec.ma_sach.id,
                    'serial_no': str(rec.ma_sach.ma_sach) + '-' + str(rec.next_num)
                })
                rec.ma_sach.next_num += 1

    def cancel(self):
        pass


class Serial(models.Model):
    _name = 'serial'
    _rec_name = 'serial_no'
    _description = 'Serial Sách'

    serial_no = fields.Char(string='Serial sách duy nhất', default=lambda self: 'New', readonly=True)
    ma_sach = fields.Many2one(string='Mã sách', comodel_name='sach.doc',
                              domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
    ten_sach = fields.Char(string='Tên sách', related='ma_sach.name')
    tinh_trang = fields.Selection([('tot', 'Tốt'), ('hong', 'Hỏng'), ('cu', 'Cũ')], string='Tình trạng', default='tot')
    ke_kho = fields.Many2one(comodel_name='ke.kho', related='ma_sach.ke_kho')


class DanhMucSach(models.Model):
    _name = 'danh.muc'
    _rec_name = 'name'
    _description = 'Danh mục sách'

    name = fields.Char(string='Tên tủ sách')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
