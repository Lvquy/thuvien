# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class TheLoai(models.Model):
    _name = 'the.loai'
    _rec_name = 'name'
    _description = 'Thể loại'

    name = fields.Char(string='Thể loại')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)