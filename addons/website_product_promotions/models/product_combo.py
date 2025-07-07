# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductCombo(models.Model):
    _name = "product.combo"
    _description = "Product Combo"
    _order = "name"

    name = fields.Char(string="Combo Name", required=True, translate=True)

    active = fields.Boolean(string="Active", default=True)

    price_total = fields.Float(
        string="Combo Price", required=True, help="Special price for this combo"
    )

    combo_line_ids = fields.One2many(
        "product.combo.line", "combo_id", string="Combo Products", required=True
    )

    original_price = fields.Float(
        string="Original Total Price", compute="_compute_original_price", store=True
    )

    discount_amount = fields.Float(
        string="Discount Amount", compute="_compute_discount_amount", store=True
    )

    discount_percentage = fields.Float(
        string="Discount %", compute="_compute_discount_amount", store=True
    )

    image = fields.Image(
        string="Combo Image", help="Image for combo display on website"
    )

    description = fields.Html(string="Description", translate=True)

    website_published = fields.Boolean(string="Published on Website", default=True)

    @api.depends("combo_line_ids.product_id.lst_price", "combo_line_ids.quantity")
    def _compute_original_price(self):
        for combo in self:
            total = 0.0
            for line in combo.combo_line_ids:
                if line.product_id:
                    total += line.product_id.lst_price * line.quantity
            combo.original_price = total

    @api.depends("original_price", "price_total")
    def _compute_discount_amount(self):
        for combo in self:
            if combo.original_price > 0:
                combo.discount_amount = combo.original_price - combo.price_total
                combo.discount_percentage = (
                    combo.discount_amount / combo.original_price
                ) * 100
            else:
                combo.discount_amount = 0.0
                combo.discount_percentage = 0.0

    @api.constrains("price_total", "original_price")
    def _check_combo_price(self):
        for combo in self:
            if combo.price_total < 0:
                raise ValidationError(_("Combo price cannot be negative."))
            if combo.original_price > 0 and combo.price_total > combo.original_price:
                raise ValidationError(
                    _("Combo price should be less than or equal to original price.")
                )

    @api.constrains("combo_line_ids")
    def _check_combo_lines(self):
        for combo in self:
            if len(combo.combo_line_ids) < 2:
                raise ValidationError(_("A combo must have at least 2 products."))

    def get_discount_rate(self):
        """Return discount rate for applying to sale order lines"""
        self.ensure_one()
        if self.original_price > 0:
            return (1 - self.price_total / self.original_price) * 100
        return 0.0

    def check_combo_match(self, order_lines):
        """Check if order lines match this combo exactly"""
        self.ensure_one()

        combo_products = {}
        for line in self.combo_line_ids:
            product_id = line.product_id.id
            combo_products[product_id] = (
                combo_products.get(product_id, 0) + line.quantity
            )

        order_products = {}
        for line in order_lines:
            if line.product_id:
                product_id = line.product_id.id
                order_products[product_id] = (
                    order_products.get(product_id, 0) + line.product_uom_qty
                )

        return combo_products == order_products


class ProductComboLine(models.Model):
    _name = "product.combo.line"
    _description = "Product Combo Line"
    _order = "combo_id, sequence, id"

    combo_id = fields.Many2one(
        "product.combo", string="Combo", required=True, ondelete="cascade"
    )

    sequence = fields.Integer(string="Sequence", default=10)

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
        domain=[("sale_ok", "=", True)],
    )

    quantity = fields.Float(string="Quantity", required=True, default=1.0)

    price_unit = fields.Float(
        string="Unit Price", related="product_id.lst_price", readonly=True
    )

    subtotal = fields.Float(string="Subtotal", compute="_compute_subtotal", store=True)

    @api.depends("product_id.lst_price", "quantity")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.price_unit * line.quantity

    @api.constrains("quantity")
    def _check_quantity(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError(_("Quantity must be greater than 0."))
