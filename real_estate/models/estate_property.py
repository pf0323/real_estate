from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "real_estate.estate_property"
    _description = "Property"

    name = fields.Char(required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    tag_ids = fields.Many2many(
        comodel_name="real_estate.estate_property_tag", string="Tags")
    state = fields.Selection([
        ("new", "New"),
        ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("canceled", "Canceled"),
    ], string="Status", copy=False, required=True, default="new")
    property_type_id = fields.Many2one(
        comodel_name="real_estate.estate_property_type", string="Property Type")
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    best_offer = fields.Float(compute="_compute_best_offer")
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),])
    offer_ids = fields.One2many(
        comodel_name="real_estate.estate_property_offer",
        inverse_name="property_id",
        string="Offers"
    )
    total_area = fields.Integer(compute="_compute_total_area")
    buyer_id = fields.Many2one(
        comodel_name="res.partner", ondelete="restrict", string="Buyer")
    salesperson_id = fields.Many2one(
        comodel_name="res.users", default=lambda self: self.env.user, ondelete="restrict", string="Salesperson",)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped('price'), default=0)
    
    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = self.garden and 10
        self.garden_orientation = self.garden and 'north'

    def action_sold(self):
        if self.filtered(lambda p: p.state == "canceled"):
            raise UserError(_("A canceled properties cannot be sold."))
        self.write({'state': 'sold'})
        return True

    def action_cancel(self):
        if self.filtered(lambda p: p.state == "sold"):
            raise UserError(_("A sold property cannot be canceled."))
        self.filtered(lambda p: p.state != "canceled").write({'state': 'canceled'})
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self): 
        for property in self:
            if property.selling_price and float_compare(
                property.selling_price,
                property.expected_price * 0.9,
                precision_digits=2
            ) == -1:
                raise ValidationError(_(
                    "The selling price of the property '%s' must be at least 90%% of the expected price."
                ) % property.name)

    _sql_constraints = [
        ("check_expected_price_positive", "CHECK(expected_price > 0)", "The expected price must be strictly positive."),
        ("check_selling_price_positive", "CHECK(selling_price IS NULL OR selling_price >= 0)", "The selling price must be positive.")
    ]