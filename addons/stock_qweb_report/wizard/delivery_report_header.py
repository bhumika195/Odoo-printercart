from openerp.osv import fields, osv
from openerp.tools.translate import _

class delivery_report_header_wizard(osv.osv_memory):
    _name = 'delivery.report.header.wizard'
    _description = 'Print header in delivery'
    _columns = {
        'header': fields.selection([('header', 'Header'), ('no_header', 'Without Header')], 'Print Header')
    }
    _defaults = {
        'header': 'no_header'
    }

    def print_report(self, cr, uid, ids, context=None):

        active_id = context.get('active_id', [])
        wizard_data = self.read(cr, uid, ids, context=context)[0]
        datas = {
             'ids': [active_id],
             'model': 'stock.picking',
             'form': wizard_data 
        }
        return self.pool['report'].get_action(
            cr, uid, [], 'stock_qweb_report.report_picking_custom', data=datas, context=context
        )
