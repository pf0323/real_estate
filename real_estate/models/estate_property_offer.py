from odoo import api, models, fields, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'real_estate.estate_property_offer'
    _description = 'Property Offer'
    _order = 'price desc'

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The offer price must be positive.")
    
    price = fields.Float(string='Price', required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string='Status', copy=False)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True
    )
    property_id = fields.Many2one(
        comodel_name='real_estate.estate_property',
        string='Property',
        required=True
    )
    validity = fields.Integer(string='Validity (days)', default=7)
    deadline_date = fields.Date(
        string='Deadline',
        compute='_compute_deadline_date',
        inverse='_inverse_deadline_date'
    )

    @api.depends('validity', 'create_date')
    def _compute_deadline_date(self):
        for offer in self:
            if offer.create_date:
                base_date = fields.Date.to_date(offer.create_date)
            else:
                base_date = fields.Date.today()
            offer.deadline_date = fields.Date.add(base_date, days=offer.validity)

    def _inverse_deadline_date(self):
        for offer in self:
            if offer.deadline_date:
                if offer.create_date:
                    create_date = fields.Date.to_date(offer.create_date)
                else:
                    create_date = fields.Date.today()
                offer.validity = (offer.deadline_date - create_date).days

    def action_accept(self):
        for offer in self:
            offer_property = offer.property_id
            if offer_property.offer_ids.filtered(lambda o: o.status == 'accepted'):
                raise UserError(_("Property '%s' already has an accepted offer!.", offer_property.name))
            offer.status = 'accepted'
            offer_property.selling_price = offer.price
            offer_property.buyer_id = offer.partner_id
            offer_property.state = 'offer_accepted'
        return True
    
    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True