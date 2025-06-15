import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton


class GraphWindow(QDialog):
    def __init__(self, title, data, column_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(600, 300, 800, 600)
        self.data = data
        self.column_name = column_name
        self.parent = parent

        # Создаем фигуру matplotlib
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        # Кнопки
        self.hist_button = QPushButton("Гистограмма")
        self.hist_button.clicked.connect(self.histogram_plot)
        self.scatter_button = QPushButton("Точечный график")
        self.scatter_button.clicked.connect(self.scatter_plot)
        self.line_button = QPushButton("Линейный график")
        self.line_button.clicked.connect(self.line_plot)
        self.box_button = QPushButton("Box plot")
        self.box_button.clicked.connect(self.boxplot)

        # Панель кнопок
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.hist_button)
        button_layout.addWidget(self.scatter_button)
        button_layout.addWidget(self.line_button)
        button_layout.addWidget(self.box_button)

        # Основной виджет
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Строим сразу гистограмму
        self.change_window_theme()
        self.histogram_plot()

    def change_window_theme(self):
        if self.parent.is_dark_theme:
            plt.style.use('dark_background')
            self.figure.set_facecolor('#1e1e1e')
            self.ax.set_facecolor('#2a2a2a')
        else:
            plt.style.use('default')
            self.figure.set_facecolor('white')
            self.ax.set_facecolor('white')

    def line_plot(self):
        """Построение линейного графика"""
        self.ax.clear()
        self.change_window_theme()
        # Строим линейный график
        x = range(len(self.data))
        self.ax.plot(
            x,
            self.data,
            color='#2ca02c',
            linewidth=2,
            marker='o',
            markersize=4
        )
        self.ax.set_title(f'Линейный график: {self.column_name}', fontsize=14)
        self.ax.set_xlabel('Номер наблюдения', fontsize=12)
        self.ax.set_ylabel(self.column_name, fontsize=12)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.canvas.draw()

    def histogram_plot(self):
        """Построение гистограммы"""
        self.ax.clear()
        self.change_window_theme()
        # Строим гистограмму
        n, bins, patches = self.ax.hist(
            self.data,
            bins=15,
            color='#007acc',
            edgecolor='white',
            alpha=0.7
        )
        self.ax.set_title(f'Распределение значений: {self.column_name}', fontsize=14)
        self.ax.set_xlabel(self.column_name, fontsize=12)
        self.ax.set_ylabel('Частота', fontsize=12)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        # Обновление холста
        self.canvas.draw()

    def boxplot(self):
        """Построение box plot"""
        self.ax.clear()
        self.change_window_theme()
        # Строим box plot
        box = self.ax.boxplot(
            self.data,
            patch_artist=True,
            boxprops=dict(facecolor='#1f77b4', color='white'),
            whiskerprops=dict(color='white'),
            capprops=dict(color='white'),
            medianprops=dict(color='yellow'),
            flierprops=dict(marker='o', markersize=5, markerfacecolor='red')
        )
        self.ax.set_title(f'Box plot: {self.column_name}', fontsize=14)
        self.ax.set_ylabel(self.column_name, fontsize=12)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        # Убираем ненужную ось X
        self.ax.set_xticks([])
        # Обновляем холст
        self.canvas.draw()

    def scatter_plot(self):
        """Построение точечного графика"""
        self.ax.clear()
        self.change_window_theme()
        # Строим точечный график
        x = range(len(self.data))
        self.ax.scatter(
            x,
            self.data,
            c='#d62728',
            alpha=0.7,
            edgecolors='w'
        )
        self.ax.set_title(f'Точечный график: {self.column_name}', fontsize=14)
        self.ax.set_xlabel('Номер наблюдения', fontsize=12)
        self.ax.set_ylabel(self.column_name, fontsize=12)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.canvas.draw()
