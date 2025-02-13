from odoo import models, api, exceptions, fields

class ButtonValidate(models.Model):
    _inherit = 'stock.move'
    
    make_order = fields.Boolean(string="Validar?", default=True)

class DeliveryOrderPartial(models.Model):
    _inherit = 'stock.picking'
    
    is_done = fields.Boolean(string='Validación completa', default=False)
    
    def set_done(self, done=False):
        self.is_done = done

    @api.multi
    def button_validate(self):
        self.ensure_one()

        # si ya esta valido
        if self.is_done:
            self.is_done = False
            return super(DeliveryOrderPartial, self).action_done()
        
        # variables
        ruta_MTO = self.env.ref('stock.route_warehouse0_mto', raise_if_not_found=False)
        productos_bajo_pedido = []
        productos_con_stock_parcial = []
        productos_sin_stock = []

        for move_line in self.move_lines:
            
            # si no se valida
            if not move_line.make_order:
                move_line.quantity_done = 0
                
            # Si se ingreso de forma manual
            elif move_line.quantity_done != 0:
                pass

            # si la cantidad disponible es mayo a la demanda
            elif move_line.product_id.qty_available >= move_line.product_uom_qty:
                move_line.quantity_done = move_line.product_uom_qty
            
            # si esta bajo pedido
            elif ruta_MTO and ruta_MTO.id in move_line.product_id.route_ids.ids:
                # si el producto (desde inventario) disponible es mayor que la demanda
                if move_line.product_id.qty_available > move_line.product_uom_qty:
                    move_line.quantity_done = move_line.product_uom_qty
                    productos_bajo_pedido.append(
                        f"""
                    Producto: {move_line.product_id.display_name}
                    Estado: Bajo pedido (Cantidad ajustada)
                    Cantidad solicitada: {move_line.product_uom_qty}
                    Cantidad disponible: {move_line.product_id.qty_available}""")
                # si el producto (desde inventario) disponible es menor o igual a la demenada y mayor que cero
                elif move_line.product_id.qty_available <= move_line.product_uom_qty and move_line.product_id.qty_available > 0:
                    move_line.quantity_done = move_line.product_id.qty_available
                    productos_bajo_pedido.append(
                        f"""
                    Producto: {move_line.product_id.display_name}
                    Estado: Bajo pedido (Cantidad ajustada)
                    Cantidad solicitada: {move_line.product_uom_qty}
                    Cantidad disponible: {move_line.product_id.qty_available}""")
                # si no hay producto disponible (desde inventario)
                else:
                    productos_sin_stock.append(
                        f"""
                    Producto: {move_line.product_id.display_name}
                    Estado: Bajo pedido (Sin stock)
                    Cantidad solicitada: {move_line.product_uom_qty}
                    Cantidad disponible: {move_line.product_id.qty_available}""")

            # si el producto (desde inventario) disponible no es mayor que la demanda pero si mayor a cero, se hace enmtrega parcial
            elif move_line.product_id.qty_available > 0:
                move_line.quantity_done = move_line.product_id.qty_available
                productos_con_stock_parcial.append(
                    f"""
                    Producto: {move_line.product_id.display_name}
                    Estado: Stock parcial (Cantidad ajustada)
                    Cantidad solicitada: {move_line.product_uom_qty}
                    Cantidad disponible: {move_line.product_id.qty_available}""")

            # si no hay stock disponible
            else:
                productos_sin_stock.append(
                    f"""
                    Producto: {move_line.product_id.display_name}
                    Estado: Sin stock (Eliminado de la entrega)
                    Cantidad solicitada: {move_line.product_uom_qty}
                    Cantidad disponible: {move_line.product_id.qty_available}""")
        
        # Vista de ninguna cantidad
        total_quantity_done = sum(self.move_lines.mapped('quantity_done'))
        if total_quantity_done == 0:
            return {
                'name': 'Sin cantidad procesada',
                'type': 'ir.actions.act_window',
                'res_model': 'check.stock.no.stock',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_picking_id': self.id,
                    'default_message': 'No se ha ingresado ninguna cantidad en los productos.',
                },
            }
        
        # vista de si ningun producto tiene stock
        if len(productos_sin_stock) == len(self.move_lines):
            mensaje = """
                    Productos sin stock:
                    """ + "\n".join(productos_sin_stock)
            return {
                'name': 'No hay stock para validar.',
                'type': 'ir.actions.act_window',
                'res_model': 'check.stock.no.stock',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_picking_id': self.id,
                    'default_message': mensaje,
                },
            }
        
        # vista de entregas parciales
        if productos_con_stock_parcial or productos_bajo_pedido:
            mensaje = """
                    Productos con cantidades ajustadas:
                    """
            mensaje += "\n".join(productos_con_stock_parcial + productos_bajo_pedido)
            return {
                'name': 'Productos con stock parcial',
                'type': 'ir.actions.act_window',
                'res_model': 'stock.partial.validate.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_picking_id': self.id,
                    'default_message': mensaje,
                },
            }
        
        return super(DeliveryOrderPartial, self).button_validate()