# -*- coding: utf-8 -*-
{
    'name': "Kursus",

    'summary': "Aplikasi kursus menggunakan odoo v18",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '18.0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'mail', 'product', 'account'],

    # always loaded
    'data':
         [
        'security/groups.xml',
        'security/ir.rule.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/menu.xml',
        'views/kursus.xml',
        'views/instruktur.xml',
        'views/propinsi.xml',
        'views/kota.xml',
        'views/kecamatan.xml',
        'views/desa.xml',
        'views/peserta.xml',
        'views/training_session.xml',
        'wizards/training_wizard.xml',
        'views/product_inherit.xml',
        'views/pendaftaran.xml',
        'views/daftar_hadir.xml',
        'reports/bukti_pendaftaran_template.xml',
        'reports/kursus_card_template.xml',
        'reports/daftar_hadir_template.xml',
        'reports/report.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

