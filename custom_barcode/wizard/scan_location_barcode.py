# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

    
# // opens a wizard when scans the location barcode
class LocationBarcode(models.TransientModel):
    _name = "location.barcode"
    
    location_id = fields.Many2one('stock.location', 'Source Location')
    location_dest_id = fields.Many2one(
        'stock.location', "Destination Location Zone")
    quantity = fields.Float("Quantity")
    product_id = fields.Many2one('product.product', 'Product')

# // creates a stock and returns to it's related form view
    @api.multi
    def submit(self):
        warehouse = self.env.user.warehouse_id
        warehouse_id = self.env['stock.picking.type'].search([('warehouse_id', '=', warehouse.id), ('name', '=', 'Internal Transfers')])
        move_lines = []
        move_vals = {}

        move_vals.update({
                        'product_id': self.product_id.id,
                        'product_uom_qty': self.quantity ,
                        'product_uom':self.product_id.uom_id.id,
                        'name': self.product_id.partner_ref,
                            })
        move_lines.append((0, 0, move_vals))
        
        values = {
                'location_id':self.location_id.id,
                'location_dest_id':self.location_dest_id.id,
                'picking_type_id':warehouse_id.id,
                'move_type':'one',
                'move_lines': move_lines,
                }
        if move_lines:
            stock_id = self.env['stock.picking'].create(values)
            
            context = dict(self.env.context or {})
            context['active_id'] = self.id
            return {
            'name': _('Internal Transfers'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'res_id': stock_id.id,
            'type': 'ir.actions.act_window',
            'context': context,
                }