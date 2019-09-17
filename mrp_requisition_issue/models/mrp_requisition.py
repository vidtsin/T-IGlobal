from odoo import models,fields,api,_
from datetime import datetime, timedelta, date

class MrpRequisition(models.Model):
    _name = 'mrp.requisition'
    
    def _get_default_warehouse(self):
        warehouse_obj = self.env['stock.warehouse']
        warehouse_ids = warehouse_obj.search([('company_id', '=',self.env.user.company_id.id)])
        warehouse_id = warehouse_ids and warehouse_ids[0] or False
        return warehouse_id.id
    
    def _get_default_picking_type(self):
        warehouse_id = self._get_default_warehouse()
        if warehouse_id:
            warehouse_obj = self.env['stock.warehouse']
            warehouse_br = warehouse_obj.browse(warehouse_id)
            return warehouse_br and warehouse_br.int_type_id.id
        picking_type_obj = self.env['stock.picking.type']
        picking_type_ids = picking_type_obj.search([('code', '=', 'internal')])
        picking_type_id = picking_type_ids and picking_type_ids[0] or False
        return picking_type_id.id
    
    @api.depends('picking_ids.state')
    def _compute_state(self):
        state = ['done','cancel']
        state_list = []
        equal = True
        rec_state = [rec.state for rec in self.picking_ids]
        print(rec_state,'uuuuuuuuuuuuuuu')
        
        def all_same(items):
            return all(x == items[0] for x in items)
        
        if self.picking_ids:
            if len(rec_state) == 1:
                if 'done' in rec_state:
                    self.state = 'received'
                else:
                    self.state = 'inprogress'
            elif len(rec_state) > 1:
                state.sort()
                rec_state.sort()
                if all_same(rec_state):
                    if 'done' in rec_state:
                        self.state = 'received'
                elif state == rec_state:
                    self.state = 'received'
                else:
                    self.state = 'partially_available'      
        else:
                self.state = 'draft'
                
                
    name = fields.Char(string="Seq",copy=False)
    sequence_id = fields.Char(string="Sequence",copy=False)
    indentor_id = fields.Many2one('res.users',string="Requested by",default=lambda self: self.env.user.id,readonly=True)
    request_type = fields.Selection([('normal','Normal')])
    department_id = fields.Many2one('mrp.department',string="Department")
    location_id = fields.Many2one('stock.location',string="Destination Location")
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.user.company_id.id,readonly=True)
    indent_date = fields.Datetime('Indent Date')
    required_date = fields.Datetime('Required Date')
    approve_date = fields.Datetime('Approve Date')
    requirement = fields.Selection([('1','Ordinary'),('2','urgent')])
    type = fields.Selection([('stock','Stock')])
    warehouse_id = fields.Many2one('stock.warehouse','Warehouse',required=True,default=_get_default_warehouse)
    picking_type_id = fields.Many2one('stock.picking.type','Picking Type',required=True,default=_get_default_picking_type,copy=False)
    state = fields.Selection([('draft','Draft'),('confirm','Confirm'),('waiting_approval','Waiting For Approval'),('inprogress','In Progress'),('partially_available','Partially Available'),('received','Issued'),('reject','Rejected')],default='draft',compute='_compute_state',copy=False, index=True, readonly=True, store=True)
    mrp_requistion_lines = fields.One2many('mrp.requisition.lines','mrp_requistion_id',string="MRP Lines")
    picking_ids = fields.Many2many('stock.picking',string="Picking")
    mrp_production_id = fields.Many2one('mrp.production',string="MO")
    
    @api.model
    def create(self, values):
        values['sequence_id'] = self.env['ir.sequence'].next_by_code('mrp.requisition') 
        values['name'] = 'Reference' +" "+  values['sequence_id']
        return super(MrpRequisition, self).create(values)  
    
    @api.multi
    def action_confirm(self):
        self.state = 'waiting_approval'
    
    @api.multi
    def action_approve(self):
        move_lines = []
        move_vals = {}
        for lines in self.mrp_requistion_lines:
            move_vals = {}
            move_vals.update({
                            'product_id': lines.product_id.id,
                            'product_uom_qty': lines.product_uom_qty,
                            'product_uom':lines.product_uom_id.id,
                            'name': lines.product_id.default_code,
                            'mrp_requisition_line_id' :lines.id
                                })
            move_lines.append((0, 0, move_vals))
        print(move_lines,'fjsgfhuefrwgefhv')
        values = {
                'location_id':self.location_id.id,
                'location_dest_id':self.location_id.id,
                'picking_type_id':self.picking_type_id.id,
                'move_type':'one',
                'move_lines': move_lines,
                'mrp_requisition_issue':self.id
                }
        if move_lines:
            stock_id = self.env['stock.picking'].create(values)
            stock_id.action_confirm()
            self.picking_ids = [(6,0,stock_id.ids)]
        self.approve_date = datetime.now()
        self.state = 'inprogress'
    
    @api.multi
    def action_reject(self):
        self.state = 'reject'         
    
    @api.multi
    def action_issue_products(self):
        tree_id = self.env.ref('stock.vpicktree').id
        form_id = self.env.ref('stock.view_picking_form').id
        return {
            'name': _('Internal Transfers'),
            'view_type': 'form',
            'view_mode': 'tree',
            'res_model': 'stock.picking',
            'view_id':tree_id,
            'views': [(tree_id, 'tree'),(form_id,'form')],
            'type': 'ir.actions.act_window',
            'domain':[('mrp_requisition_issue','=',self.id)],
                }
    
    
class MrpRequisitionLines(models.Model):
    _name = 'mrp.requisition.lines'
    
    name = fields.Text('Purpose')
    product_id = fields.Many2one('product.product',string="Product",required=True)
    required_on = fields.Date('Required On',required=True)
    product_uom_qty = fields.Float('Quantity Required',required=True)
    product_uom_id = fields.Many2one('uom.uom',string="UOM",required=True)
    product_uom_qty_issued = fields.Float('Quantity Issued',readonly=True)
    qty_available = fields.Float('In Stock')
    mrp_requistion_id = fields.Many2one('mrp.requistion',string="MRP Requistion")
    
#     @api.depends('mrp_requistion_id')
#     def _qty_issued(self):
#         result = {}
#         stock_move_obj = self.env['stock.move']
#         for line in self:
#             if line.mrp_requistion_id:
#                 print(line.mrp_requistion_id)
#                 if line.mrp_requistion_id.picking_id:
#                     val = 0.0
#                     for record in stock_move_obj.search([('indent_line_id', '=', line.id), ('state', '=', 'done')]):
#                         stock_move = stock_move_obj.browse(record)
#                         val += stock_move.product_qty
#                     result[line.id]= val
#         return result
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.qty_available = self.product_id.qty_available
            self.product_uom_id = self.product_id.uom_id.id
        else:
            self.qty_available = 0.0
    
    
    
    