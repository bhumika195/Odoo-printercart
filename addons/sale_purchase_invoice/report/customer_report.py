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

from openerp.osv import osv
from openerp.tools.translate import _
from openerp.report import report_sxw
from openerp.modules.module import get_module_resource

import itertools
import operator

import time
from datetime import datetime
import dateutil.relativedelta

class customer_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(customer_report, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'get_inactive_customer_details':self.get_inactive_customer_details,
            #'get_last_order_date':self.get_last_order_date,
            })

    def get_inactive_customer_details(self, data):
        print"\n\n get_inactive_customer_details()..............."

        partner_pool = self.pool.get('res.partner')
        sale_order_pool = self.pool.get('sale.order')
        #today_date = time.strftime("%Y-%m-%d")
        #today_date = datetime.strptime(today_date, '%Y-%m-%d')
        #now = datetime.datetime.now()
        
        wizard_date = data['date']
        wizard_date = datetime.strptime(wizard_date, '%Y-%m-%d')
        #print"wizard_date",wizard_date,type(wizard_date)
        
        before_3month = wizard_date + dateutil.relativedelta.relativedelta(months=-3)
        inactive_date = str(before_3month).split(" ")[0]

        partner_ids = partner_pool.search(self.cr, self.uid, [])
        print"partner_ids",partner_ids
        print"lenght of ids",len(partner_ids)

        
        partner_object_list = []
        partner_list = []
        #partner_ids = [1544,1545,1546,22590]
        for partner in partner_pool.read(self.cr, self.uid, partner_ids, ['name']):
            print"\n\n\npartner",partner
            sale_order_id = sale_order_pool.search(self.cr, self.uid, [('partner_id.name','=',partner['name'])], limit=1, order="date_order desc")
            partner_dict = {}
            if sale_order_id:
                sale_order = sale_order_pool.read(self.cr, self.uid, sale_order_id[0], ['date_order'])
                date_order = sale_order['date_order'].split(" ")[0]
                if inactive_date >= date_order:
                    partner_obj = partner_pool.browse(self.cr, self.uid, partner['id'])
                    partner_object_list.append(partner_obj)
            else:
                partner_obj = partner_pool.browse(self.cr, self.uid, partner['id'])
                partner_object_list.append(partner_obj)
        return partner_object_list

    '''def get_last_order_date(self, partner_name):
        print"get_last_order_date"
        sale_order_pool = self.pool.get('sale.order')
        sale_order_id = sale_order_pool.search(self.cr, self.uid, [('partner_id.name','=',partner_name)], limit=1, order="date_order desc")
        if sale_order_id :
            sale_order = sale_order_pool.read(self.cr, self.uid, sale_order_id[0], ['date_order'])
            print"sale_order['date_order']",sale_order['date_order']
            return sale_order['date_order']
        print"Never Ordered"
        return "Never Ordered"'''

class customer_report_template_id(osv.AbstractModel):
    _name = 'report.sale_purchase_invoice.report_inactive_customer'
    _inherit = 'report.abstract_report'
    _template = 'sale_purchase_invoice.report_inactive_customer'
    _wrapped_report_class = customer_report
customer_report_template_id()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
