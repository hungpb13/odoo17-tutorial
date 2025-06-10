from odoo import models, fields

class EstatePropertyTag(models.Model):
   _name = 'estate.property.tag'
   _description = 'Real Estate Property Tag'

   name = fields.Char(string='Name', required=True)
   property_ids = fields.Many2many('estate.property', string='Properties')


   _sql_constraints = [
      ('unique_tag_name', 'UNIQUE(name)', 'The tag name must be unique.')
   ]