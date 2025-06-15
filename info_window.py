from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtGui import QFont


class DfInfoWindow(QDialog):
    def __init__(self, info_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Детальная информация о столбце")
        self.setGeometry(700, 300, 800, 650)
        layout = QVBoxLayout()
        # Поле информации
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setText(info_text)
        text_edit.setFont(QFont("Times New Roman", 10))
        text_edit.setLineWrapMode(QTextEdit.NoWrap)
        # Кнопки
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        close_button.setFixedHeight(40)

        layout.addWidget(text_edit)
        layout.addWidget(close_button)
        self.setLayout(layout)
