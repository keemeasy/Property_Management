from odoo import models, fields, api


class PropertyLease(models.Model):
    _name = 'property.lease'
    _description = 'Mietvertrag'
    _rec_name = 'name'


    # -----------------------------------------
    # BASIC CONTRACT INFORMATION
    # -----------------------------------------

    name = fields.Char(
        string="Vertragsnummer",
        required=True
    )


    tenant_ids = fields.Many2many(
        'res.partner',
        string="Mieter",
        required=True
    )


    # connection to the apartment (Wohnung)
    unit_id = fields.Many2one(
        'property.unit',
        string="Wohnung",
        required=True
    )


    # automatically pulls the building from the selected unit
    # ensures lease always belongs to correct building
    property_id = fields.Many2one(
        'property.property',
        string="Gebäude",
        related="unit_id.property_id",
        store=True
    )


    start_date = fields.Date(
        string="Mietbeginn",
        required=True
    )


    end_date = fields.Date(
        string="Mietende"
    )


    contract_type = fields.Selection(
        [
            ('unlimited', 'Unbefristet'),
            ('fixed', 'Befristet'),
            ('sublease', 'Untermiete')
        ],
        default='unlimited',
        string="Vertragstyp"
    )


    # -----------------------------------------
    # RENT VALUES
    # -----------------------------------------

    cold_rent = fields.Float(
        string="Kaltmiete"
    )


    additional_cost = fields.Float(
        string="Nebenkosten"
    )


    heating_cost = fields.Float(
        string="Heizkosten"
    )


    # Warmmiete is automatically calculated
    # formula:
    # Warmmiete = Kaltmiete + Nebenkosten + Heizkosten
    total_rent = fields.Float(
        string="Warmmiete",
        compute="_compute_total_rent",
        store=True
    )


    deposit = fields.Float(
        string="Kaution"
    )


    # -----------------------------------------
    # CONTRACT DOCUMENT
    # -----------------------------------------

    contract_file = fields.Binary(
        string="Vertrag PDF"
    )


    contract_filename = fields.Char(
        string="Dateiname"
    )


    # -----------------------------------------
    # CONTRACT STATUS
    # -----------------------------------------

    state = fields.Selection(
        [
            ('draft', 'Entwurf'),
            ('active', 'Aktiv'),
            ('terminated', 'Beendet')
        ],
        default='draft',
        string="Status"
    )


    # -----------------------------------------
    # UNIT INFORMATION (Wohnungsdetails)
    # these fields automatically show data
    # from property.unit
    # no duplicated data stored in lease
    # -----------------------------------------

    unit_size = fields.Float(
        related="unit_id.size",
        string="Wohnfläche (m²)",
        readonly=True
    )


    unit_rooms = fields.Float(
        related="unit_id.rooms",
        string="Zimmer",
        readonly=True
    )


    unit_bathrooms = fields.Integer(
        related="unit_id.bathrooms",
        string="Badezimmer",
        readonly=True
    )


    unit_floor = fields.Integer(
        related="unit_id.floor",
        string="Etage",
        readonly=True
    )


    unit_balcony = fields.Boolean(
        related="unit_id.has_balcony",
        string="Balkon",
        readonly=True
    )


    unit_cellar = fields.Boolean(
        related="unit_id.has_cellar",
        string="Keller",
        readonly=True
    )


    # -----------------------------------------
    # COMPUTE FUNCTIONS
    # -----------------------------------------

    @api.depends('cold_rent', 'additional_cost', 'heating_cost')
    def _compute_total_rent(self):

        for record in self:

            record.total_rent = (
                (record.cold_rent or 0.0)
                + (record.additional_cost or 0.0)
                + (record.heating_cost or 0.0)
            )
