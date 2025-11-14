# Example of a correct __manifest__.py
{
    "name": "Real estate",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_offer_views.xml",
        "views/estate_property_tag_views.xml",
        "views/estate_property_type_views.xml",
        "views/estate_property_views.xml",
        "views/property_type_views.xml",
        "views/real_estate_menus.xml"
    ],
    "installable": True,
    "application": True,
}