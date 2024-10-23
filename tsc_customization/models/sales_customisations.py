# -*- coding: utf-8 -*-
from openerp import models, fields, api

class sales_lines_customisations(models.Model):
    _inherit = 'sale.order.line'

    commission = fields.Monetary(string='Commission')
    fxrate=fields.Integer(string='Fx Rate', compute="_fx_rate_auto_append")
    commission_options = fields.Selection([('client', 'Client 2%'),
                                                   ('enterprise', 'Enterprise 3%')],
                                                  'Commission Option')

    def _fx_rate_auto_append(self):
        for rec in self:
            rec.fxrate= rec.order_id.fxrate

    @api.onchange('commission_options')
    def onchange_commission_option(self):
        """ONCHANGE OF COMMISSION CHANGE CALC MARGIN COMSSION """
        for rec in self:
            if rec.commission_options =='client 2%':
                rec.commission=2/100*rec.margin
            elif rec.commission_options=='enterprise 3%':
                rec.commission =23100*rec.margin
class sales_order_customisations(models.Model):
    _inherit = 'sale.order'

    fxrate=fields.Integer(string='Fx Rate')




