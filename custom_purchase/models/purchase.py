from odoo import api, models, fields, _



class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    purchase_reference = fields.Char('Reference',readonly=True)

    @api.multi
    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for order in self:
            reference =order.name
            if order.name[:2] == 'PQ':                
                order.write({
                    'purchase_reference': reference,
                    'name': self.env['ir.sequence'].next_by_code('pruchase.order.sequence')
                })
                
                
        return res
        
        

