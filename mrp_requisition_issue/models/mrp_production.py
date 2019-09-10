# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from psycopg2 import IntegrityError

from datetime import datetime, timedelta, date


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    is_hide_mr = fields.Boolean('Hide MR',default=False)
    
    @api.multi
    def action_material_request(self):
        bom_lines = []
        bom_vals = {}
        for lines in self.move_raw_ids:
            bom_vals = {}
            bom_vals.update({
                            'product_id': lines.product_id.id,
                            'product_uom_qty': lines.product_uom_qty,
                            'product_uom_id':lines.product_uom.id,
                            'required_on':datetime.now().date(),
                                })
            bom_lines.append((0, 0, bom_vals))
        print(bom_lines)
        values = {
                'indent_id':self.env.user.id,
#                 'request_typq':'normal',
                'indent_date':datetime.now(),
                'required_date':datetime.now(),
                'mrp_requistion_lines':bom_lines,
                'requirement':'1',
                'type':'stock'
                }
        if bom_lines:
            mrp_requisition_id = self.env['mrp.requisition'].create(values)
            print(mrp_requisition_id)
            mrp_requisition_id.write({'mrp_production_id':self.id})
            self.is_hide_mr = True
            
    @api.multi
    def material_request(self):
        form_id = self.env.ref('mrp_requisition_issue.view_mrp_requisition_form').id
        mrp_requisition_id = self.env['mrp.requisition'].search([('mrp_production_id','=',self.id)])
        return {
            'name': _('Material Requisition'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mrp.requisition',
            'view_id':form_id,
            'res_id':mrp_requisition_id.id,
            'views': [(form_id,'form')],
            'type': 'ir.actions.act_window',
#             'domain':[('mrp_production_id','=',self.id)],
                }
            
          
    
    





