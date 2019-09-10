from odoo import models,fields,api
from datetime import datetime, timedelta, date

class StockMove(models.Model):
    _inherit = "stock.move"
    
    mrp_requisition_line_id = fields.Many2one('mrp.requisition.lines',string="MRP requisition")
    
    def write(self, vals):
        res = super(StockMove, self).write(vals)
        if vals.get('state') == 'done':
            for move in self:
                if move.product_uom_qty > 0.0:
                    if move.mrp_requisition_line_id:
                        if move.mrp_requisition_line_id.product_uom_qty_issued >= 0.0:
                            move.mrp_requisition_line_id.product_uom_qty_issued += move.product_uom_qty
#                 elif self.mrp_requisition_line_id.product_uom_qty_issued > 0.0:
#                     self.mrp_requisition_line_id.product_uom_qty_issued += self.product_uom_qty
        return res