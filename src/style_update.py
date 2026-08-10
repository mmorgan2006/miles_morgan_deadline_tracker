from PySide6.QtGui import QColor, QPalette, Qt


def apply_theme(app):
    scheme = app.styleHints().colorScheme()
    if scheme == Qt.ColorScheme.Dark:
        app.setPalette(dark_palette())
        app.setStyleSheet(dark_stylesheet())
    else:
        app.setPalette(light_palette())
        app.setStyleSheet(light_stylesheet())


def light_stylesheet():
    return """
        #AssignmentCard {
            background-color: #ffffff;
            border: 1px solid #3f3f3f;
            border-radius: 8px;
            color: #000000;
        }
        #NoteContainer {
            background-color: #DDDDDD;
            border: 1px solid #3f3f3f;
            border-radius: 10px;
            color: #000000;
        }

        #ClassContainer {
            background-color: #DDDDDD;
            border: 1px solid #222222;
            border-radius: 10px;
        }
        #ClassList {
            background-color: #D3D3D3;
        }
        #ClassListContent {
            background-color: #D3D3D3;
        }
        #NoteCard {
            background-color: #d6d6d6;
        }
    """


def dark_stylesheet():
    return """
        #AssignmentCard {
            background-color: #3F3F3F;
            border: 1px solid #3f3f3f;
            border-radius: 8px;
            color: #ffffff;
        }
        #NoteContainer {
            border: 1px solid #3f3f3f;
            border-radius: 10px;
            color: #ffffff;
        }
        #ClassContainer {
            background-color: #2b2b2b;
            border: 1px solid 3f3f3f;
            border-radius: 10px;
        }
        #ClassList {
            background-color: #1e1e1e;
        }
        #ClassListContent {
            background-color: #1e1e1e;
        }
    """


def light_palette():
    p = QPalette()
    p.setColor(QPalette.Window, QColor("#DDDDDD")) #type: ignore
    p.setColor(QPalette.WindowText, QColor("#1a1a1a")) #type: ignore
    p.setColor(QPalette.Base, QColor("#DDDDDD")) #type: ignore
    p.setColor(QPalette.AlternateBase, QColor("#eaeaea")) #type: ignore
    p.setColor(QPalette.Text, QColor("#1a1a1a")) #type: ignore
    p.setColor(QPalette.Button, QColor("#f0f0f0")) #type: ignore
    p.setColor(QPalette.ButtonText, QColor("#1a1a1a")) #type: ignore
    p.setColor(QPalette.Highlight, QColor("#2169EB"))  #type: ignore
    return p


def dark_palette():
    p = QPalette()
    p.setColor(QPalette.Window, QColor("#2b2b2b")) #type: ignore
    p.setColor(QPalette.WindowText, QColor("#e8e8e8")) #type: ignore
    p.setColor(QPalette.Base, QColor("#1e1e1e")) #type: ignore
    p.setColor(QPalette.AlternateBase, QColor("#333333")) #type: ignore
    p.setColor(QPalette.Text, QColor("#e8e8e8")) #type: ignore
    p.setColor(QPalette.Button, QColor("#3a3a3a")) #type: ignore
    p.setColor(QPalette.ButtonText, QColor("#e8e8e8")) #type: ignore
    p.setColor(QPalette.Highlight, QColor("#2169EB")) #type: ignore
    p.setColor(QPalette.HighlightedText, QColor("#FFFFFF")) #type: ignore
    return p
