# # -*- coding: utf-8 -*-

# from odoo import models, api, exceptions

# class CheckStock(models.Model):
#     _inherit = 'sale.order'

#     @api.multi
#     def action_confirm(self):
#         errors = []
#         for order in self:
#             for line in order.order_line:
#                 product = line.product_id
#                 if product.type != 'product':
#                     continue

#                 if line.product_uom_qty > product.qty_available:
#                     errors.append(
#                         f"""No hay sufuciente stock para el producto:  {product.display_name}.
#                         Cantidad solicitada: {line.product_uom_qty}.
#                         Cantidad disponible: {product.qty_available}.""")
        
#         len_errors = len(errors)
#         if len_errors > 0:
#             text = ""
#             if len_errors > 1:
#                 text += "Ajusta la cantidad de los productos o espera a que hay mas stock. :)"
#             else:
#                 text += "Ajusta la cantidad del producto o espera a que hay mas stock. :)"

#             for text_line in errors:
#                 text += '\n\n' + text_line
            
#             raise exceptions.UserError(text)
        
#         return super(CheckStock, self).action_confirm()
                                