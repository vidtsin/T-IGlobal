from odoo import models,fields,api

class Department(models.Model):
    _name = 'mrp.department'
    
    name = fields.Char(string='Name')
    