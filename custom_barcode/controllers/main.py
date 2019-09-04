from odoo import http, _
from odoo.http import request
from odoo import http, _, tools
from datetime import datetime, date
from odoo import api, fields, models, _
from odoo.addons.stock_barcode.controllers.main import StockBarcodeController


# // Inherits the Main menu of Barcode
class StockBarcodeController(StockBarcodeController):

    @http.route('/stock_barcode/scan_from_main_menu', type='json', auth='user')
    def main_menu(self, barcode, **kw):
        """ Receive a barcode scanned from the main menu and return the appropriate
            action (open an existing / new picking) or warning.
        """
        ret_open_picking = self.try_open_picking(barcode)
        if ret_open_picking:
            return ret_open_picking

        purchase_open_picking = self.try_open_picking(barcode)
        if purchase_open_picking:
            return purchase_open_picking

        if request.env.user.has_group('stock.group_stock_multi_locations'):
            ret_new_internal_picking = self.try_new_internal_picking(barcode)
            if ret_new_internal_picking:
                return ret_new_internal_picking

        if request.env.user.has_group('stock.group_stock_multi_locations'):
            return {'warning': _('No data corresponding to barcode %(barcode)s') % {'barcode': barcode}}
        else:
            return {'warning': _('No picking or return corresponding to barcode %(barcode)s') % {'barcode': barcode}}

# // inherits the domian for scanning without the particular states for stock picking 
# // scans the return, sale and purchase orders barcodes
# // Scans the products and product variants barcodes
    def try_open_picking(self, barcode):
        """ If barcode represents a picking, open it
        """
        corresponding_picking = request.env['stock.picking'].search([
            ('name', '=', barcode),
        ], limit=1)
        
        """ If barcode represents a Return Order, open it
        """
#         corresponding_return = request.env['return.order'].search([
#             ('number', '=', barcode),
#         ], limit=1)
        
        corresponding_purchase = request.env['purchase.order'].search([
            ('name', '=', barcode),
        ], limit=1)
        
        """ If barcode represents a Sale Order, open it
            """
        corresponding_sale = request.env['sale.order'].search([
            ('name', '=', barcode),
        ], limit=1)
 
        """ If barcode represents a Product, open it
            """
        corresponding_product_variant = request.env['product.product'].search([
            ('barcode', '=', barcode),
        ], limit=1)
        
        if corresponding_picking:
            action_picking_form = request.env.ref('stock_barcode.stock_picking_action_form')
            action_picking_form = action_picking_form.read()[0]
            action_picking_form['res_id'] = corresponding_picking.id
            return {'action': action_picking_form}
#         
#         if corresponding_return:
#             action_picking_form = request.env.ref('website_shop_return_rma.stock_return_action_form')
#             action_picking_form = action_picking_form.read()[0]
#             action_picking_form['res_id'] = corresponding_return.id
#             return {'action': action_picking_form}
        
        if corresponding_purchase:
            action_picking_form = request.env.ref('custom_barcode.purchase_form_action_barcode')
            action_picking_form = action_picking_form.read()[0]
            action_picking_form['res_id'] = corresponding_purchase.id
            return {'action': action_picking_form}
        
        if corresponding_sale:
            action_picking_form = request.env.ref('custom_barcode.action_quotations_custom')
            action_picking_form = action_picking_form.read()[0]
            action_picking_form['res_id'] = corresponding_sale.id
            return {'action': action_picking_form}
        print(corresponding_product_variant,"corresponding_product_variant")
        if corresponding_product_variant:
            action_rec = request.env['ir.model.data'].xmlid_to_object('custom_barcode.stock_barcode_src_location_action_main_menu')
            if action_rec:
                request.session['barcode_product_id'] = corresponding_product_variant.id
                return {'action':action_rec.read()[0]}
            
        return False

# Scans the first form and displays the source form

    @http.route('/custom_barcode/scan_src_location', type='json', auth='user')
    def scan_src_location(self, barcode, **kw):
        """ Receive a barcode scanned from the main menu and return the appropriate
            action (open an existing / new picking) or warning.
        """
        print(request.session)
        if not request.session.get('barcode_product_id'):

            return {'warning': _('Please scan product one more time')}
        print(barcode)
        source_location = request.env['stock.location'].search([('barcode', '=', barcode)])
        
        if not source_location:
            return {'warning': _('No location found')}
            
        if len(source_location) > 1:
            return {'warning': _('Warehouse name must be unique')}
        
        else:
            action_rec = request.env['ir.model.data'].xmlid_to_object('custom_barcode.stock_barcode_location_action_main_menu')
            print(action_rec,'sss')
            if action_rec:
                request.session['source'] = source_location.id
                return {'action':action_rec.read()[0]}
    
# Scans the second form and displays the destination form
    @http.route('/custom_barcode/scan_location', type='json', auth='user')
    def scan_location(self, barcode, **kw):
        """ Receive a barcode scanned from the main menu and return the appropriate
            action (open an existing / new picking) or warning.
        """
        print(request.session, "request.session")
        if request.session.get('barcode_product_id'):
            product_id = request.session['barcode_product_id']
        else:
            return {'warning': _('Please scan product one more time')}

        destination_location = request.env['stock.location'].search([('barcode', '=', barcode)])
        print(destination_location,'lllll')
        if request.session.get('source'):
            location_id = request.session['source']
        
        if len(destination_location) > 1:
            return {'warning': _('Warehouse name must be unique')}
        else:
            values = request.env['location.barcode'].create({
                                                'location_id':location_id,
                                                'location_dest_id':destination_location.id,
                                                'product_id':product_id,
                                                'quantity':1,
                                                })
            action_picking_form = request.env.ref('custom_barcode.location_barcode_action_menu')
            action_picking_form = action_picking_form.read()[0]
            action_picking_form['res_id'] = values.id
            return {'action': action_picking_form}
