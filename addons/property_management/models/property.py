from odoo import models, fields

class Property(models.Model):
    _name = 'property.property'
    _description = 'Property'

    name = fields.Char(string="Property Name", required=True)

    street = fields.Char(string="Street")
    city = fields.Char(string="City")
    zip = fields.Char(string="ZIP")
    country = fields.Char(string="Country")

    owner_id = fields.Many2one(
        'res.partner',
        string="Owner"
    )

    unit_ids = fields.One2many(
        'property.unit',
        'property_id',
        string="Apartments"
    )
