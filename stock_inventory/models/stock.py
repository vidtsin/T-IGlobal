from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    
    product_uom = fields.Many2one('uom.uom', string='Product Unit of Measure')
    product_count = fields.Integer(string='Product Measure')
    
    
    @api.onchange('uom_id')
    def _onchange_uom_id(self):
        if self.uom_id:
            self.uom_po_id = self.uom_id.id
            self.product_uom = self.uom_id.id
    
    
class StockQuant(models.Model):
    _inherit = 'stock.quant'
    
    
    product_uom = fields.Many2one('uom.uom', string='Store UOM',compute='_compute_product_measure')
    product_count = fields.Integer(string='Store Qty',compute='_compute_product_measure')
    
    
    
    @api.depends('product_id')
    def _compute_product_measure(self):
        for order in self:
            value = 0
            if not order.product_id.product_uom == order.product_id.uom_id:
                if order.product_id.product_count > 0:
                    value = (self.quantity /order.product_id.product_count)
                    self.product_count= value
                    self.product_uom = order.product_id.product_uom
            else:
                self.product_uom = order.product_id.product_uom
                self.product_count= 0   
            

class Location(models.Model):
    _inherit = "stock.location"
    
    is_applicable = fields.Boolean(string='if applicable')   















                 
    