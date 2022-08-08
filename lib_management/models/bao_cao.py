# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class BaoCao(models.Model):
    _name = 'bao.cao'
    _rec_name = 'date_update'
    _description = 'Báo cáo thống kê'

    date_update = fields.Date(string='Ngày cập nhật')
    company_id = fields.Many2one(
        'res.company', 'Trường học', readonly=True, index=1, default=lambda self: self.env.user.company_id.id)
    total_sach = fields.Integer(string='Tổng số đầu sách', readonly=True)
    total_serial = fields.Integer(string='Tổng số sách', readonly=True)
    total_sach_muon = fields.Integer(string='Số sách đang cho mượn', readonly=True)
    total_sach_trong_kho = fields.Integer(string='Số sách đang trong kho', readonly=True)
    total_sach_phe = fields.Integer(string='Số sách đã báo phế', readonly=True)
    total_doc_gia = fields.Integer(string='Tổng số độc giả', readonly=True)
    total_giao_vien = fields.Integer(string='Tổng giáo viên')
    total_hoc_sinh = fields.Integer(string='Tổng học sinh')
    total_doc_gia_khac = fields.Integer(string='Tổng độc giả khác')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id, readonly=True)

    def update_bao_cao(self):
        for rec in self:
            rec.date_update = datetime.today()
            domain =  [('company_id', 'in', [a.id for a in self.env.user.company_ids])]
            domain_dang_muon =  ['&',('state','=','1'),('company_id', 'in', [a.id for a in self.env.user.company_ids])]
            domain_dang_trong_kho =  ['&',('state','=','0'),('company_id', 'in', [a.id for a in self.env.user.company_ids])]
            domain_sach_phe =  ['&',('state','=','2'),('company_id', 'in', [a.id for a in self.env.user.company_ids])]
            domain_doc_gia =  [('company_id', 'in', [a.id for a in self.env.user.company_ids])]
            domain_giao_vien =  ['&',('company_id', 'in', [a.id for a in self.env.user.company_ids]),('kieu_the','=','gv')]
            domain_hs =  ['&',('company_id', 'in', [a.id for a in self.env.user.company_ids]),('kieu_the','=','hs')]
            domain_khac =  ['&',('company_id', 'in', [a.id for a in self.env.user.company_ids]),('kieu_the','=','other')]
            Serial = rec.env['serial']
            Sach = rec.env['sach.doc']
            DocGia = rec.env['doc.gia']
            rec.total_sach = Sach.search_count(domain)
            rec.total_serial = Serial.search_count(domain)
            rec.total_sach_muon = Serial.search_count(domain_dang_muon)
            rec.total_sach_trong_kho = Serial.search_count(domain_dang_trong_kho)
            rec.total_sach_phe = Serial.search_count(domain_sach_phe)
            rec.total_doc_gia = DocGia.search_count(domain_doc_gia)
            rec.total_giao_vien = DocGia.search_count(domain_giao_vien)
            rec.total_hoc_sinh = DocGia.search_count(domain_hs)
            rec.total_doc_gia_khac = DocGia.search_count(domain_khac)

    @api.model
    def create(self, values):
        res = super(BaoCao, self).create(values)
        count = self.search_count([('company_id', 'in', [a.id for a in self.env.user.company_ids])])
        if count > 1:
            raise UserError('Đã tạo báo cáo rồi!')
        return res