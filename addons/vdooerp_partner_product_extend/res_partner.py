#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp import netsvc

class res_partner(models.Model):


    _inherit = 'res.partner'

    @api.onchange('country_id')
    def onchange_country_id(self):
        coun_obj=self.env['res.country']
        country_data=coun_obj.browse(self.country_id.id)
        result={'val':{}}
        if country_data.name:
                if country_data.name in ('Austria','Belgium','Bulgaria','Croatia','Republic of Cyprus','Czech Republic',\
            'Denmark','Estonia','Finland','France','Germany','Greece','Hungary','Ireland','Italy','Latvia','Lithuania','Luxembourg','Malta',\
            'Netherlands','Poland','Portugal','Romania','Slovakia','Slovenia','Spain','Sweden','UK'):
                        self.flage = True
                        print 'return true in on change >>'
                self.flage = False
                 
    category_id = fields.Many2many('res.partner.category', id1='partner_id', id2='category_id', string='Tags',required=True)
    street = fields.Char(string='street',required=True)
    city = fields.Char(string='City',size=128,required=True)
    country_id = fields.Many2one('res.country',string='Country',required=True)
    vat = fields.Char(string='TIN', size=32, help="Tax Identification Number. Check the box if this contact is subjected to taxes. Used by the some of the legal statements.",required=True)
    flage = fields.Boolean(string='flage',default=False)

        #_constraints = [(_check_country_id, 'Error: UNIQUE MSG', ['FIELD'])]
