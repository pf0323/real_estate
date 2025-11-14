from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'real_estate.estate_property_tag'
    _description = 'Property Tag'

    _sql_constraints = [
        ("name_unique", "UNIQUE(name)", "The tag name must be unique.")
    ]
    
    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')  # Para darle colores a los tags en la vista
