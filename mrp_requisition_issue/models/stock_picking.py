from odoo import models,fields,api
from datetime import datetime, timedelta, date

class Picking(models.Model):
    _inherit = "stock.picking"
    
    mrp_requisition_issue = fields.Many2one('mrp.requisition',string="MRP requisition")
    
    @api.model
    def create(self, vals):
        res = super(Picking, self).create(vals)
        if res.backorder_id:
            if res.backorder_id.mrp_requisition_issue:
                res.mrp_requisition_issue = res.backorder_id.mrp_requisition_issue.id
                res.mrp_requisition_issue.write({'picking_ids':[(4,res.id)]}) 
        return res