from odoo import models, fields, api


class Property(models.Model):
    _name = 'property.property'
    _description = 'Property'


    name = fields.Char(
        string="Property Name",
        required=True
    )


    street = fields.Char(
        string="Street"
    )

    city = fields.Char(
        string="City"
    )

    zip = fields.Char(
        string="ZIP"
    )

    country = fields.Char(
        string="Country"
    )


    owner_id = fields.Many2one(
        'res.partner',
        string="Owner"
    )


    unit_ids = fields.One2many(
        'property.unit',
        'property_id',
        string="Apartments"
    )


    # TOTAL NUMBER OF UNITS IN BUILDING
    # counts how many apartments belong to this property

    unit_count = fields.Integer(
        string="Einheiten",
        compute="_compute_unit_count",
        store=True
    )


    # NUMBER OF RENTED UNITS
    # counts apartments where status = rented

    rented_count = fields.Integer(
        string="Vermietet",
        compute="_compute_rented_count",
        store=True
    )


    # NUMBER OF VACANT UNITS
    # counts apartments where status = vacant

    vacant_count = fields.Integer(
        string="Leerstand",
        compute="_compute_vacant_count",
        store=True
    )


    # COMPUTE TOTAL UNITS

    @api.depends('unit_ids')
    def _compute_unit_count(self):

        for record in self:

            record.unit_count = len(record.unit_ids)


    # COMPUTE RENTED UNITS

    @api.depends('unit_ids.occupancy_status')
    def _compute_rented_count(self):

        for record in self:

            rented_units = record.unit_ids.filtered(
                lambda u: u.occupancy_status == 'rented'
            )

            record.rented_count = len(rented_units)


    # COMPUTE VACANT UNITS

    @api.depends('unit_ids.occupancy_status')
    def _compute_vacant_count(self):

        for record in self:

            vacant_units = record.unit_ids.filtered(
                lambda u: u.occupancy_status == 'vacant'
            )

            record.vacant_count = len(vacant_units)
