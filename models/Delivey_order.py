from odoo import models, api, exceptions, fields

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
            # Si no se ingreso de forma manual
            if move_line.quantity_done != 0:
                continue

            # si la cantidad disponible es mayo a la demanda
            if move_line.product_id.qty_available >= move_line.product_uom_qty:
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
                    Cantidad disponible: {move_line.product_id.qty_available}
                    Cantidad entregada: {move_line.quantity_done}""")
                # si el producto (desde inventario) disponible es menor o igual a la demenada y mayor que cero
                elif move_line.product_id.qty_available <= move_line.product_uom_qty and move_line.product_id.qty_available > 0:
                    move_line.quantity_done = move_line.product_id.qty_available
                    productos_bajo_pedido.append(
                        f"""
                    Producto: {move_line.product_id.display_name}
                    Estado: Bajo pedido (Cantidad ajustada)
                    Cantidad solicitada: {move_line.product_uom_qty}
                    Cantidad disponible: {move_line.product_id.qty_available}
                    Cantidad entregada: {move_line.quantity_done}""")
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
                    Cantidad disponible: {move_line.product_id.qty_available}
                    Cantidad entregada: {move_line.quantity_done}""")

            # si no hay stock disponible
            else:
                productos_sin_stock.append(
                    f"""
                    Producto: {move_line.product_id.display_name}
                    Estado: Sin stock (Eliminado de la entrega)
                    Cantidad solicitada: {move_line.product_uom_qty}
                    Cantidad disponible: {move_line.product_id.qty_available}""")
        
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