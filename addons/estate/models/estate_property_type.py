from odoo import models, fields, api

class EstatePropertyType(models.Model):
   _name = 'estate.property.type'
   _description = 'Real Estate Property Type'
   _order = 'sequence, name'

   name = fields.Char(string='Name', required=True)
   sequence = fields.Integer(string='Sequence', default=10)
   property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
   offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
   offer_count = fields.Integer(string='Offer Count', compute='_compute_offer_count')


   _sql_constraints = [
      ('unique_type_name', 'UNIQUE(name)', 'The property type name must be unique.')
   ]


   @api.depends('offer_ids')
   def _compute_offer_count(self):
      for record in self:
         record.offer_count = len(record.offer_ids)