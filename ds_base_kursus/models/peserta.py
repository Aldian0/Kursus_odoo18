from odoo import models, fields, api


class Peserta(models.Model):
    _name = 'cdn.peserta'
    _description = 'Data Peserta'
    _inherits = {'res.partner':'partner_id'}

    partner_id = fields.Many2one('res.partner', string='Partner ID', required=True, ondelete='cascade')

    pendidikan = fields.Selection([
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
        ('s1', 'Sarjana S1')
    ], string='Pendidikan')

    pekerjaan = fields.Char(string='Pekerjaan')
    is_menikah = fields.Boolean(string='Sudah Menikah')
    image = fields.Binary(string="Foto Peserta")
    nama_pasangan = fields.Char(string='Nama Pansangan')
    hp_pasangan = fields.Char(string='HP Pasangan')
    tmp_lahir = fields.Char(string='Tempat Lahir')
    tgl_lahir = fields.Date(string='Tanggal Lahir')
    mobile = fields.Char(string='No Telp')
    email = fields.Char(string='Email')
    no_peserta = fields.Char(string='No Peserta', readonly=True, copy=True, default='New')


    @api.model
    def create(self, vals):
        if vals.get('no_peserta', 'New') == 'New':
            vals['no_peserta'] = self.env['ir.sequence'].next_by_code(
                'cdn.peserta'
            ) or 'New'
        return super().create(vals)

    def action_print_kartu_peserta(self):
        self.ensure_one()
        return self.env.ref(
            'ds_base_kursus.action_report_kartu_peserta'
        ).report_action(self)
    
    
    