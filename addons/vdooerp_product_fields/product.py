
from openerp import models, fields, api


class product_product(models.Model):
    """ add fields in product"""

    _inherit = "product.product"

    page_yield = fields.Integer(string='Page Yield')
    oem_part_num = fields.Char(string='OEM Part Number')
    lexmark_rebate_oem_part_num = fields.Char(string='Lexmark Rebate OEM Part Number')
    dealer_price = fields.Float(string='Dealer price', digit=(10,5))
    currency_id = fields.Many2one('res.currency', string='Currency')
    cost_to_price = fields.Float(string='Cost To Price')
    engine_based = fields.Char(string='Engine Based On')
    euro_graphics_price = fields.Char(string='Eurographics Price')
    euro_graphics_part = fields.Char(string='Eurographics Part Number')
    euro_special_yield = fields.Char(string='Eurographics Special Yield')

    @api.multi
    def update_currency(self):
        for product in self:
            amount = product.currency_id.compute(product.standard_price,product.currency_id,round=True)
            product.cost_to_price = amount



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
