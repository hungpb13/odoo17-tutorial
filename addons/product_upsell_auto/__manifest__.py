# -*- coding: utf-8 -*-
{
    "name": "Product Upsell Auto",
    "version": "17.0.1.0.0",
    "category": "Website/eCommerce",
    "summary": "Automatic product upsell recommendations based on data analysis",
    "description": """
        This module provides automatic product upsell recommendations for Odoo eCommerce:
        
        Features:
        - Automatic upsell product recommendations based on category and price
        - Smart algorithm to suggest higher-priced products in same category
        - Automated cron job to update recommendations daily
        - Beautiful frontend display of upsell suggestions
        - Backend management of recommendations
        
        Key Benefits:
        - Increase average order value automatically
        - Reduce manual work of setting up upsell products
        - Data-driven recommendations
        - Improved customer experience with relevant suggestions
        - Easy integration with existing eCommerce setup
    """,
    "author": "Beemart",
    "website": "https://beemart.vn",
    "depends": [
        "product",
        "website_sale",
        "sale_management",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_views.xml",
        "views/recommendation_views.xml",
        "views/website_templates.xml",
        "data/ir_cron.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "product_upsell_auto/static/src/css/upsell.css",
        ],
    },
    "installable": True,
    "auto_install": False,
    "application": False,
    "license": "LGPL-3",
}
