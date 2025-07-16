# Website Sale Product Promotions

Module này hợp nhất toàn bộ tính năng của:

- `website_product_promotions`: Combo sản phẩm, upsell/cross-sell thủ công, khuyến mãi website
- `product_upsell_auto`: Gợi ý upsell/cross-sell tự động, combo thông minh, recommendation

## Tính năng nổi bật

- Tạo combo sản phẩm với giá ưu đãi, tự động áp dụng khi khách mua đủ combo
- Gợi ý upsell/cross-sell thủ công và tự động dựa trên dữ liệu
- Giao diện đẹp cho website, backend quản lý dễ dàng
- Cron tự động cập nhật recommendation
- Tăng giá trị đơn hàng trung bình, trải nghiệm khách hàng tốt hơn

## Cấu trúc thư mục

- models/: Toàn bộ models về combo, recommendation, product extension, sale order
- controllers/: Controller xử lý combo, recommendation, API website
- views/: Giao diện backend, frontend, website, assets
- security/: Phân quyền truy cập
- static/: CSS, JS cho website
- data/: Cron jobs, dữ liệu mẫu

## Tác giả

Beemart

## License

LGPL-3
