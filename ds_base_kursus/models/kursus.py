from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class Kursus(models.Model):
    _name = 'cdn.kursus'
    _description = 'Tabel Kursus'

    name = fields.Char(string='Nama Kursus', required=True)
    deskripsi = fields.Text(string='Keterangan')

    # RELATION_FIELDS
    user_id = fields.Many2one('res.users', string='Penanggung Jawab')
    session_line = fields.One2many(comodel_name='cdn.training.session', inverse_name='kursus_id', string='Daftar Sesi')

    # RELATED_FIELDS
    harga_kursus = fields.Float(string='Harga Kursus', related='produk_kursus_id.lst_price')
    biaya_konsumsi = fields.Float(string='Biaya Konsumsi', compute='_compute_biaya_konsumsi')
    produk_kursus_id = fields.Many2one('product.product', string='Produk Kursus', required=True, domain=[('is_kursus_product', '=', True)])
    produk_ids = fields.Many2many(comodel_name='product.product', string='Konsumsi')

    @api.depends('produk_ids')
    def _compute_biaya_konsumsi(self): 
        for record in self:
            record.biaya_konsumsi = sum(record.produk_ids.mapped('lst_price'))

class TrainingCourse(models.Model):
    _name = 'cdn.training.session'
    _description = 'Training Session'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Nama Sesi', required=True, tracking=True)
    kursus_id = fields.Many2one(comodel_name='cdn.kursus', string='Materi Kursus', required=True, ondelete='cascade', tracking=True)
    tgl_mulai = fields.Date(string='Tanggal Mulai', required=True, tracking=True)
    durasi = fields.Float(string='Durasi Kursus (Jam)', required=True, tracking=True)
    seats = fields.Integer(string='Tempat Duduk', compute='_compute_seats', tracking=True)
    no_hp = fields.Char(string='No Hp', related='instruktur_id.mobile')
    email = fields.Char(string='Email', related="instruktur_id.email")
    jenis_kelamin = fields.Selection(string='Jenis Kelamin', related="instruktur_id.jenis_kelamin")
    jml_peserta = fields.Integer(string='Jumlah Peserta')
    state = fields.Selection(string='Status', 
                             selection=[('draft', 'Draft'), 
                                        ('confirm', 'Sedang Berlangsung'),
                                        ('done', 'Selesai'),], default='draft', tracking=True)

    
    instruktur_id = fields.Many2one(comodel_name='cdn.instruktur', string='Instruktur', ondelete='cascade')
    peserta_ids = fields.Many2many(comodel_name='cdn.peserta', string='Peserta')
    

    @api.depends('peserta_ids')
    def _compute_seats(self):
        for record in self:
            record.seats= len(record.peserta_ids)

    def action_reset(self):
        for record in self:
            if record.state != 'done':
                record.state = 'draft'

    def action_reset_override(self):
        for record in self:
            record.state = 'draft'

    def action_confirm(self):
        for record in self:
            if not record.instruktur_id:
                raise ValidationError("Instruktur harus diisi sebelum konfirmasi!")
            if record.state != 'done':
                record.state = 'confirm'

    def action_done(self):
        for record in self:
            if record.state != 'draft':
                record.state = 'done'

        
    