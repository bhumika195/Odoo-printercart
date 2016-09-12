from datetime import datetime
from openerp import workflow
from openerp import fields, models, api, exceptions, _
from openerp.osv import osv
from openerp.osv import fields
#



class sale_order_line(osv.osv):

    _inherit = 'sale.order.line'
    _columns = {
                
        'default_code': fields.related('product_id', 'default_code', type='char', string='Internal Reference'),
    }  
    
    
class account_invoice_line(osv.osv):

    _inherit = 'account.invoice.line'
    _columns = {
                
        'default_code': fields.related('product_id', 'default_code', type='char', string='Internal Reference'),
    }   
    
    
    
class stock_move(osv.osv):
    _inherit = 'stock.move'
    _columns = {
                
        'default_code': fields.related('product_id', 'default_code', type='char', string='Internal Reference'),
    }                      