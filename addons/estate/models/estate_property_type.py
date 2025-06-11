from odoo import models, fields

class EstatePropertyType(models.Model):
   _name = 'estate.property.type'
   _description = 'Real Estate Property Type'
   _order = 'sequence, name'

   name = fields.Char(string='Name', required=True)
   sequence = fields.Integer(string='Sequence', default=10)
   property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')


   _sql_constraints = [
      ('unique_type_name', 'UNIQUE(name)', 'The property type name must be unique.')
   ]