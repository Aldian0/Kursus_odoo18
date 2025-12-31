# -*- coding: utf-8 -*-
# from odoo import http


# class DsBaseKursus(http.Controller):
#     @http.route('/ds_base_kursus/ds_base_kursus', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ds_base_kursus/ds_base_kursus/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ds_base_kursus.listing', {
#             'root': '/ds_base_kursus/ds_base_kursus',
#             'objects': http.request.env['ds_base_kursus.ds_base_kursus'].search([]),
#         })

#     @http.route('/ds_base_kursus/ds_base_kursus/objects/<model("ds_base_kursus.ds_base_kursus"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ds_base_kursus.object', {
#             'object': obj
#         })

