from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout,
    QWidget, QLabel, QFileDialog
)
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtGui import QFont
from results_window import ResultsWindow
from graph_window import GraphWindow
from info_window import DfInfoWindow
from style import get_style


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ цен на жилье в Бостоне")
        self.setGeometry(500, 200, 400, 200)
        self.settings = QSettings("-", "Анализ цен на жилье в Бостоне")
        self.load_settings()

        self.is_dark_theme = False
        self.results_windows = []
        self.graph_windows = []
        self.info_windows = []

        #
        title = QLabel("Предсказание цен на жилье в Бостоне")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))

        self.load_button = QPushButton("Загрузить CSV")
        self.load_button.setFixedHeight(40)
        self.load_button.clicked.connect(self.load_dataset)
        self.change_theme_button = QPushButton("Переключить тему")
        self.change_theme_button.setFixedHeight(40)
        self.change_theme_button.clicked.connect(self.change_theme)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(self.load_button)
        layout.addWidget(self.change_theme_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_dataset(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите CSV файл", "", "CSV Files (*.csv);;All Files (*)")
        if file_name:
            data = self.read_csv(file_name)
            self.open_results_window(data)

    def change_theme(self):
        dark_stylesheet = get_style()

        if self.is_dark_theme:
            self.setStyleSheet("")
            for window in self.results_windows:
                window.setStyleSheet("")
            for window in self.graph_windows:
                window.setStyleSheet("")
            for window in self.info_windows:
                window.setStyleSheet("")
            self.is_dark_theme = False
        else:
            self.setStyleSheet(dark_stylesheet)
            for window in self.results_windows:
                window.setStyleSheet(dark_stylesheet)
            for window in self.graph_windows:
                window.setStyleSheet(dark_stylesheet)
            for window in self.info_windows:
                window.setStyleSheet(dark_stylesheet)
            self.is_dark_theme = True

    # функиця чтения файла
    def read_csv(self, file_name):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                data = []
                for line in file:
                    row = line.strip().split()
                    if row:
                        data.append(row)
                return data
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return []

    def open_results_window(self, data):
        results_window = ResultsWindow(data, self)
        results_window.show()
        self.results_windows.append(results_window)
        if self.is_dark_theme:
            results_window.setStyleSheet(self.styleSheet())

    def open_graph_window(self, title, column_data, column_name):
        graph_window = GraphWindow(title, column_data, column_name, self)
        graph_window.show()
        self.graph_windows.append(graph_window)
        if self.is_dark_theme:
            graph_window.setStyleSheet(self.styleSheet())

    def open_info_window(self, info_text):
        info_window = DfInfoWindow(info_text, self)
        info_window.show()
        self.info_windows.append(info_window)
        if self.is_dark_theme:
            info_window.setStyleSheet(self.styleSheet())

    def load_settings(self):
        self.restoreGeometry(self.settings.value("geometry", self.saveGeometry()))

    def closeEvent(self, event):
        self.settings.setValue("geometry", self.saveGeometry())
        super().closeEvent(event)
