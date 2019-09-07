from odoo import api, models, fields, _



class PurchaseOrder(models.Model):
    _inherit = "purchase.order"


    @api.multi
    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for order in self:
            if order.name[:2] == 'PQ':
                order.name = self.env['ir.sequence'].next_by_code('pruchase.order.sequence')
        return res
        
        

