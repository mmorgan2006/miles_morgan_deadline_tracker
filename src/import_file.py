import PySide6.QtWidgets as qt
from docx import Document
from pathlib import Path


def get_location():
    file_path, _ = qt.QFileDialog.getOpenFileName(
            None,
            "Save File",
            "",
            "Word Document (*.docx)"
        )
    return file_path

def import_docx():
    file_path = get_location()
    if not file_path: return
    doc = Document(file_path)
    html_parts = []
    for para in doc.paragraphs:
        if not para.runs:
            html_parts.append("<p></p>")
            continue
        run_html = ""
        for run in para.runs:
            text = (
                run.text.replace("&", "&amp;")
                        .replace("<", "&lt;")
                        .replace(">", "&gt;")
            )
            styles = []
            if run.font.name:
                styles.append(f"font-family:{run.font.name}")
            if run.font.size:
                styles.append(f"font-size:{run.font.size.pt}pt")
            if run.font.color and run.font.color.rgb:
                styles.append(f"color:#{run.font.color.rgb}")
            if styles:
                text = f'<span style="{";".join(styles)}">{text}</span>'
            if run.bold:
                text = f"<b>{text}</b>"
            if run.italic:
                text = f"<i>{text}</i>"
            if run.underline:
                text = f"<u>{text}</u>"
            run_html += text
        html_parts.append(f"<p>{run_html}</p>")
    return "".join(html_parts), Path(file_path).stem
