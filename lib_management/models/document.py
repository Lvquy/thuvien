# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class Document(models.Model):
    _name = 'document'
    _description = 'Tài liệu hướng dẫn sử dụng'
    _rec_name = 'name'

    name = fields.Char(string='Tên tài liệu')
    body = fields.Html(string='Nội dung')
    state = fields.Selection([('0','Nháp'),('1','Xác nhận')],string='Trạng thái', default='0')
    author = fields.Many2one(comodel_name='res.users', string='Người hướng dẫn',readonly=True, default=lambda self: self.env.user.id)
    create_date = fields.Date(string='Ngày tạo', default=datetime.today())

    def confirm(self):
        self.state = '1'

    def unconfirm(self):
        self.state = '0'