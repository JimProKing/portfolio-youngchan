# -*- coding: utf-8 -*-
"""이영찬 — 포트폴리오 / GitHub / LinkedIn 링크 시트 (A4)"""

from io import BytesIO
from pathlib import Path

import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

OUT = Path(r"C:\Users\a\Desktop\portfolio-youngchan\이영찬_링크_QR.pdf")
OUT_DESKTOP = Path(r"C:\Users\a\Desktop\이영찬_링크_QR.pdf")
FONT_R = r"C:\Windows\Fonts\malgun.ttf"
FONT_B = r"C:\Windows\Fonts\malgunbd.ttf"

NAVY = (0.04, 0.06, 0.12)
CYAN = (0.05, 0.55, 0.72)
TEXT = (0.12, 0.16, 0.24)
MUTE = (0.42, 0.48, 0.58)
LINE = (0.82, 0.86, 0.93)
SOFT = (0.95, 0.97, 0.99)
WHITE = (1, 1, 1)
CARD_BG = (0.98, 0.985, 0.995)

W, H = A4
MARGIN = 18 * mm

LINKS = [
    {
        "label": "01  PORTFOLIO",
        "title": "포트폴리오 사이트",
        "desc": (
            "이영찬 개인 소개 페이지입니다. 스토리·보안 프로젝트·기술 스택을 "
            "한눈에 볼 수 있으며, 데모가 있는 작업은 바로 실행해 보실 수 있습니다."
        ),
        "url": "https://web-production-d48cbf.up.railway.app/",
        "hint": "YC.RUNTIME · Railway",
    },
    {
        "label": "02  GITHUB",
        "title": "GitHub",
        "desc": (
            "위협 헌팅 엔진, 웹 해킹 랩, 보안 학습 도구 등 공개 저장소와 "
            "코드를 확인하실 수 있습니다. (JimProKing)"
        ),
        "url": "https://github.com/JimProKing",
        "hint": "github.com/JimProKing",
    },
    {
        "label": "03  LINKEDIN",
        "title": "LinkedIn",
        "desc": (
            "경력·학력·연락 가능한 프로페셔널 프로필입니다. "
            "협업·채용 관련 메시지도 환영합니다."
        ),
        "url": "https://www.linkedin.com/in/young-chan-lee-9304a3287/",
        "hint": "Young-chan Lee",
    },
]


def reg_fonts():
    pdfmetrics.registerFont(TTFont("KR", FONT_R))
    pdfmetrics.registerFont(TTFont("KR-B", FONT_B))


def set_fill(c, col):
    c.setFillColorRGB(*col)


def set_stroke(c, col):
    c.setStrokeColorRGB(*col)


def wrap_text(text, font, size, max_w, c):
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        buf = ""
        for ch in para:
            trial = buf + ch
            if c.stringWidth(trial, font, size) <= max_w:
                buf = trial
            else:
                if buf:
                    lines.append(buf)
                buf = ch
        if buf:
            lines.append(buf)
    return lines


def make_qr(url: str, box_size: int = 10) -> ImageReader:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0a1628", back_color="white").convert("RGB")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ImageReader(buf)


def draw_round_rect(c, x, y, w, h, r=10, fill=None, stroke=None, sw=0.8):
    c.saveState()
    if fill:
        set_fill(c, fill)
    if stroke:
        set_stroke(c, stroke)
        c.setLineWidth(sw)
    c.roundRect(x, y, w, h, r, fill=1 if fill else 0, stroke=1 if stroke else 0)
    c.restoreState()


def draw_card(c, x, y, w, h, item):
    """Card bottom-left at (x,y). QR on the right, text on the left."""
    draw_round_rect(c, x, y, w, h, r=12, fill=CARD_BG, stroke=LINE, sw=1)
    # left accent
    set_fill(c, CYAN)
    c.roundRect(x, y, 3.5, h, 2, fill=1, stroke=0)

    pad = 14
    qr_size = 38 * mm
    qr_x = x + w - pad - qr_size
    qr_y = y + (h - qr_size) / 2

    # QR plate
    draw_round_rect(
        c, qr_x - 6, qr_y - 6, qr_size + 12, qr_size + 12,
        r=8, fill=WHITE, stroke=LINE, sw=0.6,
    )
    qr_img = make_qr(item["url"])
    c.drawImage(qr_img, qr_x, qr_y, width=qr_size, height=qr_size, mask="auto")

    # text column
    tx = x + pad + 6
    text_w = qr_x - tx - 14
    ty = y + h - pad - 4

    set_fill(c, CYAN)
    c.setFont("KR-B", 8.5)
    c.drawString(tx, ty, item["label"])
    ty -= 16

    set_fill(c, TEXT)
    c.setFont("KR-B", 15)
    c.drawString(tx, ty, item["title"])
    ty -= 14

    set_fill(c, MUTE)
    c.setFont("KR", 8)
    c.drawString(tx, ty, item["hint"])
    ty -= 16

    set_stroke(c, LINE)
    c.setLineWidth(0.6)
    c.line(tx, ty + 6, tx + min(text_w, 120), ty + 6)
    ty -= 4

    set_fill(c, TEXT)
    c.setFont("KR", 9.2)
    for line in wrap_text(item["desc"], "KR", 9.2, text_w, c):
        c.drawString(tx, ty, line)
        ty -= 13.5

    ty -= 6
    set_fill(c, CYAN)
    c.setFont("KR", 8)
    # URL may wrap
    for line in wrap_text(item["url"], "KR", 8, text_w, c):
        c.drawString(tx, ty, line)
        ty -= 11.5


def main():
    reg_fonts()
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("이영찬 — Portfolio · GitHub · LinkedIn")
    c.setAuthor("이영찬")

    # header band
    set_fill(c, NAVY)
    c.rect(0, H - 42 * mm, W, 42 * mm, fill=1, stroke=0)
    set_fill(c, CYAN)
    c.rect(0, H - 42 * mm, W, 2.2, fill=1, stroke=0)

    set_fill(c, WHITE)
    c.setFont("KR-B", 18)
    c.drawString(MARGIN, H - 18 * mm, "이영찬  ·  Lee Young-chan")
    set_fill(c, (0.65, 0.78, 0.88))
    c.setFont("KR", 10)
    c.drawString(MARGIN, H - 26 * mm, "Portfolio  ·  GitHub  ·  LinkedIn")
    set_fill(c, (0.55, 0.68, 0.78))
    c.setFont("KR", 8.5)
    c.drawString(MARGIN, H - 33 * mm, "QR 코드를 스캔하거나 링크를 눌러 바로 이동하세요.")

    # three cards
    card_w = W - 2 * MARGIN
    card_h = 58 * mm
    gap = 8 * mm
    top = H - 50 * mm

    for i, item in enumerate(LINKS):
        y = top - (i + 1) * card_h - i * gap
        draw_card(c, MARGIN, y, card_w, card_h, item)

    # footer
    set_fill(c, MUTE)
    c.setFont("KR", 8)
    c.drawCentredString(W / 2, 12 * mm, "이영찬  ·  caramel2516@naver.com  ·  github.com/JimProKing")

    c.save()
    OUT_DESKTOP.write_bytes(OUT.read_bytes())
    print("WROTE", OUT)
    print("COPY", OUT_DESKTOP)


if __name__ == "__main__":
    main()
