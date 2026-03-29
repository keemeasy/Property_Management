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


    # OLD RENT FIELD (manual)
    # kept for compatibility for now
    # later we may remove it

    rent = fields.Float(
        string="Monthly Rent"
    )


    # OLD TENANT FIELD (manual)
    # still kept so nothing breaks
    # replaced by automatic tenant below

    tenant_id = fields.Many2one(
        'res.partner',
        string="Tenant"
    )


    # RELATION TO LEASES
    # one unit can have multiple leases over time

    lease_ids = fields.One2many(
        'property.lease',
        'unit_id',
        string="Mietverträge"
    )


    # CURRENT TENANT (automatic)
    # takes tenant from ACTIVE lease

    current_tenant_id = fields.Many2one(
        'res.partner',
        string="Current Tenant",
        compute="_compute_current_tenant",
        store=True
    )


    # CURRENT RENT (automatic Warmmiete)
    # takes Warmmiete from ACTIVE lease

    current_rent = fields.Float(
        string="Current Rent",
        compute="_compute_current_rent",
        store=True
    )


    # COMPUTE CURRENT TENANT
    # finds lease where state = active
    # extracts tenant from that lease

    @api.depends('lease_ids.state', 'lease_ids.tenant_id')
    def _compute_current_tenant(self):

        for unit in self:

            active_lease = unit.lease_ids.filtered(
                lambda lease: lease.state == 'active'
            )

            unit.current_tenant_id = (
                active_lease[:1].tenant_id
                if active_lease else False
            )


    # COMPUTE CURRENT RENT (Warmmiete)
    # finds active lease
    # extracts total_rent from lease

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


    # BELEGUNGSSTATUS (automatic)
    # shows if the unit is currently rented or vacant
    # based on ACTIVE lease

    occupancy_status = fields.Selection(

        [
            ('vacant', 'Frei'),
            ('rented', 'Vermietet')
        ],

        string="Belegungsstatus",

        compute="_compute_occupancy_status",

        store=True
    )


    # COMPUTE BELEGUNGSSTATUS
    # if active lease exists → Vermietet
    # otherwise → Frei

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
