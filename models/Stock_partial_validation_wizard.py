from odoo import models, fields

class StockPartialValidateWizard(models.TransientModel):
    _name = 'stock.partial.validate.wizard'

    picking_id = fields.Many2one('stock.picking', string='Albarán', required=True, ondelete='cascade')
    message = fields.Text(string='Mensaje', readonly=True)

    def action_confirm(self):
        self.picking_id.set_done(done=True)
        self.picking_id.button_validate()
        return {'type': 'ir.actions.act_window_close'}
    # def action_confirm(self):
    #     # Redirigir a la vista del albarán después de validar
    #     return {
    #         'name': 'Validación',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'stock.picking',
    #         'res_id': self.picking_id.id,
    #         'view_mode': 'form',
    #         'target': 'current',
    #     }

    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}