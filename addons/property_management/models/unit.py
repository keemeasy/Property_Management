from odoo import models, fields, api


class PropertyUnit(models.Model):
    _name = 'property.unit'
    _description = 'Property Unit'


    # BASIC INFORMATION ABOUT THE UNIT

    name = fields.Char(
        string="Unit Name",
        required=True
    )

    property_id = fields.Many2one(
        'property.property',
        string="Property",
        required=True
    )

    size = fields.Float(
        string="Size (m²)"
    )


    #  APARTMENT DETAILS

    number = fields.Char(
        string="Wohnungsnummer"
    )

    floor = fields.Integer(
        string="Etage"
    )

    rooms = fields.Float(
        string="Zimmer"
    )

    bathrooms = fields.Integer(
        string="Badezimmer"
    )

    has_cellar = fields.Boolean(
        string="Keller"
    )

    has_balcony = fields.Boolean(
        string="Balkon"
    )

    parking = fields.Boolean(
        string="Stellplatz"
    )   # RELATION TO LEASES

    lease_ids = fields.One2many(
        'property.lease',
        'unit_id',
        string="Mietverträge"
    )


    # CURRENT TENANT (first tenant from active lease)

    current_tenant_id = fields.Many2one(
        'res.partner',
        string="Current Tenant",
        compute="_compute_current_tenant",
        store=True
    )


    # ALL ACTIVE TENANTS (for tags)

    active_tenant_ids = fields.Many2many(
        'res.partner',
        string="Aktive Mieter",
        compute="_compute_active_tenant_ids"
    )


    # CURRENT RENT

    current_rent = fields.Float(
        string="Warmmiete",
        compute="_compute_current_rent",
        store=True
    )


    # OCCUPANCY STATUS

    occupancy_status = fields.Selection(
        [
            ('vacant', 'Frei'),
            ('rented', 'Vermietet')
        ],  string="Belegungsstatus",
        compute="_compute_occupancy_status",
        store=True
    )


    # FIRST TENANT

    @api.depends('lease_ids.state', 'lease_ids.tenant_ids')
    def _compute_current_tenant(self):

        for unit in self:

            active_lease = unit.lease_ids.filtered(
                lambda lease: lease.state == 'active'
            )

            unit.current_tenant_id = (
                active_lease[:1].tenant_ids[:1]
                if active_lease else False
            )


    # ALL TENANTS (WG support)

    @api.depends('lease_ids.state', 'lease_ids.tenant_ids')
    def _compute_active_tenant_ids(self):

        for unit in self:

            active_lease = unit.lease_ids.filtered(
                lambda lease: lease.state == 'active'
            )

            if active_lease:

                unit.active_tenant_ids = active_lease[0].tenant_ids

            else:

                unit.active_tenant_ids = False


    # CURRENT RENT

    @api.depends('lease_ids.state', 'lease_ids.total_rent')
    def _compute_current_rent(self):

        for unit in self:
            active_lease = unit.lease_ids.filtered(
                lambda lease: lease.state == 'active'
            )

            unit.current_rent = (
                active_lease[:1].total_rent
                if active_lease else 0.0
            )


    # OCCUPANCY STATUS

    @api.depends('lease_ids.state')
    def _compute_occupancy_status(self):

        for unit in self:

            active_lease = unit.lease_ids.filtered(
                lambda lease: lease.state == 'active'
            )

            unit.occupancy_status = (
                'rented'
                if active_lease
                else 'vacant'
            ) 
