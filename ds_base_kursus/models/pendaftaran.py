from odoo import models, fields, api
from odoo.exceptions import UserError


class Pendaftaran(models.Model):
    _name = 'cdn.pendaftaran'
    _description = 'Tabel Pendaftaran'

    name = fields.Char(string='No Pendaftaran', readonly=True, copy=True, default='New')
    tanggal = fields.Date(string='Tanggal', default=lambda self: fields.Date.today(), required=True)
    state = fields.Selection(string='Status', selection=[('draft', 'Draft'), ('confirm', 'Konfirmasi'),], default='draft')

    # RELATION_FIELDS
    pendaftar_id = fields.Many2one(comodel_name='cdn.peserta', string='Peserta Kursus', required=True)
    kursus_id = fields.Many2one(comodel_name='cdn.kursus', string='Kursus', required=True)
    invoice_id = fields.Many2one('account.move', string='No.Tagihan')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    

    # RELATED_FIELDS
    jenis_kelamin = fields.Selection(string='Jenis Kelamin', related='pendaftar_id.jenis_kelamin', store=True)
    no_hp = fields.Char(string='No HP', related='pendaftar_id.mobile', store=True)
    harga_kursus = fields.Float(string='Harga Kursus', related='kursus_id.harga_kursus', store=True)
    status_pembayaran = fields.Selection(string='Status Pembayaran', related='invoice_id.status_in_payment', store=True)
    # status_pembayaran = fields.Selection(string='Status Pembayaran', selection=[('unpaid', 'Belum Lunas'), ('paid', 'Lunas'),], default='unpaid')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('pendaftaran.sequence')
        return super(Pendaftaran, self).create(vals)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'cdn.pendaftaran'
            ) or 'New'
        return super().create(vals)

    def action_print_bukti_pendaftaran(self):
        self.ensure_one()
        return self.env.ref(
            'ds_base_kursus.action_report_bukti_pendaftaran'
        ).report_action(self)

    def action_confirm(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'confirm'

    def action_reset(self):
        for rec in self:
            if rec.invoice_id:
                raise UserError(
                    'Tidak bisa reset karena masih ada invoice. '
                    'Silakan reset tagihan terlebih dahulu.'
                )
            rec.write({
                'state': 'draft',
                })

    def action_create_invoice(self):
        Invoice = self.env['account.move']
        for rec in self:
            Invoice = self.env['account.move'].create({
                'partner_id': rec.pendaftar_id.partner_id.id,
                'move_type': 'out_invoice',
                'invoice_date': rec.tanggal,
                'invoice_line_ids': [(0, 0, {
                    'name': rec.kursus_id.name,
                    'product_id': rec.kursus_id.produk_kursus_id.id,
                    'quantity': 1,
                    'price_unit': rec.harga_kursus,
                })], 
            })
            rec.invoice_id = Invoice.id
            Invoice.action_post()
    
    def action_reset_invoice(self):
        for rec in self:
            if not rec.invoice_id:
                raise UserError('Belum ada invoice untuk di-reset.')

            # Jika invoice sudah posted → cancel dulu
            if rec.invoice_id.state == 'posted':
                rec.invoice_id.button_cancel()

            rec.invoice_id.unlink()
            rec.invoice_id = False


    # def actiion_reset_invoice(self):
    #     for record in self:
    #         if record.invoice_id:
    #             record.invoice_id.button_draft()
    #             record.invoice_id.unlink()
    #             record.invoice_id = False