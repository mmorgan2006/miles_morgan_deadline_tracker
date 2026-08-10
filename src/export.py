import PySide6.QtWidgets as qt
from bs4 import BeautifulSoup
from htmldocx import HtmlToDocx


def get_location():
    file_path, _ = qt.QFileDialog.getSaveFileName(
            None,
            "Save File",
            "",
            "Word Document (*.docx)"
        )
    return file_path
def export(html):
    file_path = get_location()
    if file_path:
        try:
            html = normalize_html(html)
            doc = HtmlToDocx().parse_html_string(html)
            doc.save(file_path)
        except PermissionError:
            qt.QMessageBox.warning(None, "Error", "The file is open elsewhere.")
        except Exception as e:   # noqa: BLE001
            qt.QMessageBox.warning(None, "error", f"Failed to export: {e}")

def normalize_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(style=True):
        style = tag.get("style", "")
        if "font-weight:700" in style or "font-weight:600" in style or "font-weight:bold" in style: #type: ignore
            tag.wrap(soup.new_tag("b"))
        if "font-style:italic" in style: #type: ignore
            tag.wrap(soup.new_tag("i"))
        if "text-decoration:underline" in style or "text-decoration: underline" in style: #type: ignore
            tag.wrap(soup.new_tag("u"))

    for p in soup.find_all("p"):
        children = [c for c in p.contents if str(c).strip() != ""]
        if len(children) == 1 and children[0].name == "br": #type: ignore
            children[0].decompose()

    body = soup.find("body")
    if body:
        return "".join(str(child) for child in body.contents)
    return str(soup)
