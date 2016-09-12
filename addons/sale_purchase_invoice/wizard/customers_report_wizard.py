# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import datetime
import time

from openerp.report import report_sxw

class customers_report_wizard(osv.osv_memory):
    _name = "customer.report.wizard"
    _columns = {
        'date': fields.date('Date', required='1'),
    }
    _defaults = {
        'date': fields.datetime.now,
    }

    #report for inactive customers - all customers that have not placed a repeat order for 3 month or more
    def print_customer_report(self,cr, uid, ids, context=None):
        """
         To get the date and print the report
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param context: A standard dictionary
         @return: return report
        """
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, [], context=context)[0]
        
        datas = {
             'ids': [data.get('id')],
             'model': 'res.partner',
             'form': data
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'sale_purchase_invoice.report_inactive_customer',
            'datas': datas,
        }

customers_report_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
