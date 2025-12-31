from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    propinsi_id = fields.Many2one('cdn.propinsi', string='Propinsi')
    kota_id = fields.Many2one('cdn.kota', string='kota')
    kecamatan_id = fields.Many2one('cdn.kecamatan', string='Kecamatan')
    desa_id = fields.Many2one('cdn.desa', string='Desa')
    jenis_kelamin = fields.Selection(string='Jenis Kelamin', 
                    selection=[('l', 'Laki Laki'), 
                               ('p', 'Perempuan')])   