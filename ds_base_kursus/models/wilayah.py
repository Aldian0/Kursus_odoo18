from odoo import models, fields, api, _


# ============================
#   PROPINSI
# ============================
class Propinsi(models.Model):
    _name = 'cdn.propinsi'
    _description = 'Referensi Provinsi'

    kode = fields.Char(string='Kode', required=True)
    name = fields.Char(string='Nama Provinsi', required=True)
    singkatan = fields.Char(string='Singkatan')
    deskripsi = fields.Text(string='Deskripsi')

    kota_ids = fields.One2many(
        'cdn.kota',
        'propinsi_id',
        string='Daftar Kota'
    )


# ============================
#   KOTA
# ============================
class Kota(models.Model):
    _name = 'cdn.kota'
    _description = 'Referensi Kota'

    name = fields.Char(string='Nama Kota', required=True)
    kode = fields.Char(string='Kode', required=True)
    singkatan = fields.Char(string='Singkatan')
    deskripsi = fields.Text(string='Deskripsi')

    propinsi_id = fields.Many2one(
        'cdn.propinsi',
        string='Provinsi'
    )

    kecamatan_ids = fields.One2many(
        'cdn.kecamatan',
        'kota_id',
        string='Daftar Kecamatan'
    )


# ============================
#   KECAMATAN
# ============================
class Kecamatan(models.Model):
    _name = 'cdn.kecamatan'
    _description = 'Referensi Kecamatan'

    name = fields.Char(string="Nama Kecamatan", required=True)
    kode = fields.Char(string='Kode')
    deskripsi = fields.Text(string="Deskripsi")

    propinsi_id = fields.Many2one('cdn.propinsi', string='Propinsi')
    kota_id = fields.Many2one('cdn.kota',string="Kota")
    desa_ids = fields.One2many('cdn.desa','kecamatan_id',string="Daftar Desa")


# ============================
#   DESA
# ============================
class Desa(models.Model):
    _name = "cdn.desa"
    _description = "Referensi Desa/Kelurahan"

    name = fields.Char(string="Nama Desa/Kelurahan", required=True)
    kode = fields.Char(string='Kode', required=True)
    deskripsi = fields.Text(string="Deskripsi")

    kecamatan_id = fields.Many2one("cdn.kecamatan",string="Kecamatan")
