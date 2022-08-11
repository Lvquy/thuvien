# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class NgonNgu(models.Model):
    _name = 'lang'
    _rec_name = 'name'
    _description = 'Ngôn ngữ sách'
    _order = "id desc"


    name = fields.Char(string='Ngôn ngữ sách')
    company_id = fields.Many2one(
        'res.company', 'Company', index=1, default=lambda self: self.env.user.company_id.id)