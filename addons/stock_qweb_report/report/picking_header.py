from openerp.osv import osv
from openerp.tools.translate import _


class PosInvoiceReport(osv.AbstractModel):
    _name = 'report.stock_qweb_report.report_picking_custom'

    def render_html(self, cr, uid, ids, data=None, context=None):
        report_obj = self.pool['report']
        StockPicking = self.pool['stock.picking']
        print "data",data
        # report = report_obj._get_report_from_name(cr, uid, 'stock_qweb_report.report_picking_custom')
        selected_orders = StockPicking.browse(cr, uid, data['ids'], context=context)
        ids_to_print = []
        for picking in selected_orders:
             ids_to_print.append(picking.id)
        docargs = {
            'doc_ids': ids_to_print,
            'doc_model': 'stock.picking',
            'docs': selected_orders,
            'data': data
        }
        return report_obj.render(cr, uid, ids, 'stock_qweb_report.report_picking_custom', docargs, context=context)
