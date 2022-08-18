# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Book(http.Controller):
    @http.route(['/top_book'], auth='public', website=True, csrf=False)
    def index(self, **kw):

        Sach = request.env['sach.doc'].sudo()
        Truong = request.env['res.company'].sudo()
        values = {
            'Sach': None,
            'Truong': Truong.search([]),
        }
        if kw:
            if kw.get('truong') != 'false':
                truong_id = int(kw['truong'].split('.')[0])
                domain = [('company_id', '=', truong_id)]


                top_sach = Sach.search(domain, order='so_lan_muon asc', limit=20).sorted(key=lambda r: r.so_lan_muon,
reverse=True)
                values.update({
                    'Sach': top_sach,
                })

        return request.render('lib_management.index', values)

    @http.route(['/top_book/details/<model("sach.doc"):sach>'], auth='public', website=True, page=True, csrf=False)
    def sach(self, sach):
        values = {'sach':sach}
        return request.render('lib_management.sach', values)

    @http.route('/muon_tra_sach/', auth='public', website=True)
    def qua_han_tra(self, **kw):
        Truong = request.env['res.company'].sudo()
        MT = request.env['muon.tra'].sudo()
        values = {
            'MT': None,
            'Truong': Truong.search([])
        }
        if kw:
            print(kw)
            if kw['truong'] != 'false':
                truong = kw['truong'].split('.')
                if kw.get('qua_han') == 'on':
                    domain = ['&', ('state', '!=', ('new', '2')), ('is_qua_han', '=', True),
                              ('company_id', '=', int(truong[0]))]
                else:
                    domain = ['&', ('state', '!=', ('new', '2')), ('company_id', '=', int(truong[0]))]
                if kw.get('ma_doc_gia') != '':
                    id_doc_gia = request.env['doc.gia'].sudo().search([('ma_docgia', 'ilike', kw['ma_doc_gia'])])
                    domain = ['&', ('nguoi_muon', 'in', [a.id for a in id_doc_gia]), ('state', '!=', ('new', '2')),
                              ('company_id', '=', int(truong[0]))]
                values.update({
                    'MT': MT.search(domain, limit=100)
                })

        return request.render('lib_management.muon_tra', values)

    @http.route(['/list_book'], auth='public', website=True, csrf=False)
    def list_book(self, **kw):
        Sach = request.env['sach.doc'].sudo()
        company = request.env['res.company'].sudo()
        values = {
            'sach':Sach
        }
        return request.render('lib_management.list_book', values)