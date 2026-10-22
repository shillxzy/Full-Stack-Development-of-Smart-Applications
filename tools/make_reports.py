"""Генерує звіти до лабораторних робіт у форматі .docx (папка reports/).

У звіт потрапляють: титульна сторінка, мета, хід роботи з лістингами програм,
фактичний вивід програм (папки outputs/, створені run_all.py та pytest),
скриншоти й графіки, висновки.

Запуск: .venv\\Scripts\\python tools\\make_reports.py
"""
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from PIL import Image

from reports_content import LABS

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "reports"
MAX_IMAGE_HEIGHT_CM = 21

STUDENT_LINE = "студент(ка) групи 444(Б) ____________________________"
TEACHER_LINE = "____________________________"


def set_cell_shading(paragraph, color="F2F2F2"):
    """Сіра заливка абзацу - для блоків коду та виводу програм."""
    p_pr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    p_pr.append(shd)


def base_styles(doc):
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    normal.font.size = Pt(14)
    normal.paragraph_format.space_after = Pt(4)
    normal.paragraph_format.line_spacing = 1.15
    for name, size in (("Heading 1", 16), ("Heading 2", 14), ("Heading 3", 14)):
        style = doc.styles[name]
        style.font.name = "Times New Roman"
        style.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0, 0, 0)
        # Шрифт теми документа (Calibri Light) має пріоритет над явно заданим - прибираємо його.
        r_fonts = style.element.rPr.rFonts
        for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
            r_fonts.attrib.pop(qn(attr), None)
    section = doc.sections[0]
    section.left_margin, section.right_margin = Cm(2.5), Cm(1.5)
    section.top_margin = section.bottom_margin = Cm(2)


def centered(doc, text, size=14, bold=False, space_after=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(space_after)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.bold = bold
    return p


def title_page(doc, lab):
    centered(doc, "МІНІСТЕРСТВО ОСВІТИ І НАУКИ УКРАЇНИ", bold=True)
    centered(doc, "Чернівецький національний університет імені Юрія Федьковича", bold=True)
    centered(doc, "Навчально-науковий інститут фізико-технічних та комп'ютерних наук", space_after=100)
    centered(doc, "ЗВІТ", size=18, bold=True, space_after=6)
    centered(doc, f"про виконання лабораторної роботи №{lab['number']}", size=16)
    centered(doc, "з дисципліни «Full-Stack розробка»", size=16, space_after=12)
    centered(doc, f"Тема: «{lab['title']}»", size=16, bold=True, space_after=110)
    for label, value in (("Виконав(ла):", STUDENT_LINE), ("Перевірив(ла):", TEACHER_LINE)):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(8)
        p.add_run(label + "\n").bold = True
        p.add_run(value)
    p = centered(doc, "Чернівці – 2026")
    p.paragraph_format.space_before = Pt(90)


def heading(doc, text, level):
    doc.add_heading(text, level=level)


def paragraph(doc, text):
    for chunk in text.strip().split("\n\n"):
        p = doc.add_paragraph(chunk.strip())
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.first_line_indent = Cm(1.25)


def bullets(doc, items):
    for item in items:
        doc.add_paragraph(item, style="List Bullet")


def code_block(doc, text, size=9):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.0
    set_cell_shading(p)
    lines = text.rstrip("\n").split("\n")
    for i, line in enumerate(lines):
        run = p.add_run(line.replace("\t", "    "))
        run.font.name = "Consolas"
        run.element.rPr.rFonts.set(qn("w:eastAsia"), "Consolas")
        run.font.size = Pt(size)
        if i < len(lines) - 1:
            run.add_break()


def caption(doc, text):
    p = doc.add_paragraph(text)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.runs[0].italic = True
    p.runs[0].font.size = Pt(12)


def render_item(doc, lab_dir, item, counters):
    kind = item[0]
    if kind == "text":
        paragraph(doc, item[1])
    elif kind == "bullets":
        bullets(doc, item[1])
    elif kind == "h":
        heading(doc, item[1], 2)
    elif kind == "code":                     # ("code", "шлях", необов'язковий підпис)
        path = lab_dir / item[1]
        counters["listing"] += 1
        p = doc.add_paragraph()
        p.add_run(f"Лістинг {counters['listing']} – файл {item[1]}").bold = True
        code_block(doc, path.read_text(encoding="utf-8-sig"))
    elif kind == "output":                   # ("output", "outputs/x.txt", "підпис")
        path = lab_dir / item[1]
        p = doc.add_paragraph()
        p.add_run(item[2] if len(item) > 2 else "Результат виконання:").bold = True
        text = path.read_text(encoding="utf-8")
        max_lines = item[3] if len(item) > 3 else 120
        lines = text.rstrip("\n").split("\n")
        if len(lines) > max_lines:
            lines = lines[:max_lines] + [f"... (повний вивід - у файлі {item[1]})"]
        code_block(doc, "\n".join(lines), size=8.5)
    elif kind == "image":                    # ("image", "шлях", "підпис", ширина_см)
        counters["figure"] += 1
        path = lab_dir / item[1]
        width = item[3] if len(item) > 3 else 16
        with Image.open(path) as img:
            ratio = img.height / img.width
        if width * ratio > MAX_IMAGE_HEIGHT_CM:          # дуже високі скриншоти не мають вилазити за сторінку
            doc.add_picture(str(path), height=Cm(MAX_IMAGE_HEIGHT_CM))
        else:
            doc.add_picture(str(path), width=Cm(width))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        caption(doc, f"Рисунок {counters['figure']} – {item[2]}")
    else:
        raise ValueError(kind)


def build(lab):
    doc = Document()
    base_styles(doc)
    title_page(doc, lab)
    lab_dir = ROOT / lab["folder"]
    counters = {"listing": 0, "figure": 0}

    heading(doc, "Мета роботи", 1)
    doc.paragraphs[-1].paragraph_format.page_break_before = True   # титулка завжди на окремій сторінці
    paragraph(doc, lab["goal"])
    heading(doc, "Хід роботи", 1)
    for item in lab["body"]:
        render_item(doc, lab_dir, item, counters)
    if lab.get("questions"):
        heading(doc, "Відповіді на контрольні запитання", 1)
        for q, a in lab["questions"]:
            p = doc.add_paragraph()
            p.add_run(q).bold = True
            paragraph(doc, a)
    heading(doc, "Висновки", 1)
    paragraph(doc, lab["conclusions"])

    OUT.mkdir(exist_ok=True)
    path = OUT / f"ЛР{lab['number']:02d}_{lab['file_title']}.docx"
    doc.save(path)
    return path


if __name__ == "__main__":
    for lab in LABS:
        print("saved", build(lab).relative_to(ROOT))
