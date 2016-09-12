
from openerp import netsvc
from openerp import models, fields, api, _


class res_partner(models.Model):
    _inherit = "res.partner"

    prospect = fields.Boolean(string='Prospect')
    inactive_customer = fields.Boolean(string='Inactive customer')

class sale_order(models.Model):


    _inherit = "sale.order"

    @api.multi
    def action_button_confirm(self):
        assert len(self._ids) == 1, 'This option should only be used for a single id at a time.'
        wf_service = netsvc.LocalService('workflow')
        wf_service.trg_validate(self._uid, 'sale.order', self._ids[0], 'order_confirm', self._cr)
        for sale in self:
            if sale.partner_id.prospect:
                partner_rec = self.env['res.partner'].browse(sale.partner_id.id)
                partner_rec.write({'prospect': False})
            # redisplay the record as a sales order
            view_ref = self.env['ir.model.data'].get_object_reference('sale', 'view_order_form')
            view_id = view_ref and view_ref[1] or False,
            return {
                'type': 'ir.actions.act_window',
                'name': _('Sales Order'),
                'res_model': 'sale.order',
                'res_id': self._ids[0],
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id,
                'target': 'current',
                'nodestroy': True,
            }
