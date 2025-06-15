# Стили для темной темы приложения
def get_style():
    styles = """
        QWidget {
            background-color: #303030;
            color: #e0e0e0;
        }
        QPushButton {
            background-color: #3b3b3b;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #3a3a3a;
        }
        QTableWidget {
            background-color: #2a2a2a;
            gridline-color: #444;
        }
        QHeaderView::section {
            background-color: #3b3b3b;
            color: #ffffff;
            padding: 6px;
        }
        QScrollBar:vertical {
            background: #303030;
            width: 10px;
        }
        QScrollBar::handle:vertical {
            background: #5c5c5c;
            border-radius: 5px;
        }
        QTableWidget::item:selected {
            background-color: #007acc;
            color: #ffffff;
        }
        QInputDialog {
            background-color: #262626;
            color: #e0e0e0;
        }
        QLabel {
            color: #e0e0e0;
        }
        QComboBox {
            background-color: #3b3b3b;
            color: #e0e0e0;
        }
        QTextEdit {
            background-color: #262626;
            color: #fafafa;
        }
        QToolBar {
            background-color: #2b2b2b;
            padding: 6px;
        }
        QToolButton {
            background-color: #2e2e2e;
            color: #e0e0e0;
            padding: 5px 10px;
            margin: 5px;
        }
    """
    return styles
