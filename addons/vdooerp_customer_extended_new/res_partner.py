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

from openerp import models, fields, api

class res_partner(models.Model):

    _inherit='res.partner'

    @api.multi
    def name_get(self):
        if self._context is None:
            self._context = {}
        if isinstance(self._ids, (int, long)):
            ids = [self._ids]
        res = []
        for record in self:
            name = record.name
            if record.is_company and not record.parent_id:
                name=record.name
            if not record.is_company and record.parent_id:
                name = record.name
            if self._context.get('show_address'):
                name = name + "\n" + self._display_address(record, without_company=True)
                name = name.replace('\n\n','\n')
                name = name.replace('\n\n','\n')
            if self._context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)
            res.append((record.id, name))
        return res

    @api.multi
    def _get_comapany_chield(self):
        res={}
        for data in self:
            users_list=[]
            for child in data.child_ids:
                if child.is_default_contact:
                    users_list.append(child.id)
            if users_list:
                data.default_contact_id = users_list and users_list[0] or False

    last_order_date = fields.Date(string='Order Date')
    last_schedule_date = fields.Date(string='Scheduled Date')
    is_default_contact = fields.Boolean('Use Default Contact')
    default_contact_id = fields.Many2one(compute='_get_comapany_chield', relation='res.partner', string='Default Contact')
 
