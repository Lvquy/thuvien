# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class BaoCao(models.Model):
    _name = 'bao.cao'
    _rec_name = 'name'
    _description = 'Báo cáo thống kê'

    name = fields.Char(string='Name')
    company_id = fields.Many2one(
        'res.company', 'Trường học', readonly=True, index=1, default=lambda self: self.env.user.company_id.id)