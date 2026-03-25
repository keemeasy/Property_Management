from odoo import models, fields

class PropertyUnit(models.Model):
    _name = 'property.unit'
    _description = 'Property Unit'

    name = fields.Char(string="Unit Name", required=True)
    property_id = fields.Many2one('property.property', string="Property", required=True)

    size = fields.Float(string="Size (m²)")
    rent = fields.Float(string="Monthly Rent")

    tenant_id = fields.Many2one('res.partner', string="Tenant")
