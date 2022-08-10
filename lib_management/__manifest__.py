# -*- coding: utf-8 -*-
{
    'name': 'Thư Viện Minh Nghĩa',
    'version': '1',
    'category': 'lib management',
    'live_test_url': '#',
    'summary': 'Phần mềm quản lý thư viện',
    'author': 'Lv Quy',
    'company': 'Minh Nghĩa',
    'website': 'https://#',
    'depends': ['base_setup','prt_report_attachment_preview','rowno_in_tree','web_responsive'],
    'data': [
        # security
        'data/thu_vien_security.xml',
        # 'data/sequence.xml',
        'data/cron_job.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',

        # views
        'views/search.xml',
        'views/serial_views.xml',
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
        'views/danh_muc_sach_views.xml',
        'views/purchase_views.xml',
        'views/bao_phe_views.xml',
        'views/bao_cao_views.xml',
        'views/res_users.xml',


        #menu
        'views/menu.xml',
        # report
        'report/the_doc_gia.xml',
        'report/gay_sach.xml',
        'report/menu_report.xml',
        'report/template.xml',


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

