# -*- coding: utf-8 -*-
{
    'name': 'Sach',
    'version': '1',
    'category': 'lib management',
    'live_test_url': '#',
    'summary': 'Phần mềm quản lý thư viện',
    'author': 'Lv Quy',
    'company': 'Minh Nghĩa',
    'website': 'https://#',
    'depends': ['base_setup'],
    'data': [
        # security
        'data/thu_vien_security.xml',
        'data/sequence.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',

        # views
        'views/search.xml',
        'views/sach_views.xml',
        'views/doc_gia_views.xml',
        'views/ke_kho_views.xml',
        'views/ngon_ngu_views.xml',
        'views/nhan_vien_views.xml',
        'views/nxb_views.xml',
        'views/tac_gia_views.xml',
        'views/the_loai_views.xml',
        'views/muon_tra_views.xml',
        'views/res_company_views.xml',
        'views/menu.xml',

        # report

    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
}

