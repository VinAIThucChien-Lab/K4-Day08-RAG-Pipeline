from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"


def setup_directory():
    """Tạo thư mục data/landing/legal/ nếu chưa có."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Thư mục đã sẵn sàng: {DATA_DIR}")


LEGAL_DOCS = [
    {
        "filename": "returns-refund-policy-shopee.pdf",
        "title": "Shopee Returns and Refund Policy",
        "customer_role": "both",
        "content": """1. Dieu kien tra hang va hoan tien
Nguoi mua co the yeu cau Tra hang va Hoan tien trong cac truong hop sau:
- San pham bi loi hoac bi hu hach trong qua trinh van chuyen.
- San pham giao sai (sai kich thuoc, sai mau sac, sai san pham).
- San pham khac bien dang so voi mo ta cua Nguoi ban.
- Nguoi ban giao thieu hang hoac thieu phu kien di kem.

2. Thoi gian yeu cau Tra hang / Hoan tien
- Doi voi Shopee Mall: Nguoi mua co 15 ngay ke tu khi nhan hang de gui yeu cau.
- Doi voi Shop Thuong (Non-Mall): Nguoi mua co 3 ngay ke tu khi don hang cap nhat trang thai Da giao hang.

3. Quy trinh xu ly Hoan tien
- Nguoi ban co 48 gio de phan hoi yeu cau tra hang cua Nguoi mua.
- Neu Nguoi ban dong y hoac khong phan hoi trong 48h, Shopee se cap ma tra hang mien phi.
- Tien hoan se duoc chuyen ve Vi ShopeePay hoac Tai khoan ngan hang cua Nguoi mua trong 3-5 ngay lam viec sau khi kiem hang thanh cong.
"""
    },
    {
        "filename": "payment-methods-shopee.pdf",
        "title": "Shopee Payment Methods Regulations",
        "customer_role": "buyer",
        "content": """1. Cac phuong thuc thanh toan hop le tren Shopee
Shopee ho tro nhieu phuong thuc thanh toan an toan va tien loi:
- Thanh toan khi nhan hang (COD - Cash on Delivery).
- Vi dien tu ShopeePay (lien ket ngan hang, thanh toan tuc thi).
- The Tin dung / The Ghi no (Visa, Mastercard, JCB).
- Chuyen khoan ngan hang va SPayLater (Mua truoc tra sau).

2. Quy dinh va han muc thanh toan COD
- Phuong thuc COD chi ap dung cho cac don hang co gia tri duoi 20.000.000 VNĐ.
- Nguoi mua duoc phep kiem tra ngoai quan kien hang (Kiem hang) theo quy dinh Shopee Dong Kiem.

3. Bao mat thanh toan va Hoan tien
- Tat ca giao dich qua Shopee deu duoc bao ve boi Shopee Dam Bao (Shopee Guarantee).
- Tien thanh toan cua Nguoi mua se duoc Shopee giu lai va chi chuyen cho Nguoi ban sau khi Nguoi mua xac nhan Da nhan duoc hang va khong co khieu nai.
"""
    },
    {
        "filename": "privacy-policy-shopee.pdf",
        "title": "Shopee Privacy and Data Protection Policy",
        "customer_role": "both",
        "content": """1. Thu nhap va su dung thong tin ca nhan
Shopee thu nhap thong tin ca nhan cua Nguoi dung (Nguoi mua va Nguoi ban) bao gom:
- Ho va ten, so dien thoai, dia chi giao hang, dia chi email.
- Thong tin tai khoan ngan hang va giao dich thanh toan.
- Du lieu thiet bi va nhat ky truy cap ung dung.

2. Muc dich su dung thong tin
- Xu ly don hang, giao hang va hoan tien.
- Xac thuc danh tinh va ngan chan cac hanh vi gian luan.
- Cung cap dich vu ho tro khach hang va gui thong bao uu dai.

3. Cam ket bao mat du lieu
- Shopee cam ket khong chia se hay ban thong tin ca nhan cho ben thu ba khi chua duoc su dong y cua Nguoi dung.
- Tat ca du lieu duoc ma hoa theo chuan an ninh SSL/TLS va luu truc an toan.
"""
    },
    {
        "filename": "product-listing-regulations-shopee.pdf",
        "title": "Shopee Seller Product Listing and Compliance Regulations",
        "customer_role": "seller",
        "content": """1. Quy dinh ve dang ban san pham
Nguoi ban phai tuan thu cac quy dinh sau khi dang ban san pham tren Shopee:
- Ten san pham phai ro rang, chinh xac, khong chua tu khoa spam hoac thuong hieu khac.
- Hinh anh san pham phai la hinh anh thuc te, dung kich thuoc va chat luong cao.
- Gia ban va so luong ton kho phai duoc cap nhat chinh xac.

2. Quy dinh ve chung tu va giay phep cho nganh hang co dieu kien
Doi voi cac san pham thuoc nganh hang kinh doanh co dieu kien (Thuc pham, My pham, Thiet bi y te, San pham me va be):
- Nguoi ban phai cung cap Giay phep kinh doanh, Giay xac nhan cong bo san pham, hoac Chung nhan an toan thuc pham.
- Nguoi ban tai ban scan mau giay to goc len he thong Shopee Uni / Ban Hang de duoc phieu duyet truoc khi hien thi san pham.

3. Hinh thuc xu ly vi pham
- San pham vi pham se bi khoa, xoa hoac tinh diem phat Sao Qua Quat (Penalty).
- Tai khoan Nguoi ban co the bi tam khoa hoac khoa vinh vien neu vi pham nhieu lan.
"""
    }
]


def create_pdf_fallback(filepath: Path, title: str, customer_role: str, content: str):
    """Tạo file PDF 1.4 chuẩn bằng Pure Python không cần thư viện ngoài."""
    lines = [f"Title: {title}", f"Customer Role: {customer_role}", ""]
    for para in content.strip().split("\n\n"):
        lines.extend(para.split("\n"))
        lines.append("")

    stream_text = []
    y = 750
    for line in lines:
        if y < 50:
            break
        escaped = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream_text.append(f"1 0 0 1 50 {y} Tm ({escaped}) Tj")
        y -= 14

    stream_content = "BT /F1 10 Tf\n" + "\n".join(stream_text) + "\nET\n"
    stream_bytes = stream_content.encode("latin1", errors="replace")

    pdf_parts = [
        b"%PDF-1.4\n",
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n",
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n",
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj\n",
        b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n",
        f"5 0 obj << /Length {len(stream_bytes)} >>\nstream\n".encode("latin1"),
        stream_bytes,
        b"endstream\nendobj\n",
    ]

    body = b"".join(pdf_parts)
    xref_offset = len(body)
    trailer = f"""xref
0 6
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000244 00000 n 
0000000315 00000 n 
trailer << /Size 6 /Root 1 0 R >>
startxref
{xref_offset}
%%EOF
"""
    filepath.write_bytes(body + trailer.encode("latin1"))


def create_legal_pdfs():
    """Tạo 4 file PDF chính sách pháp luật TMĐT cho Task 1."""
    setup_directory()

    for doc in LEGAL_DOCS:
        filepath = DATA_DIR / doc["filename"]

        try:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("helvetica", "B", 15)
            pdf.cell(0, 10, doc["title"], new_x="LMARGIN", new_y="NEXT", align="C")
            pdf.ln(5)

            pdf.set_font("helvetica", "I", 10)
            pdf.cell(0, 8, f"Customer Role: {doc['customer_role']}", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(5)

            pdf.set_font("helvetica", "", 11)
            for paragraph in doc["content"].strip().split("\n\n"):
                for line in paragraph.split("\n"):
                    pdf.multi_cell(0, 7, line)
                pdf.ln(3)

            pdf.output(str(filepath))
        except Exception:
            create_pdf_fallback(filepath, doc["title"], doc["customer_role"], doc["content"])

        size = filepath.stat().st_size
        print(f"  ✓ Created: {filepath.name} ({size} bytes)")


if __name__ == "__main__":
    create_legal_pdfs()


