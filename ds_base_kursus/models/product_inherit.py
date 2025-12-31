from odoo import models, fields, api, _



class ProductTemplateInherit(models.Model):
   _inherit = 'product.template'


   is_kursus_product = fields.Boolean(string='Produk Kursus', default=False, help='Tandai jika produk ini terkait dengan kursus.')


   @api.model
   def create(self, vals):
       if vals.get('is_kursus_product'):
           vals['type'] = 'service'
       return super(ProductTemplateInherit, self).create(vals)