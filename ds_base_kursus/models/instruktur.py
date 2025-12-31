from odoo import models, fields, api


class Instruktur(models.Model):
    _name = 'cdn.instruktur'
    _description = 'Instruktur'
    _inherits = {'res.partner': 'partner_id'}
    
    partner_id = fields.Many2one('res.partner', string='partner', ondelete='cascade', required=True)
    keahlian_ids = fields.Many2many('cdn.keahlian', string='Keahlian')


class Keahlian(models.Model):
    _name = 'cdn.keahlian'
    _description = 'Nama Keahlian'

    name = fields.Char(string='Nama Keahlian', required=True)


    




    
    

    
    
    
    
    




    