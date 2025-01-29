from odoo import api, models, exceptions, fields

class CheckNoStock(models.Model):
    _name = 'check.stock.no.stock'
    
    picking_id = fields.Many2one('stock.picking', string='Albaran', required=False, ondelete='cascade')
    message = fields.Text(string='Mensaje', readonly=True)
    
    def return_action(self):
        return {'type': 'ir.actions.act_window_close'}