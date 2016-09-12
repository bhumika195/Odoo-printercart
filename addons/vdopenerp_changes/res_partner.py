
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc
from openerp import models, fields, api, _

class crm_phonecall(models.Model):

    _inherit='crm.phonecall'

    @api.model
    def create(self, vals):
        res=super(crm_phonecall, self).create(vals)
        if vals.get('partner_id'):
            partner_obj = self.env['res.partner']
            #partner_rec = partner_obj.browse(vals['partner_id'])
            #partner_rec.write({'last_schedule_date':vals['date']})
            self.env.cr.execute("UPDATE res_partner set last_schedule_date = %s where id = %s", (vals['date'],vals['partner_id']))
        return res

class sale_order(models.Model):

    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        res=super(sale_order, self).create(vals)
        partner_obj = self.env['res.partner']
        if vals.get('partner_id') and vals.get('date_order'):
            partner_rec = partner_obj.browse(vals['partner_id'])
            partner_rec.write({'last_order_date':vals['date_order']})
        return res

    @api.multi
    def action_button_confirm(self):
        assert len(self._ids) == 1, 'This option should only be used for a single id at a time.'
        wf_service = netsvc.LocalService('workflow')
        wf_service.trg_validate(self._uid,'sale.order',self.id,'order_confirm',self._cr)
        for sale_data in self:
            sale_data.partner_id.write({'last_order_date':sale_data.date_confirm})
            # redisplay the record as a sales order
            view_ref = self.env['ir.model.data'].get_object_reference('sale', 'view_order_form')
            view_id = view_ref and view_ref[1] or False,
            return {
                'type': 'ir.actions.act_window',
                'name': _('Sales Order'),
                'res_model': 'sale.order',
                'res_id': self.id,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id,
                'target': 'current',
                'nodestroy': True,
            }

class res_partner(models.Model):

    _inherit='res.partner'

    @api.model
    def create(self, vals):
        if vals.get('account_number',False)==False:
            if len(vals['name'].replace(" ",""))>=3:
                name_acc=vals['name'].replace(" ","")[0:3]
            else:
                name_acc=vals['name'].replace(" ","")
            vals['account_number'] = (name_acc + self.env['ir.sequence'].get('res.partner')).upper()
        res = super(res_partner, self).create(vals)
        if vals.get('is_company') and vals.get('last_schedule_date') :
            self.env['crm.phonecall'].create({
                            'name' : vals.get('payment_next_action') or vals.get('name'),
                            'user_id' :self.env.uid,
                            'date' : vals.get('last_schedule_date'),
                            'partner_id':res.id,
                            'state':'open'})
                     
        return res

    def write(self, cr, uid, ids, vals, context=None):
		if context is None:
			context = {}
		print vals.get('last_schedule_date')
		if vals.get('last_schedule_date'):
			scheduled_obj = self.pool.get('crm.phonecall')
			scheduled_vals = {'name':'Follow up',
							  'date': vals.get('last_schedule_date'),
							  'user_id': uid,
							  'partner_id':ids[0],
				}
			scheduled_obj.create(cr, uid, scheduled_vals, context=context)
		return super(res_partner, self).write(cr, uid, ids, vals, context=context)


    @api.one
    @api.depends('name')
    def _get_name(self):
        if self.default_contact_id:
            self.default_contact_name = self.name

    default_contact_name = fields.Char(string='Default Contact', compute = '_get_name')

