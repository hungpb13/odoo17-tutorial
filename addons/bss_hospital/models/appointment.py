from odoo import models, fields, api


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _inherit = ['mail.thread']
    _rec_name = 'patient_id'

    reference = fields.Char(string='Reference', default='New')
    patient_id = fields.Many2one('hospital.patient', string='Patient')
    date = fields.Date(string='Appointment Date')
    note = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, val_list):
        for vals in val_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super().create(val_list)

    