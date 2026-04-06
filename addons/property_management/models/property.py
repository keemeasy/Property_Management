from odoo import models, fields, api


class Property(models.Model):
    _name = 'property.property'
    _description = 'Property'


    # -----------------------------------------
    # BASIC PROPERTY INFORMATION
    # -----------------------------------------

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


    # -----------------------------------------
    # RELATION TO UNITS
    # each property can contain many units
    # -----------------------------------------

    unit_ids = fields.One2many(
        'property.unit',
        'property_id',
        string="Apartments"
    )


    # -----------------------------------------
    # STATISTICS
    # -----------------------------------------

    # TOTAL NUMBER OF UNITS IN BUILDING
    # automatically counts related units

    unit_count = fields.Integer(
        string="Einheiten",
        compute="_compute_unit_count",
        store=True
    )


    # NUMBER OF RENTED UNITS
    # counts apartments where occupancy_status = rented

    rented_count = fields.Integer(
        string="Vermietet",
        compute="_compute_rented_count",
        store=True
    )


    # NUMBER OF VACANT UNITS
    # counts apartments where occupancy_status = vacant

    vacant_count = fields.Integer(
        string="Leerstand",
        compute="_compute_vacant_count",
        store=True
    )


    # -----------------------------------------
    # BULK CREATION HELPER FIELDS
    # used to quickly generate multiple units
    # without manually creating each one
    # -----------------------------------------

    bulk_unit_count = fields.Integer(
        string="Anzahl neue Einheiten"
    )


    bulk_start_number = fields.Integer(
        string="Startnummer",
        default=1
    )


    # optional default values
    # used when creating multiple similar apartments

    bulk_default_size = fields.Float(
        string="Standard m²"
    )


    bulk_default_rooms = fields.Float(
        string="Standard Zimmer"
    )


    bulk_default_bathrooms = fields.Integer(
        string="Standard Badezimmer"
    )


    bulk_default_floor = fields.Integer(
        string="Standard Etage"
    )


    bulk_default_balcony = fields.Boolean(
        string="Standard Balkon"
    )


    bulk_default_cellar = fields.Boolean(
        string="Standard Keller"
    )


    # -----------------------------------------
    # COMPUTE METHODS
    # -----------------------------------------

    @api.depends('unit_ids')
    def _compute_unit_count(self):

        for record in self:

            record.unit_count = len(record.unit_ids)


    @api.depends('unit_ids.occupancy_status')
    def _compute_rented_count(self):

        for record in self:

            rented_units = record.unit_ids.filtered(
                lambda u: u.occupancy_status == 'rented'
            )

            record.rented_count = len(rented_units)


    @api.depends('unit_ids.occupancy_status')
    def _compute_vacant_count(self):

        for record in self:

            vacant_units = record.unit_ids.filtered(
                lambda u: u.occupancy_status == 'vacant'
            )

            record.vacant_count = len(vacant_units)


    # -----------------------------------------
    # BULK GENERATOR FUNCTIONS
    # -----------------------------------------

    def action_generate_empty_units(self):
        """
        Creates empty units quickly.

        Example:
        15 empty apartments created instantly.
        User fills details afterwards.

        Does NOT overwrite existing units.
        """

        for record in self:

            if not record.bulk_unit_count:
                continue

            for i in range(record.bulk_unit_count):

                number = record.bulk_start_number + i

                self.env["property.unit"].create({

                    "name": f"Einheit {number}",

                    "number": str(number),

                    "property_id": record.id,

                })


    def action_generate_prefilled_units(self):
        """
        Creates units with predefined values.

        Useful when many apartments have similar layout.

        Example:
        10 apartments
        60m²
        2 rooms
        balcony
        """

        for record in self:

            if not record.bulk_unit_count:
                continue

            for i in range(record.bulk_unit_count):

                number = record.bulk_start_number + i

                self.env["property.unit"].create({

                    "name": f"Einheit {number}",

                    "number": str(number),

                    "property_id": record.id,

                    "size": record.bulk_default_size,

                    "rooms": record.bulk_default_rooms,

                    "bathrooms": record.bulk_default_bathrooms,

                    "floor": record.bulk_default_floor,

                    "has_balcony": record.bulk_default_balcony,

                    "has_cellar": record.bulk_default_cellar,

                })
