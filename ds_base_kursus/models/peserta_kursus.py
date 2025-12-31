from odoo import models, fields, api

class PesertaKursus(models.Model):
    _name = 'cdn.peserta.kursus'
    _description = 'Data Peserta Kursus'

    name = fields.Char(string="Nama", required=True)
    no_peserta = fields.Char(string="No. Peserta", readonly=True, default='New')
    alamat = fields.Text(string="Alamat")
    no_hp = fields.Char(string="No. HP")
    jenis_kelamin = fields.Selection([
        ('laki', 'Laki-laki'),
        ('perempuan', 'Perempuan')
    ], string="Jenis Kelamin")
    image = fields.Binary(string="Foto")

    @api.model
    def create(self, vals):
        if vals.get('no_peserta', 'New') == 'New':
            vals['no_peserta'] = self.env['ir.sequence'].next_by_code(
                'cdn.peserta.kursus'
            ) or 'New'
        return super().create(vals)

    def action_print_peserta_kursus(self):
        self.ensure_one()
        return self.env.ref(
            'ds_base_kursus.action_report_peserta_kursus'
        ).report_action(self)