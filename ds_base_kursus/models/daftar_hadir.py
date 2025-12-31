from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DaftarHadir(models.Model):
    _name = 'cdn.daftar.hadir'
    _description = 'Daftar Hadir'
    _rec_name = 'tanggal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    tanggal = fields.Date(string="Tanggal",default=fields.Date.today, required=True, tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')],string="Status",default='draft', tracking=True)

    # RELATION_FIELDS
    peserta_id = fields.Many2one(comodel_name="cdn.peserta",string="Peserta")
    kursus_id = fields.Many2one("cdn.kursus",string="Kursus",required=True, tracking=True)
    session_id = fields.Many2one("cdn.training.session",string="Sesi",domain="[('kursus_id', '=', kursus_id)]",required=True, tracking=True)
    daftar_hadir_ids = fields.One2many(comodel_name="cdn.daftar_hadir_line",inverse_name="daftar_hadir_id",string="Detail Kehadiran", tracking=True)
    instruktur_id = fields.Many2one(comodel_name='cdn.instruktur', string='Instruktur', ondelete='cascade')
    no_hp = fields.Char(string="No HP Instruktur", related="instruktur_id.mobile", store=True, readonly=True)
    email = fields.Char(string="Email Instruktur", related="instruktur_id.email", store=True, readonly=True)
    jenis_kelamin = fields.Selection(string="Jenis Kelamin", related="instruktur_id.jenis_kelamin", store=True, readonly=True)
    no_peserta = fields.Char(string="No Peserta", related="peserta_id.no_peserta", store=True, readonly=True)
    pendaftaran_id = fields.Many2one('cdn.daftar.hadir', string='Pendaftaran')

    # RELATED_FIELDS 
    jml_peserta_hadir = fields.Integer(string="Jumlah Peserta Hadir",compute="_compute_peserta_hadir")
    harga_kursus_total = fields.Float(string="Total Harga", compute="_compute_harga_total",store=True)

    @api.onchange('kursus_id')
    def _onchange_kursus_id(self):
       if self.kursus_id:
           siswa_terdaftar = self.env['cdn.pendaftaran'].search([('kursus_id', '=', self.kursus_id.id),('state', '=', 'confirm')]).mapped('pendaftar_id')
           self.daftar_hadir_ids = [(5, 0, 0)]  # Hapus baris yang ada
           daftar_hadir_ids = []
           for siswa in siswa_terdaftar:
               daftar_hadir_ids.append((0, 0, {
                   'peserta_id': siswa.id,
                   'is_hadir': 'hadir',
               }))
           self.daftar_hadir_ids = daftar_hadir_ids

    
    @api.depends('kursus_id.harga_kursus', 'jml_peserta_hadir')
    def _compute_harga_total(self):
        for rec in self:
            rec.harga_kursus_total = (
                rec.kursus_id.harga_kursus * rec.jml_peserta_hadir
        )

    @api.depends('daftar_hadir_ids.is_hadir')
    def _compute_peserta_hadir(self):
        for record in self:
            record.jml_peserta_hadir = len(
                record.daftar_hadir_ids.filtered(
                    lambda x: x.is_hadir == 'hadir'
                )
            )

    def action_print_daftar_hadir(self):
        self.ensure_one()
        return self.env.ref(
            'ds_base_kursus.action_report_daftar_hadir'
        ).report_action(self)

    def action_confirm(self):
        for record in self:
            if not record.daftar_hadir_ids:
                raise ValidationError("Daftar hadir masih kosong!")
            record.state = 'confirm'

    def action_reset(self):
        for record in self:
            record.state = 'draft'



class DaftarHadirLine(models.Model):
    _name = "cdn.daftar_hadir_line"
    _description = "Detail Daftar Hadir"

    daftar_hadir_id = fields.Many2one("cdn.daftar.hadir",ondelete="cascade",required=True)
    peserta_id = fields.Many2one("cdn.peserta",string="Peserta")
    is_hadir = fields.Selection([('hadir', 'Hadir'), ('tidak_hadir', 'Tidak Hadir'), ('izin', 'Izin')],string="Hadir",default='hadir',required=True)
    jenis_kelamin = fields.Selection(string='Jenis Kelamin', related='peserta_id.jenis_kelamin')
    no_hp = fields.Char(string='No HP', related='peserta_id.mobile')