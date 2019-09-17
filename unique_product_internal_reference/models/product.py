from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

class Product(models.Model):
    _inherit = "product.template"
    
    @api.one
    @api.constrains('default_code')
    def validate_default_code(self):
        rec = self.search([('default_code','=',self.default_code)])
        if rec:
            if self.default_code:
                for res in rec:
                    if res.id != self.id:
                        raise ValidationError(_("Internal Reference must be unique"))
