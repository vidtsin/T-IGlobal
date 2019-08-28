# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


# // Inherits res users
class Users(models.Model):

    _inherit = "res.users"

    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', domain="[('company_id', '=',company_id)]")