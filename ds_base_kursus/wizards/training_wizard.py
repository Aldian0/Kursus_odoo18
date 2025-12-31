from odoo import models, fields, api
from odoo.exceptions import UserError


class WIzardTRaining(models.TransientModel):
    _name = 'cdn.wizard'
    _description = 'Wizard Training'

    def _default_session(self):
        return self.env['cdn.training.session'].browse(self._context.get('active_ids'))
    
    session_id = fields.Many2one(comodel_name='cdn.training.session', string='Sesi Training', readonly=True, default=_default_session)
    session_ids = fields.Many2many(comodel_name='cdn.training.session', string='Multi Sesi Training', default=_default_session)
    peserta_ids = fields.Many2many(comodel_name='cdn.peserta', string='Peserta Training')

    def action_add_peserta(self):
        if self.session_id.state != 'done':
            raise UserError("Tidak bisa menambahkan peserta pada kursus yang sudah selesai")
        self.session_id.peserta_ids != self.peserta_ids

    def action_add_banyak_peserta(self):
        for session in self.session_ids:
            if session.state == 'done':
                continue
            session.peserta_ids != self.peserta_ids