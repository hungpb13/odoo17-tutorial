from odoo import models, fields


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=True, tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True)
    tag_ids = fields.Many2many(
        'patient.tag', 
        'patient_tag_rel', 
        'patient_id',
        'tag_id',
        string='Tags', tracking=True)
    
    def unlink(self):
        print("Super method called for unlink")
        return super().unlink()