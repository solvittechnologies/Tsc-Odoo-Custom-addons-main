# -*- coding: utf-8 -*-
from openerp import models, fields, api

class sales_lines_customisations(models.Model):
    _inherit = 'res.partner'

    supplier_invoice_count=fields.Integer(string="Invoice Count")

    @api.multi
    def _purchase_inedvoice_count(self):
        Invoice = self.env['account.invoice']
        for partner in self:
            print("log",partner.save_supplier_invoice_count)
            partner.save_supplier_invoice_count=Invoice.search_count(
                 [('partner_id', 'child_of', partner.id), ('type', '=', 'in_invoice')])


class purchase_order_customisations(models.Model):
    _inherit = 'purchase.order'

    purchase_request=fields.Many2one('purchase.request', string="Purchase Request Id")

    @api.onchange('purchase_request')
    def _onchange_purchase_request(self):
        if self.purchase_request:
            # Clear existing order lines before adding new ones
            self.order_line = [(5, 0, 0)]
            if self.purchase_request.sale_order_id:
                for request_line in self.purchase_request.sale_order_id.order_line:
                    # Create a new purchase order line using data from the request line
                    order_line = self.env['purchase.order.line'].new({
                        'product_id': request_line.product_id.id,
                        'name': request_line.name,
                        'product_qty': request_line.product_uom_qty,
                        'product_uom': request_line.product_uom.id,
                        'price_unit': request_line.price_unit,
                        'price_subtotal': request_line.price_subtotal,
                        'taxes_id': [(6, 0, request_line.tax_id.ids)],
                    })
                    self.order_line += order_line
            else:
                for request_line in self.purchase_request.line_ids:
                    # Create a new purchase order line using data from the request line
                    order_line = self.env['purchase.order.line'].new({
                        'product_id': request_line.product_id.id,
                        'name': request_line.name,
                        'product_qty': request_line.product_qty,
                        'product_uom': request_line.product_uom_id.id,
                    })
                    self.order_line += order_line



    # You may need to add additional logic for validation, etc.

    # You may need to add additional logic for validation, etc.