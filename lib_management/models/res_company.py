# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime
from odoo.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'
    _description = 'Res Company'

    dv_chu_quan = fields.Char(string='Đơn vị chủ quản')
    hieu_truong = fields.Char(string='Hiệu trưởng')
    dv_ql_cap1 = fields.Char(string='Đơn vị quản lý cấp 1')