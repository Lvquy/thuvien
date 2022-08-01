# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class NXB(models.Model):
    _name = 'nxb'
    _rec_name = 'name'
    _description = 'Nhà xuất bản'


    name = fields.Char(string='Tên nhà xuất bản')
    note = fields.Text(string='Ghi chú')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)