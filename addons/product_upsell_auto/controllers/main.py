# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleUpsell(WebsiteSale):
    def debug_upsell_data(self, product):
        """Log and return all upsell recommendation data for a product for deep debugging"""
        import logging

        _logger = logging.getLogger(__name__)
        data = {
            "product_id": product.id,
            "product_name": product.name,
            "recommendations": [],
        }
        for rec in product.auto_upsell_recommendation_ids:
            rec_data = {
                "rec_id": rec.id,
                "recommended_product_id": rec.recommended_product_id.id,
                "recommended_product_name": rec.recommended_product_id.name,
                "active": rec.active,
                "type": rec.type,
                "website_published": rec.recommended_product_id.website_published,
                "sale_ok": rec.recommended_product_id.sale_ok,
                "product_active": rec.recommended_product_id.active,
                "score": rec.score,
            }
            data["recommendations"].append(rec_data)
            _logger.warning(f"[DEBUG] Upsell Rec: {rec_data}")
        _logger.warning(f"[DEBUG] All upsell data: {data}")
        return data

    def product(self, product, category="", search="", **kwargs):
        result = super().product(product, category, search, **kwargs)
        # Debug: kiểm tra product và context trả về
        import logging

        _logger = logging.getLogger(__name__)
        _logger.warning(f"[DEBUG] Controller product: {product}")
        _logger.warning(f"[DEBUG] Controller result type: {type(result)}")
        if isinstance(result, dict):
            _logger.warning(f"[DEBUG] Controller context keys: {list(result.keys())}")
            result["upsell_products"] = product.get_upsell_recommendations()
            _logger.warning(
                f"[DEBUG] Controller upsell_products: {result['upsell_products']}"
            )
        return result

    @http.route(
        ["/shop/product/upsell/<int:product_id>"],
        type="json",
        auth="public",
        website=True,
    )
    def get_product_upsell(self, product_id, limit=4, **kwargs):
        """JSON endpoint to get upsell recommendations"""
        try:
            product = request.env["product.template"].sudo().browse(product_id)
            if not product.exists():
                return {"success": False, "message": "Product not found"}

            upsell_products = product.get_upsell_recommendations(limit=limit)

            products_data = []
            for upsell_product in upsell_products:
                products_data.append(
                    {
                        "id": upsell_product.id,
                        "name": upsell_product.name,
                        "price": upsell_product.list_price,
                        "currency": request.env.company.currency_id.symbol,
                        "image_url": f"/web/image/product.template/{upsell_product.id}/image_1920",
                        "url": f"/shop/product/{upsell_product.id}",
                        "description_sale": upsell_product.description_sale or "",
                    }
                )

            return {
                "success": True,
                "products": products_data,
                "count": len(products_data),
            }

        except Exception as e:
            return {"success": False, "message": str(e)}

    @http.route(
        ["/shop/generate_upsell"],
        type="http",
        auth="user",
        website=True,
        methods=["POST"],
    )
    def generate_upsell_recommendations(self, **kwargs):
        """Manual trigger to generate upsell recommendations (admin only)"""
        if not request.env.user.has_group("sales_team.group_sale_manager"):
            return request.redirect("/shop")

        try:
            # Trigger upsell generation
            request.env["product.template"].sudo().action_generate_all_upsell()

            return request.redirect(
                "/web#action=product_upsell_auto.action_product_recommendation"
            )

        except Exception as e:
            # Log error and redirect
            import logging

            _logger = logging.getLogger(__name__)
            _logger.error(f"Error generating upsell recommendations: {e}")
            return request.redirect("/shop")
