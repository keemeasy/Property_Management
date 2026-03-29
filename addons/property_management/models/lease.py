from odoo import models, fields, api


class PropertyLease(models.Model):
    _name = 'property.lease'
    _description = 'Mietvertrag'
    _rec_name = 'name'


    name = fields.Char(
        string="Vertragsnummer",
        required=True
    )

    tenant_id = fields.Many2one(
        'res.partner',
        string="Mieter",
        required=True
    )

    unit_id = fields.Many2one(
        'property.unit',
        string="Wohnung",
        required=True
    )

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


    cold_rent = fields.Float(string="Kaltmiete")

    additional_cost = fields.Float(
        string="Nebenkosten"
    )

    heating_cost = fields.Float(
        string="Heizkosten"
    )

    total_rent = fields.Float(
        string="Warmmiete",
        compute="_compute_total_rent",
        store=True
    )


    deposit = fields.Float(
        string="Kaution"
    )


    contract_file = fields.Binary(
        string="Vertrag PDF"
    )

    contract_filename = fields.Char(
        string="Dateiname"
    )


    state = fields.Selection(
        [
            ('draft', 'Entwurf'),
            ('active', 'Aktiv'),
            ('terminated', 'Beendet')
        ],
        default='draft',
        string="Status"
    )


    @api.depends('cold_rent', 'additional_cost', 'heating_cost')
    def _compute_total_rent(self):

        for record in self:

            record.total_rent = (
                (record.cold_rent or 0.0)
                + (record.additional_cost or 0.0)
                + (record.heating_cost or 0.0)
            )
