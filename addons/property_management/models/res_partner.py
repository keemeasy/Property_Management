from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    building_id = fields.Many2one(
        'property.property',
        string="Building"
    )
