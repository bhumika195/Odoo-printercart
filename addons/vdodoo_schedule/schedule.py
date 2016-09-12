from datetime import datetime
from openerp import workflow
from openerp import fields, models, api, exceptions, _
from openerp.osv import osv

class res_partner(models.Model):
    """Travel"""
    _inherit = 'res.partner'


    def write(self, cr, uid, ids, vals, context=None):
        # stage change: update date_last_stage_update
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            if record.is_company  :       
                pho_obj=self.pool.get('crm.phonecall')
                if 'last_schedule_date' in vals  and  vals.get('payment_next_action') :
                    vals1 = {
                            'name' : vals.get('payment_next_action'),
                            'user_id' : uid ,
                            'date' : vals.get('last_schedule_date'),
                            'partner_id':record.id,
                            'state':'open'
                            
                    }
                    new_id = pho_obj.create(cr, uid, vals1, context=context)
        return super(res_partner, self).write(cr, uid, ids, vals, context=context)
