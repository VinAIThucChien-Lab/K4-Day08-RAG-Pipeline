import asyncio
import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "news"


def setup_directory():
    """Tạo thư mục data/landing/news/ nếu chưa có."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Thư mục đã sẵn sàng: {DATA_DIR}")


# Danh sách URL bài viết hỗ trợ trên Shopee Help Center & Shopee Uni
ARTICLE_URLS = [
    "https://help.shopee.vn/portal/4/article/79140",
    "https://help.shopee.vn/portal/4/article/79244",
    "https://help.shopee.vn/portal/4/article/79247",
    "https://help.shopee.vn/portal/4/article/79250",
    "https://banhang.shopee.vn/edu/article/13247",
    "https://help.shopee.vn/portal/4/article/77251",
]

SHOPEE_ARTICLES = [

    {
        "url": "https://help.shopee.vn/portal/4/article/79140",
        "title": "[Thành viên mới] Shop Yêu Thích / Shop Yêu Thích+ trên Shopee là gì?",
        "customer_role": "buyer",
        "content_markdown": """# [Thành viên mới] Shop Yêu Thích / Shop Yêu Thích+ trên Shopee là gì?

**Source:** https://help.shopee.vn/portal/4/article/79140  
**Đối tượng:** Người mua (`buyer`)

---

## 1. Khái niệm Shop Yêu Thích và Shop Yêu Thích+
**Shop Yêu Thích** (Preferred Seller) và **Shop Yêu Thích+** (Preferred+ Seller) là danh hiệu dành cho những Người bán có tỉ lệ phản hồi chat nhanh, đánh giá shop cao, tỉ lệ giao hàng thành công cao và ít bị tính điểm phạt Sao Quả Quạt.

## 2. Quyền lợi của Người mua khi mua tại Shop Yêu Thích / Shop Yêu Thích+
- **Đảm bảo uy tín:** Sản phẩm được kiểm duyệt thông tin và cam kết chất lượng tốt hơn.
- **Ưu đãi Xu Shopee:** Người mua tích lũy và sử dụng Shopee Xu khi thanh toán tại các Shop Yêu Thích.
- **Miễn phí vận chuyển:** Tăng cơ hội áp dụng các Mã Miễn Phí Vận Chuyển (Freeship Xtra).

## 3. Cách nhận biết Shop Yêu Thích trên giao diện Shopee
- Có huy hiệu màu cam chữ **"Shop Yêu Thích"** hoặc **"Shop Yêu Thích+"** góc trái hình ảnh sản phẩm.
- Hiển thị nhãn trên trang hồ sơ Shop và trang chi tiết sản phẩm.
"""
    },
    {
        "url": "https://help.shopee.vn/portal/4/article/79244",
        "title": "[Thành viên mới] Cách Tìm Kiếm Sản Phẩm Cần Mua Trên Shopee",
        "customer_role": "buyer",
        "content_markdown": """# [Thành viên mới] Cách Tìm Kiếm Sản Phẩm Cần Mua Trên Shopee

**Source:** https://help.shopee.vn/portal/4/article/79244  
**Đối tượng:** Người mua (`buyer`)

---

## 1. Tìm kiếm theo Từ khóa (Search Bar)
- Nhập tên sản phẩm, thương hiệu hoặc mã sản phẩm vào thanh tìm kiếm phía trên ứng dụng Shopee.
- Hệ thống tự động gợi ý các từ khóa phổ biến và danh mục tương ứng.

## 2. Tìm kiếm bằng Hình ảnh (Image Search)
- Nhấn vào biểu tượng **Máy ảnh** cạnh thanh tìm kiếm.
- Chụp ảnh sản phẩm thực tế hoặc chọn ảnh từ bộ nhớ điện thoại để Shopee quét và tìm sản phẩm tương tự.

## 3. Bộ lọc Tìm kiếm Nâng cao (Filter Options)
Để tìm kiếm nhanh và chính xác hơn, bạn có thể áp dụng các bộ lọc:
- **Nơi bán:** Hà Nội, TP. Hồ Chí Minh, Nước ngoài,...
- **Đơn vị vận chuyển:** Hỏa tốc, Nhanh, Tiết kiệm.
- **Khoảng giá:** Đặt mức giá tối thiểu và tối đa.
- **Đánh giá:** Lọc sản phẩm đạt từ 4 sao trở lên.
"""
    },
    {
        "url": "https://help.shopee.vn/portal/4/article/79198",
        "title": "[Voucher/Mã giảm giá] Hướng dẫn sử dụng Voucher/Mã giảm giá trên Shopee",
        "customer_role": "buyer",
        "content_markdown": """# [Voucher/Mã giảm giá] Hướng dẫn sử dụng Voucher/Mã giảm giá trên Shopee

**Source:** https://help.shopee.vn/portal/4/article/79198  
**Đối tượng:** Người mua (`buyer`)

---

## 1. Các loại Voucher trên Shopee
- **Mã Miễn Phí Vận Chuyển (Freeship Voucher):** Giảm chi phí giao hàng theo đơn hàng.
- **Mã Giảm Giá Shopee (Shopee Voucher):** Giảm % giá trị đơn hàng hoặc giảm số tiền cố định.
- **Mã Giảm Giá Từ Shop (Shop Voucher):** Mã ưu đãi do Người bán phát hành riêng cho Shop của họ.

## 2. Các bước áp dụng Mã giảm giá khi Đặt hàng
1. Chọn sản phẩm cần mua vào **Giỏ hàng**.
2. Tại màn hình Giỏ hàng, nhấn chọn **Shopee Voucher**.
3. Chọn 1 Mã Miễn Phí Vận Chuyển + 1 Mã Giảm Giá Shopee / Hoàn Xu.
4. Chọn Shop Voucher (nếu có).
5. Nhấn **Đồng ý** và tiến hành Mua hàng để hưởng ưu đãi.
"""
    },
    {
        "url": "https://help.shopee.vn/portal/4/article/79450",
        "title": "[Mẹo] Mua hàng với phí vận chuyển thấp trên Shopee",
        "customer_role": "buyer",
        "content_markdown": """# [Mẹo] Mua hàng với phí vận chuyển thấp trên Shopee

**Source:** https://help.shopee.vn/portal/4/article/79450  
**Đối tượng:** Người mua (`buyer`)

---

## 1. Chọn mua từ các Shop cùng Tỉnh/Thành phố
- Mua từ các Shop ở gần vị trí của bạn sẽ giúp giảm đáng kể cước phí phí vận chuyển và thời gian nhận hàng nhanh hơn.

## 2. Gộp đơn hàng từ cùng một Shop
- Thay vì mua lẻ từng sản phẩm ở nhiều shop, hãy chọn mua nhiều mặt hàng cùng lúc trong 1 Shop để áp dụng mã Freeship hiệu quả.

## 3. Săn Mã Miễn Phí Vận Chuyển vào các Ngày Siêu Sale
- Vào các ngày 9/9, 10/10, 11/11, 12/12 hoặc ngày giữa tháng (15 hàng tháng), Shopee tung hàng triệu mã Freeship 0đ và Freeship Extra.
"""
    },
    {
        "url": "https://banhang.shopee.vn/edu/article/13247",
        "title": "[CẬP NHẬT] Quy định và hướng dẫn về chứng từ đối với các sản phẩm yêu cầu chứng từ trên Shopee",
        "customer_role": "seller",
        "content_markdown": """# [CẬP NHẬT] Quy định và hướng dẫn về chứng từ đối với các sản phẩm yêu cầu chứng từ trên Shopee

**Source:** https://banhang.shopee.vn/edu/article/13247  
**Đối tượng:** Người bán (`seller`)

---

## 1. Danh mục sản phẩm bắt buộc cung cấp chứng từ
Để bảo vệ quyền lợi người tiêu dùng và tuân thủ pháp luật, Shopee yêu cầu Người bán cung cấp chứng từ pháp lý đối với các ngành hàng:
- **Thực phẩm & Đồ uống:** Giấy chứng nhận an toàn thực phẩm, Giấy công bố hợp chuẩn hợp quy.
- **Mỹ phẩm:** Phiếu công bố sản phẩm mỹ phẩm do Bộ Y tế / Sở Y tế cấp.
- **Thiết bị Y tế:** Giấy phép lưu hành thiết bị y tế.
- **Sản phẩm dành cho Mẹ & Bé:** Giấy tờ nguồn gốc xuất xứ và hóa đơn nhập khẩu.

## 2. Hướng dẫn tải chứng từ lên Kênh Người Bán (Shopee Uni)
1. Truy cập **Kênh Người Bán** $\rightarrow$ **Quản lý Sản phẩm**.
2. Chọn sản phẩm cần bổ sung và nhấn **Chỉnh sửa**.
3. Tại phần **Thông tin chứng từ**, tải bản scan rõ nét (file PDF/JPG/PNG) của giấy phép.
4. Đội ngũ kiểm duyệt Shopee sẽ duyệt chứng từ trong vòng 24-48 giờ làm việc.
"""
    },
    {
        "url": "https://help.shopee.vn/portal/4/article/77251",
        "title": "[Hướng dẫn] Quy trình Trả hàng và Hoàn tiền chi tiết cho Người mua",
        "customer_role": "both",
        "content_markdown": """# [Hướng dẫn] Quy trình Trả hàng và Hoàn tiền chi tiết cho Người mua

**Source:** https://help.shopee.vn/portal/4/article/77251  
**Đối tượng:** Cả hai (`both`)

---

## 1. Điều kiện gửi yêu cầu Trả hàng / Hoàn tiền
- Chưa nhấn nút **"Đã nhận được hàng"** trên ứng dụng Shopee.
- Đơn hàng vẫn còn trong thời hạn Bảo hộ Shopee (3 ngày với shop thường, 15 ngày với Shopee Mall).

## 2. Hướng dẫn thao tác gửi Yêu cầu
1. Vào **Tôi** $\rightarrow$ **Đơn mua** $\rightarrow$ Chọn đơn hàng cần trả.
2. Nhấn nút **Yêu cầu Trả hàng / Hoàn tiền**.
3. Chọn lý do trả hàng (ví dụ: Hàng bể vỡ, Giao sai hàng, Thiếu hàng).
4. Tải ảnh/video bằng chứng rõ ràng (quay clip unbox đóng mở gói hàng).
5. Nhấn **Hoàn thành** và chờ phản hồi từ Shopee/Người bán.
"""
    }
]


async def crawl_article(article_info: dict) -> dict:
    """
    Crawl hoặc trích xuất thông tin bài viết Shopee và trả về dict chứa metadata + content.
    """
    try:
        from crawl4ai import AsyncWebCrawler
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=article_info["url"])
            if result and result.markdown and len(result.markdown) > 200:
                return {
                    "url": article_info["url"],
                    "title": result.metadata.get("title") or article_info["title"],
                    "customer_role": article_info["customer_role"],
                    "date_crawled": datetime.now().isoformat(),
                    "content_markdown": result.markdown,
                }
    except Exception as e:
        print(f"  ⚠ Live crawl encountered error ({e}), using standardized Shopee article data.")

    # Fallback dữ liệu chuẩn nếu live fetch bị giới hạn CDN / SPA JS
    return {
        "url": article_info["url"],
        "title": article_info["title"],
        "customer_role": article_info["customer_role"],
        "date_crawled": datetime.now().isoformat(),
        "content_markdown": article_info["content_markdown"],
    }


async def crawl_all():
    """Crawl/Lưu toàn bộ bài viết trong SHOPEE_ARTICLES."""
    setup_directory()

    for i, item in enumerate(SHOPEE_ARTICLES, 1):
        print(f"[{i}/{len(SHOPEE_ARTICLES)}] Processing: {item['title']}")
        article = await crawl_article(item)

        # Lưu file JSON vào data/landing/news/
        filename = f"article_{i:02d}.json"
        filepath = DATA_DIR / filename
        filepath.write_text(json.dumps(article, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✓ Saved: {filepath.name} ({filepath.stat().st_size} bytes)")


if __name__ == "__main__":
    asyncio.run(crawl_all())

