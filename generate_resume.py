# -*- coding: utf-8 -*-
"""이영찬 이력서 PDF 생성 — YC.RUNTIME 톤"""

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

OUT = Path(r"C:\Users\a\Desktop\portfolio-youngchan\이영찬_이력서.pdf")
PHOTO = Path(r"C:\Users\a\Desktop\임시\이영찬-수정원본.jpg")
FONT_R = r"C:\Windows\Fonts\malgun.ttf"
FONT_B = r"C:\Windows\Fonts\malgunbd.ttf"

# Palette (portfolio-aligned)
NAVY = (0.02, 0.03, 0.08)
SIDE = (0.05, 0.08, 0.16)
CARD = (0.96, 0.97, 0.99)
LINE = (0.82, 0.86, 0.93)
CYAN = (0.05, 0.55, 0.72)
TEXT = (0.12, 0.16, 0.24)
MUTE = (0.40, 0.45, 0.55)
WHITE = (1, 1, 1)
SOFT = (0.94, 0.96, 0.99)

W, H = A4  # 595.27 x 841.89
SIDE_W = 58 * mm
MARGIN = 14 * mm
RIGHT_X = SIDE_W + 12 * mm
RIGHT_W = W - RIGHT_X - MARGIN


def rgb(c, a=None):
    return c


def reg_fonts():
    pdfmetrics.registerFont(TTFont("KR", FONT_R))
    pdfmetrics.registerFont(TTFont("KR-B", FONT_B))


def set_fill(c, col):
    c.setFillColorRGB(*col)


def set_stroke(c, col):
    c.setStrokeColorRGB(*col)


def draw_round_rect(c, x, y, w, h, r=6, fill=None, stroke=None, sw=0.6):
    c.saveState()
    if fill:
        set_fill(c, fill)
    if stroke:
        set_stroke(c, stroke)
        c.setLineWidth(sw)
    else:
        c.setStrokeColorRGB(*fill if fill else WHITE)
    c.roundRect(x, y, w, h, r, fill=1 if fill else 0, stroke=1 if stroke else 0)
    c.restoreState()


def wrap_text(text, font, size, max_w, c):
    """Wrap preferring spaces; fall back to char break for long CJK/tokens."""
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        words = para.split(" ")
        buf = ""
        for wi, word in enumerate(words):
            piece = word if buf == "" else buf + " " + word
            if c.stringWidth(piece, font, size) <= max_w:
                buf = piece
                continue
            if buf:
                lines.append(buf)
                buf = ""
            # word alone may exceed width — hard-break by char
            if c.stringWidth(word, font, size) <= max_w:
                buf = word
            else:
                chunk = ""
                for ch in word:
                    trial = chunk + ch
                    if c.stringWidth(trial, font, size) <= max_w:
                        chunk = trial
                    else:
                        if chunk:
                            lines.append(chunk)
                        chunk = ch
                buf = chunk
        if buf:
            lines.append(buf)
    return lines


def draw_paragraph(c, text, x, y, max_w, font="KR", size=9, leading=13.5, color=TEXT, max_lines=None):
    lines = wrap_text(text, font, size, max_w, c)
    if max_lines:
        lines = lines[:max_lines]
    set_fill(c, color)
    c.setFont(font, size)
    for i, line in enumerate(lines):
        c.drawString(x, y - i * leading, line)
    return y - len(lines) * leading


def draw_section_title(c, title, x, y, w):
    set_fill(c, TEXT)
    c.setFont("KR-B", 11)
    c.drawString(x, y, title)
    set_stroke(c, CYAN)
    c.setLineWidth(1.6)
    c.line(x, y - 4, x + min(28 * mm, w * 0.25), y - 4)
    set_stroke(c, LINE)
    c.setLineWidth(0.5)
    c.line(x + min(28 * mm, w * 0.25) + 4, y - 4, x + w, y - 4)
    return y - 16


def draw_chip(c, label, x, y, font="KR", size=7.5):
    pad_x, pad_y = 5, 3
    tw = c.stringWidth(label, font, size)
    w, h = tw + pad_x * 2, size + pad_y * 2 + 1
    draw_round_rect(c, x, y - pad_y, w, h, r=3.5, fill=(0.90, 0.96, 0.98), stroke=(0.70, 0.88, 0.93))
    set_fill(c, CYAN)
    c.setFont(font, size)
    c.drawString(x + pad_x, y, label)
    return w + 4


def draw_sidebar(c, page=1):
    # full height sidebar
    set_fill(c, SIDE)
    c.rect(0, 0, SIDE_W, H, fill=1, stroke=0)
    # accent bar
    set_fill(c, CYAN)
    c.rect(0, 0, 3.2, H, fill=1, stroke=0)

    # photo circle
    photo_d = 38 * mm
    px = (SIDE_W - photo_d) / 2
    py = H - 22 * mm - photo_d

    if PHOTO.exists():
        c.saveState()
        path = c.beginPath()
        path.circle(px + photo_d / 2, py + photo_d / 2, photo_d / 2)
        c.clipPath(path, stroke=0)
        img = ImageReader(str(PHOTO))
        # cover crop
        c.drawImage(img, px - 2, py - 4, width=photo_d + 4, height=photo_d + 8, preserveAspectRatio=True, anchor="c", mask="auto")
        c.restoreState()
        set_stroke(c, CYAN)
        c.setLineWidth(1.8)
        c.circle(px + photo_d / 2, py + photo_d / 2, photo_d / 2 + 1.2, fill=0, stroke=1)

    # name
    set_fill(c, WHITE)
    c.setFont("KR-B", 16)
    name = "이 영 찬"
    c.drawCentredString(SIDE_W / 2, py - 14 * mm, name)
    c.setFont("KR", 8)
    set_fill(c, (0.55, 0.72, 0.82))
    c.drawCentredString(SIDE_W / 2, py - 19 * mm, "Lee Young-chan")
    set_fill(c, (0.65, 0.72, 0.82))
    c.setFont("KR", 7.5)
    c.drawCentredString(SIDE_W / 2, py - 24 * mm, "전산 · 보안 · 풀스택 개발")

    y = py - 32 * mm

    def side_block(title, items, y0):
        set_fill(c, CYAN)
        c.setFont("KR-B", 8)
        c.drawString(10 * mm, y0, title)
        set_stroke(c, (0.15, 0.28, 0.38))
        c.setLineWidth(0.5)
        c.line(10 * mm, y0 - 3, SIDE_W - 8 * mm, y0 - 3)
        y1 = y0 - 12
        for it in items:
            set_fill(c, (0.82, 0.88, 0.94))
            c.setFont("KR", 7.2)
            # wrap long lines
            lines = wrap_text(it, "KR", 7.2, SIDE_W - 18 * mm, c)
            for ln in lines:
                c.drawString(10 * mm, y1, ln)
                y1 -= 10
            y1 -= 2
        return y1 - 6

    y = side_block("CONTACT", [
        "caramel2516@naver.com",
        "Kakao · caramel112",
        "github.com/JimProKing",
        "1996. 12. 27",
    ], y)

    y = side_block("SKILLS", [
        "Language",
        "  Python · Dart · JS · HTML/CSS",
        "  VBA",
        "Backend",
        "  FastAPI · Flask · Django · Spring",
        "Mobile",
        "  Flutter (iOS · Android 배포)",
        "Security",
        "  웹해킹 · SQLi/XSS/IDOR · Burp",
        "Detect",
        "  로그 상관 · IOC · ATT&CK",
        "Data / Ops",
        "  pandas · 크롤링 · OCR",
        "  GitHub Actions · Railway",
    ], y)

    y = side_block("EDUCATION", [
        "경상국립대학교",
        "융합전공 P&P화학공학",
        "공학사 · 2021. 02 졸업",
    ], y)

    y = side_block("CERT / EXAM", [
        "국가직 9급 전산직 합격",
        "국세청 전산직 재직 중",
        "정보보안기사 학습 중",
    ], y)

    if page == 1:
        side_block("LINKS", [
            "github.com/JimProKing",
            "Public repos 50+",
            "상호명 짐앱 (JimApp)",
            "Portfolio · Railway 배포",
        ], y)
    else:
        side_block("MOBILE APPS", [
            "미라클모닝 · 기적의 습관",
            "영어단어의 전설 시리즈",
            "영어 토익 9000",
            "오픽의 전설",
            "한국사의 전설",
            "화공기사 필기·실기",
            "다국어성경 2023 외 다수",
        ], y)


def page1(c):
    # background
    set_fill(c, WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_sidebar(c, 1)

    x = RIGHT_X
    y = H - 18 * mm

    # Header
    set_fill(c, TEXT)
    c.setFont("KR-B", 18)
    c.drawString(x, y, "이력서  /  RESUME")
    y -= 8
    set_stroke(c, CYAN)
    c.setLineWidth(2.2)
    c.line(x, y, x + 36 * mm, y)
    y -= 14

    # summary card
    summary = (
        "화학공학 현장 자동화에서 출발해 Flutter로 10여 개 모바일 앱을 직접 출시·운영하고, "
        "앱 해킹 피해를 계기로 보안 역량을 키워 국가직 9급 전산직에 합격한 개발자입니다. "
        "현재 국세청 전산직으로 근무하며, 방어형 위협 헌팅·웹 해킹 교육 랩·실전 웹 도구를 "
        "GitHub에 공개하며 보안·개발 역량을 계속 확장하고 있습니다."
    )
    card_h = 42 * mm
    draw_round_rect(c, x, y - card_h + 8, RIGHT_W, card_h, r=7, fill=SOFT, stroke=LINE)
    set_fill(c, CYAN)
    c.rect(x, y - card_h + 8, 2.8, card_h, fill=1, stroke=0)
    draw_paragraph(c, summary, x + 8, y - 4, RIGHT_W - 14, size=8.6, leading=12.8, color=TEXT)
    y = y - card_h - 6

    # Experience
    y = draw_section_title(c, "경력 및 여정", x, y, RIGHT_W)
    y -= 2

    jobs = [
        {
            "title": "전산직 공무원",
            "org": "국세청 · 국가직 9급",
            "when": "현재",
            "bullets": [
                "4개월 집중 수험 후 국가직 9급 전산직 합격, 국세청 전산 업무 수행",
                "앱 해킹 피해 경험을 계기로 법리·보안 전문성 보완을 목표로 공직 진출",
                "행정 전산 환경에서의 안정적 시스템 운영·업무 전산화 감각 축적",
            ],
        },
        {
            "title": "모바일 앱 개발 · 개인사업자 (상호명: 짐앱)",
            "org": "App Store · Google Play · Flutter 크로스플랫폼",
            "when": "2022 – 2023",
            "bullets": [
                "Flutter로 교육·자격 대비 앱 10여 개 직접 개발, iOS·Android 동시 출시·판매",
                "영어·토익·오픽, 한국사, 화공기사, 미라클모닝 등 시리즈 운영 (App Store · Play Console)",
                "기획·UI·배포·판매까지 전 과정 단독 수행, 개인사업자 형태로 서비스 운영",
                "출시 앱 해킹 피해를 겪으며 개발만으로는 부족한 보안·대응 역량의 필요성을 체감",
            ],
        },
        {
            "title": "화학 엔지니어",
            "org": "화학공학 전공 후 사회생활 시작",
            "when": "입사 후 약 1년",
            "bullets": [
                "화학공학 전공 후, 화학 엔지니어로 사회생활을 시작",
                "다양한 공정 자동화 프로그램을 개인적 프로젝트로 만들며 개발에 적성을 느낌",
                "이후 본격적으로 개발 공부를 시작한 뒤 전산계통으로 업종을 변경",
            ],
        },
    ]

    for job in jobs:
        # title row
        set_fill(c, TEXT)
        c.setFont("KR-B", 10)
        c.drawString(x, y, job["title"])
        set_fill(c, MUTE)
        c.setFont("KR", 8)
        tw = c.stringWidth(job["when"], "KR", 8)
        c.drawRightString(x + RIGHT_W, y, job["when"])
        y -= 11
        set_fill(c, CYAN)
        c.setFont("KR", 8)
        c.drawString(x, y, job["org"])
        y -= 12
        for b in job["bullets"]:
            set_fill(c, MUTE)
            c.setFont("KR", 8.2)
            c.drawString(x + 1, y, "·")
            y = draw_paragraph(c, b, x + 8, y, RIGHT_W - 10, size=8.2, leading=11.5, color=TEXT)
            y -= 3
        y -= 8

    # Projects
    y = draw_section_title(c, "주요 프로젝트 (GitHub)", x, y, RIGHT_W)
    y -= 2

    projects = [
        (
            "Aegis Cortex — 방어형 위협 헌팅 엔진",
            "인증·방화벽·프록시·DNS·EDR 로그와 IOC를 상관분석해 킬체인 스토리를 재구성. MITRE ATT&CK 매핑·리포트 생성 (Python).",
            "Python · 상관분석 · IOC · ATT&CK  ·  github.com/JimProKing/aegis-cortex",
        ),
        (
            "AEGIS PROTOCOL — 정보보안 교육 시뮬레이션",
            "브라우저 기반 10개 작전(CIA~탐지대응). 브리핑·실습·디브리핑으로 위험·신뢰경계·심층방어 사고 프레임 훈련.",
            "JavaScript · 교육 게임 · 오프라인  ·  github.com/JimProKing/aegis-protocol",
        ),
        (
            "VulnBoard / 웹해킹 바이블 랩",
            "의도적 취약 웹 실습(SQLi, XSS, IDOR, Command Injection 등). Burp Suite 실습·구조화된 문제와 풀이 제공.",
            "Python · Flask · 웹 보안  ·  github.com/JimProKing/webhacking-bible-lab",
        ),
        (
            "Elliott Wave Scanner · Optical QR Transfer",
            "엘리어트 파동 기반 차트 스캐너(GitHub Actions 자동 분석). 인터넷 없이 빛(QR)·카메라만으로 파일 전송 프로토타입.",
            "Python · JS · Railway  ·  github.com/JimProKing",
        ),
        (
            "info-sec-memo · tax-invoice-web 외",
            "정보보안기사 손글씨 기출 웹 노트(82p), 한국형 세금계산서 작성 웹앱 등 실무·학습용 도구.",
            "Flask · JavaScript · 실무 웹",
        ),
    ]

    for title, desc, meta in projects:
        if y < 28 * mm:
            break
        set_fill(c, TEXT)
        c.setFont("KR-B", 9)
        c.drawString(x, y, title)
        y -= 11
        y = draw_paragraph(c, desc, x, y, RIGHT_W, size=8, leading=11.2, color=TEXT)
        y -= 1
        set_fill(c, MUTE)
        c.setFont("KR", 7.2)
        c.drawString(x, y, meta)
        y -= 13

    # footer
    set_fill(c, MUTE)
    c.setFont("KR", 7)
    c.drawCentredString(W / 2 + SIDE_W / 4, 10 * mm, "1 / 2  ·  이영찬  ·  github.com/JimProKing")


def page2(c):
    set_fill(c, WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    draw_sidebar(c, 2)

    x = RIGHT_X
    y = H - 18 * mm

    set_fill(c, TEXT)
    c.setFont("KR-B", 16)
    c.drawString(x, y, "스토리 — 왜 이 길을 택했는가")
    y -= 8
    set_stroke(c, CYAN)
    c.setLineWidth(2.2)
    c.line(x, y, x + 42 * mm, y)
    y -= 16

    story = (
        "화학공학 전공 후, 화학 엔지니어로 사회생활을 시작하였습니다. "
        "다양한 공정 자동화 프로그램을 개인적 프로젝트로 만들며, 개발에 적성을 느꼈습니다. "
        "이후, 본격적으로 개발 공부를 시작한 뒤 전산계통으로 업종을 변경하였습니다.\n\n"
        "퇴사 후 프로그래밍과 컴퓨터공학 실력을 쌓았고, ‘내 손으로 만든 앱을 스토어에 올리고 싶다’는 "
        "목표로 Flutter를 택했습니다. 안드로이드·iOS 동시 배포가 가능했기 때문입니다. "
        "개인사업자(상호명 짐앱)를 내고 교육·자격 대비 앱 10여 개를 직접 개발·출시·판매했습니다.\n\n"
        "이후 제작한 모바일 앱이 해킹당하는 일을 겪었습니다. 개발 실력만으로는 해결되지 않는 문제가 "
        "많다는 것을 배웠고, 법리와 보안 전문성을 함께 키우고 싶었습니다. 전산직 공무원 수험이 그 "
        "공백을 메우는 길이 될 수 있다고 판단해 4개월간 준비하고, 국가직 9급에 합격해 국세청 "
        "전산직으로 근무하고 있습니다.\n\n"
        "공직 생활과 병행해 GitHub(JimProKing)에 방어형 위협 헌팅 엔진, 정보보안 교육 게임, 웹 해킹 "
        "실습 랩, 금융·온체인 분석 도구 등을 공개하며 실전 역량을 계속 쌓고 있습니다."
    )
    y = draw_paragraph(c, story, x, y, RIGHT_W, size=8.8, leading=13.2, color=TEXT)
    y -= 14

    y = draw_section_title(c, "핵심 강점", x, y, RIGHT_W)
    y -= 4

    strengths = [
        ("현장 → 코드", "공정 자동화·개인 프로젝트 경험으로 ‘현장 문제를 소프트웨어로 줄이는’ 감각을 갖춤"),
        ("제품 출시 경험", "아이디어를 스토어 배포·운영까지 완주한 10+ 앱 포트폴리오 (짐앱)"),
        ("보안 동기부여", "실제 해킹 피해를 계기로 방어·교육·탐지 쪽으로 학습 방향을 전환"),
        ("공직 + 개발", "국세청 전산 업무와 개인 오픈소스 프로젝트를 병행하는 실행력"),
        ("학습의 공개화", "정보보안 교육 게임·암기장·랩을 만들어 스스로 검증하며 공유"),
    ]

    for title, desc in strengths:
        # mini card
        ch = 18 * mm
        if y - ch < 55 * mm:
            break
        draw_round_rect(c, x, y - ch + 6, RIGHT_W, ch, r=5, fill=SOFT, stroke=LINE)
        set_fill(c, CYAN)
        c.setFont("KR-B", 8.5)
        c.drawString(x + 7, y - 2, title)
        draw_paragraph(c, desc, x + 7, y - 13, RIGHT_W - 14, size=8, leading=11, color=TEXT)
        y -= ch + 4

    y -= 6
    y = draw_section_title(c, "기술 스택 한눈에", x, y, RIGHT_W)
    y -= 2

    chips = [
        "Python", "Flutter / Dart", "FastAPI", "Flask", "Django", "Spring",
        "JavaScript", "HTML/CSS", "VBA / Excel", "SQLite", "pandas",
        "GitHub Actions", "Burp Suite", "MITRE ATT&CK", "XRPL / Binance API",
        "Railway", "OCR", "Three.js",
    ]
    cx, cy = x, y
    row_h = 14
    for label in chips:
        tw = c.stringWidth(label, "KR", 7.5) + 12
        if cx + tw > x + RIGHT_W:
            cx = x
            cy -= row_h
        draw_chip(c, label, cx, cy - 2)
        cx += tw + 2
    y = cy - 20

    y = draw_section_title(c, "학력", x, y, RIGHT_W)
    set_fill(c, TEXT)
    c.setFont("KR-B", 9.5)
    c.drawString(x, y, "경상국립대학교 (Gyeongsang National University)")
    set_fill(c, MUTE)
    c.setFont("KR", 8)
    c.drawRightString(x + RIGHT_W, y, "2021. 02")
    y -= 12
    set_fill(c, MUTE)
    c.setFont("KR", 8.2)
    c.drawString(x, y, "융합전공 P&P화학공학 · 공학사")
    y -= 18

    y = draw_section_title(c, "연락 및 포트폴리오", x, y, RIGHT_W)
    rows = [
        ("Email", "caramel2516@naver.com"),
        ("KakaoTalk", "caramel112"),
        ("GitHub", "https://github.com/JimProKing"),
        ("주요 저장소", "aegis-cortex · aegis-protocol · webhacking-bible-lab · elliott-wave-scanner"),
        ("Portfolio", "Railway 배포 예정 (YC.RUNTIME)"),
    ]
    for k, v in rows:
        set_fill(c, MUTE)
        c.setFont("KR-B", 8)
        c.drawString(x, y, k)
        set_fill(c, TEXT)
        c.setFont("KR", 8.2)
        c.drawString(x + 28 * mm, y, v)
        y -= 12

    y -= 6
    note = (
        "위의 경력·프로젝트는 실제 경험과 GitHub 공개 저장소를 바탕으로 작성했습니다. "
        "상세 코드·데모는 github.com/JimProKing 에서 확인하실 수 있습니다."
    )
    draw_round_rect(c, x, y - 22 * mm + 6, RIGHT_W, 22 * mm, r=5, fill=SOFT, stroke=LINE)
    draw_paragraph(c, note, x + 7, y - 2, RIGHT_W - 14, size=7.8, leading=11.2, color=MUTE)

    set_fill(c, MUTE)
    c.setFont("KR", 7)
    c.drawCentredString(W / 2 + SIDE_W / 4, 10 * mm, "2 / 2  ·  이영찬  ·  github.com/JimProKing")


def main():
    reg_fonts()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=A4)
    c.setTitle("이영찬 이력서 — Lee Young-chan")
    c.setAuthor("이영찬")
    c.setSubject("Resume / Portfolio companion")
    page1(c)
    c.showPage()
    page2(c)
    c.save()
    print("WROTE", OUT)
    print("SIZE", OUT.stat().st_size)


if __name__ == "__main__":
    main()
