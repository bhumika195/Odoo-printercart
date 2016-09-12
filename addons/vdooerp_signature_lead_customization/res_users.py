
from openerp.osv import osv, fields
from openerp import models, fields, api, _

class res_users(models.Model):

    _inherit = 'res.users'

    signature_logo = fields.Binary(string='Signature Logo')


class res_partner(models.Model):

    _inherit = 'res.partner'

    account_number = fields.Char(string='Account Number')

    _sql_constraints = [
        ('account_number_uniq', 'UNIQUE(account_number)', 'Account Number must be unique!'),
    ]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
