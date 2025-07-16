# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    applied_combo_ids = fields.Many2many(
        "product.combo",
        string="Applied Combos",
        help="Combos that have been applied to this order",
    )

    def _cart_update(
        self, product_id=None, line_id=None, add_qty=0, set_qty=0, **kwargs
    ):
        """Override to check and apply combo discounts after cart update"""
        try:
            result = super()._cart_update(
                product_id, line_id, add_qty, set_qty, **kwargs
            )
            self._apply_combo_discounts()
            return result
        except Exception as e:
            import logging
            _logger = logging.getLogger(__name__)
            _logger.error(f"Error in combo cart update: {e}")
            return super()._cart_update(product_id, line_id, add_qty, set_qty, **kwargs)

    def _apply_combo_discounts(self):
        """Check all active combos and apply discounts if cart matches"""
        self.ensure_one()
        if self.state != "draft" or not self.order_line:
            return
        try:
            existing_lines = self.order_line.filtered(lambda l: l.product_id)
            existing_lines.write({"discount": 0, "combo_applied": False})
            self.applied_combo_ids = [(5, 0, 0)]
            active_combos = self.env["product.combo"].search([("active", "=", True)])
            applied_combos = []
            for combo in active_combos:
                if self._check_and_apply_combo(combo):
                    applied_combos.append(combo.id)
            if applied_combos:
                self.applied_combo_ids = [(6, 0, applied_combos)]
        except Exception as e:
            import logging
            _logger = logging.getLogger(__name__)
            _logger.error(f"Error applying combo discounts: {e}")
            pass

    def _check_and_apply_combo(self, combo):
        """Check if combo can be applied and apply it"""
        self.ensure_one()
        available_lines = self.order_line.filtered(
            lambda l: not getattr(l, "combo_applied", False) and l.product_id
        )
        combo_products = {}
        for combo_line in combo.combo_line_ids:
            product_id = getattr(combo_line.product_id, "id", None)
            combo_products[product_id] = combo_products.get(product_id, 0) + combo_line.quantity
        order_products = {}
        for line in available_lines:
            if line.product_id:
                product_id = getattr(line.product_id, "id", None)
                order_products[product_id] = order_products.get(product_id, 0) + line.product_uom_qty
        if combo_products == order_products:
            discount = combo.get_discount_rate()
            for line in available_lines:
                line.write({"discount": discount, "combo_applied": True})
            return True
        return False
