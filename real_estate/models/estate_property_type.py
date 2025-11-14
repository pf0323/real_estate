# -*- coding: utf-8 -*-
from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = 'real_estate.estate_property_type'
    _description = 'Property type'

    name = fields.Char(required=True)
