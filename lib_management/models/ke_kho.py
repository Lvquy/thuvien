# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class KeKho(models.Model):
    _name = 'ke.kho'
    _rec_name = 'name'
    _description = 'Kệ kho để sách'
    _order = "id desc"


    name = fields.Char(string='Tên kệ')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)