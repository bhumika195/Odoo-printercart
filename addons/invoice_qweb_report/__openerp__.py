{
    'name': 'Custom Qweb Invoice Report',
    'category': 'Accounting & Finance',
    'summary': 'Invoice Qweb Report',
    'version': '1.0',
    'description': """
Custom Invoice Qweb Report
        """,
    'author': 'OpenERP SA',
    'depends': ['report_custom_header','account'],
    'data': [
        'views/report_invoice_custom.xml',
        'invoice_report_views.xml'
   ],
    'installable': True,
    'auto_install': True,
}