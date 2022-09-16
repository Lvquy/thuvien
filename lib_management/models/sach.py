# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class Sach(models.Model):
    _name = 'sach.doc'
    _rec_name = 'ma_sach'
    _order = 'id desc'
    _description = 'Sách thư viện'
    _order = "id desc"

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
    next_num = fields.Integer(string='Số serial tiếp theo', default=100, readonly=True)
    so_luong = fields.Integer(string='Số lượng trong kho',compute='onchange_serial_list')
    so_luong_muon = fields.Integer(string='Số lượng đang cho mượn',compute='onchange_serial_list')
    total_qty = fields.Integer(string='Tổng số lượng sách', compute='onchange_serial_list')
    so_luong_huy = fields.Integer(string='Sách đã hủy',compute='onchange_serial_list')
    gia_sach = fields.Integer(string='Giá sách')
    serial_list =  fields.Many2many(string='Serial sách', comodel_name='serial', compute='compute_serial',
                                    domain=lambda self: [
                                        ('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    so_lan_muon = fields.Integer(string='Số lần mượn')

    def onchange_serial_list(self):
        for rec in self:
            rec.total_qty = 0
            rec.so_luong = 0
            rec.so_luong_muon = 0
            rec.so_luong_huy = 0
            print('update qty...')
            for i in rec.serial_list:
                rec.total_qty +=1
                if i.state == '0':
                    rec.so_luong +=1
                if i.state == '1':
                    rec.so_luong_muon +=1
                if i.state == '2':
                    rec.so_luong_huy +=1


    def compute_serial(self):
        for rec in self:
            domain =  ['&',('ma_sach','=',rec.id),('company_id', 'in', [a.id for a in self.env.user.company_ids])]
            SR = rec.env['serial'].search(domain)
            rec.serial_list = SR

    @api.model
    def create(self, vals):
        global res
        if vals.get('ma_sach', 'New' == 'New'):
            vals['ma_sach'] = self.env['ir.sequence'].next_by_code('masach.code') or 'New'
            res = super(Sach, self).create(vals)
        BaoCao = self.env['bao.cao'].search([('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo()
        BaoCao.update_bao_cao()
        return res


    def unlink(self):
        res = super(Sach, self).unlink()
        BaoCao = self.env['bao.cao'].search([('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo()
        BaoCao.update_bao_cao()
        return res

    def create_serial(self):
        return {
            'name': 'Tạo serial cho sách',
            'type': 'ir.actions.act_window',
            'res_model': 'create.serial',
            'view_mode': 'form',
            'target': 'new',
            'context': "{'default_ma_sach': active_id, 'default_create_qty': 1}"
        }

    def action_view_none(self):
        return None

    def action_view_sach(self, context=None):
        field_ids = self.env['serial'].search([('ma_sach', '=', self.ma_sach)]).ids
        domain = [('id', 'in', field_ids)]
        view_id_tree = self.env['ir.ui.view'].sudo().search([('name', '=', "serial.tree")])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'serial',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(view_id_tree[0].id, 'tree'), (False, 'form')],
            'target': 'current',
            'domain': domain,
            'name':'Serial Sách'
        }

    # số lượng đang mượn
    def action_view_sach_muon(self, context=None):
        field_ids = self.env['serial'].search(['&', ('ma_sach', '=', self.ma_sach), ('state', '=', '1')]).ids
        domain = [('id', 'in', field_ids)]
        view_id_tree = self.env['ir.ui.view'].sudo().search([('name', '=', "serial.tree")])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'serial',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(view_id_tree[0].id, 'tree'), (False, 'form')],
            'target': 'current',
            'domain': domain,
            'name': 'Sách đang cho mượn'
        }

    # trong kho
    def action_view_sach_onhand(self, context=None):
        field_ids = self.env['serial'].search(['&', ('ma_sach', '=', self.ma_sach), ('state', '=', '0')]).ids
        domain = [('id', 'in', field_ids)]
        view_id_tree = self.env['ir.ui.view'].sudo().search([('name', '=', "serial.tree")])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'serial',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(view_id_tree[0].id, 'tree'), (False, 'form')],
            'target': 'current',
            'domain': domain,
            'name': 'Sách đang trong thư viện'
        }

    # sách đã hủy
    def action_view_sach_huy(self, context=None):
        field_ids = self.env['serial'].search(['&', ('ma_sach', '=', self.ma_sach), ('state', '=', '2')]).ids
        domain = [('id', 'in', field_ids)]
        view_id_tree = self.env['ir.ui.view'].sudo().search([('name', '=', "serial.tree")])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'serial',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'views': [(view_id_tree[0].id, 'tree'), (False, 'form')],
            'target': 'current',
            'domain': domain,
            'name': 'Sách đã báo phế'
        }


class CreateSerial(models.Model):
    _name = 'create.serial'
    _rec_name = 'ma_sach'
    _description = 'Create serial for sach'

    ma_sach = fields.Many2one(string='Mã sách',
                              comodel_name='sach.doc',
                              required=True,
                              ondelete='cascade',
                              domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
    create_qty = fields.Integer(string='Số lượng tạo')
    next_num = fields.Integer(string='Số serial tiếp theo', related='ma_sach.next_num')
    ten_sach = fields.Char(string='Tên sách', related='ma_sach.name')

    def create_serial(self):
        for rec in self:
            SR = rec.env['serial']
            if rec.create_qty <= 0:
                raise UserError("Số lượng phải lớn hơn 0")
            for i in range(0, rec.create_qty):
                SR.create({
                    'ma_sach': rec.ma_sach.id,
                    'serial_no': str(rec.ma_sach.ma_sach) + '-' + str(rec.next_num)
                })
                rec.ma_sach.next_num += 1
            BaoCao = self.env['bao.cao'].search(
                [('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo()
            BaoCao.update_bao_cao()

    def cancel(self):
        pass

class Serial(models.Model):
    _name = 'serial'
    _rec_name = 'serial_no'
    _description = 'Serial Sách'
    _order = "id,ma_sach,serial_no asc"

    serial_no = fields.Char(string='Serial sách duy nhất', default=lambda self: 'New', readonly=True)
    ma_sach = fields.Many2one(string='Mã sách', comodel_name='sach.doc',
                              required=False, readonly=True,
                              domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
    ten_sach = fields.Char(string='Tên sách', related='ma_sach.name')
    tinh_trang = fields.Selection([('tot', 'Tốt'), ('cu', 'Cũ'),('hong', 'Hỏng')], string='Tình trạng', default='tot')
    ke_kho = fields.Many2one(comodel_name='ke.kho', related='ma_sach.ke_kho')
    state = fields.Selection([('0', 'Trong kho'), ('1', 'Cho mượn'), ('2', 'Phế phẩm')], string='Trạng thái sách',
                             default='0')
    note = fields.Text(string='Ghi chú')
    nguoi_muon = fields.Many2one(comodel_name='doc.gia', string='Người đang mượn',
                                 domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    ngay_tao = fields.Date(string='Ngày tạo', default=datetime.today())
    gia_sach = fields.Integer(string='Giá sách', related='ma_sach.gia_sach')

    def bao_phe_sach(self):
        return {
            'name': 'Báo phế sách',
            'type': 'ir.actions.act_window',
            'res_model': 'create.baophe',
            'view_mode': 'form',
            'target': 'new',
            'context': "{'default_serial_sach': active_id}"
        }

    def unlink(self):
        res = super(Serial, self).unlink()
        BaoCao = self.env['bao.cao'].search(
            [('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo()
        BaoCao.update_bao_cao()
        return res



class CreateBaoPhe(models.Model):
    _name = 'create.baophe'
    _description = 'Tạo báo phế sách'
    _rec_name = 'name'

    serial_sach = fields.Many2one(comodel_name='serial', string='Serial sách cần báo phế',
                                  domain=lambda self: [('company_id', 'in', [a.id for a in self.env.user.company_ids])])
    ly_do = fields.Text(string='Lý do báo phế')
    name = fields.Char(string='Tên sách', related='serial_sach.ten_sach')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)

    def create_baophe_sach(self):
        for rec in self:
            rec.serial_sach.tinh_trang = 'hong'
            BaoPhe = rec.env['bao.phe']
            BaoPhe.create({
                'ly_do':rec.ly_do,
                'danh_sach_phe': rec.serial_sach,
                'state':'1',

            })
            rec.serial_sach.state = '2'
            BaoCao = self.env['bao.cao'].search(
                [('company_id', 'in', [a.id for a in self.env.user.company_ids])]).sudo()
            BaoCao.update_bao_cao()

class DanhMucSach(models.Model):
    _name = 'danh.muc'
    _rec_name = 'name'
    _description = 'Danh mục sách'

    name = fields.Char(string='Tên tủ sách')
    ma_ts = fields.Char(string='Mã tủ sách', required=True)
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)
