# -*- coding: utf-8 -*-
from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'real_estate.estate_property_type'
    _description = 'Property type'

    _sql_constraints = ["name_uniq", "unique(name)", "The property type name must be unique."]

    name = fields.Char(required=True)
