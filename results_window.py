import csv
import numpy as np
from PyQt5.QtWidgets import (
    QDialog, QTableWidget, QTableWidgetItem, QToolBar, QAction,
    QStatusBar, QInputDialog, QVBoxLayout, QMessageBox, QFileDialog, QApplication,
    QPushButton, QFormLayout, QLineEdit, QLabel
)
from PyQt5.QtGui import QIcon, QPixmap, QImage
import base64
from model import build_linear_regression_model
import pandas as pd


class ResultsWindow(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Просмотр данных")
        self.setGeometry(500, 200, 1000, 800)
        self.data = data
        self.parent = parent
        self.model = None
        self.scaler = None
        self.feature_names = []

        # Элементы виджета
        self.toolbar = QToolBar("Панель инструментов")
        self.add_toolbar_actions()
        self.table = QTableWidget()
        self.populate_table(data)
        self.status_bar = QStatusBar()
        self.status_bar.showMessage(f"Загружено строк: {len(data)}")

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.table)
        layout.addWidget(self.status_bar)
        self.setLayout(layout)

    # функция добавления кнопок на панель инструментов
    def add_toolbar_actions(self):
        # Кнопки
        save_action = QAction(QIcon(), "Сохранить", self)
        save_action.triggered.connect(self.save_data)
        save_action.setShortcut("Ctrl+S")
        copy_action = QAction(QIcon(), "Копировать", self)
        copy_action.triggered.connect(self.copy_data)
        plot_action = QAction(QIcon(), "Построить график", self)
        plot_action.triggered.connect(self.plot_data)
        info_action = QAction(QIcon(), "Детальная информация", self)
        info_action.triggered.connect(self.show_column_info)
        build_model_action = QAction(QIcon(), "Построить модель", self)
        build_model_action.triggered.connect(self.build_regression_model)
        predict_action = QAction(QIcon(), "Предсказать MEDV", self)
        predict_action.triggered.connect(self.show_prediction_dialog)
        close_action = QAction(QIcon(), "Закрыть", self)
        close_action.triggered.connect(self.close)

        self.toolbar.addAction(save_action)
        self.toolbar.addAction(copy_action)
        self.toolbar.addAction(plot_action)
        self.toolbar.addAction(info_action)
        self.toolbar.addAction(build_model_action)
        self.toolbar.addAction(predict_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(close_action)

    def populate_table(self, data):
        if data:
            headers = [
                "CRIM", "ZN", "INDUS",
                "CHAS", "NOX", "RM",
                "AGE", "DIS", "RAD", "TAX",
                "PTRATIO", "B", "LSTAT", "MEDV"
            ]

            # Проверяем соответствие количества колонок
            if len(data[0]) != len(headers):
                QMessageBox.warning(self, "Предупреждение",
                                    f"Количество столбцов в данных ({len(data[0])}) "
                                    f"не соответствует ожидаемому ({len(headers)})")

            self.table.setColumnCount(len(headers))
            self.table.setRowCount(len(data))
            self.table.setHorizontalHeaderLabels(headers)

            for i, row in enumerate(data):
                for j, cell in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(cell)))

    def save_data(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить данные",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )

        if not file_name:
            return
        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=' ')
                # Читаем таблицу и записываем данные
                for row in range(self.table.rowCount()):
                    row_data = []
                    for col in range(self.table.columnCount()):
                        item = self.table.item(row, col)
                        row_data.append(item.text() if item else "")
                    writer.writerow(row_data)
            self.status_bar.showMessage(f"Файл успешно сохранен: {file_name}")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось сохранить файл:\n{str(e)}"
            )

    # Функция копирования данных в буфер
    def copy_data(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            return

        # Определение границ выделения
        rows = sorted({item.row() for item in selected_items})
        cols = sorted({item.column() for item in selected_items})
        text = ""
        for row in rows:
            row_data = []
            for col in cols:
                item = self.table.item(row, col)
                row_data.append(item.text() if item else "")
            text += "\t".join(row_data) + "\n"
        # Копируем в буфер обмена
        QApplication.clipboard().setText(text.strip())
        self.status_bar.showMessage(
            f"Скопировано: {len(rows)} строк, {len(cols)} колонок"
        )

    # Получение графиков
    def plot_data(self):
        headers = [
            self.table.horizontalHeaderItem(i).text()
            for i in range(self.table.columnCount())
        ]

        # Запрашиваем у пользователя выбор столбца
        column_name, ok = QInputDialog.getItem(self, "Выбор столбца",
            "Выберите столбец для построения графика:", headers, 0, False)
        if not ok or not column_name:
            return

        # Находим индекс выбранного столбца
        col_index = headers.index(column_name)

        # Собираем данные со столбца
        column_data = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, col_index)
            if item and item.text():
                # Преобразование в число
                try:
                    value = float(item.text())
                    column_data.append(value)
                except ValueError:
                    continue

        if not column_data:
            QMessageBox.warning(
                self,
                "Ошибка данных",
                f"В столбце '{column_name}' нет числовых данных для построения графика"
            )
            return

        # Открываем окно с графиком
        self.parent.open_graph_window(
            f"График: {column_name}",
            column_data,
            column_name
        )

    # Показывает детальную информацию о выбранном столбце
    def show_column_info(self):
        headers = [
            self.table.horizontalHeaderItem(i).text()
            for i in range(self.table.columnCount())
        ]

        if not headers:
            QMessageBox.warning(self, "Ошибка", "В таблице нет столбцов")
            return

        column_name, ok = QInputDialog.getItem(
            self,
            "Выбор столбца",
            "Выберите столбец для получения информации:",
            headers,
            0,
            False
        )

        if not ok or not column_name:
            return

        col_index = headers.index(column_name)
        rows = self.table.rowCount()

        # Собираем данные столбца
        values = []
        for row in range(rows):
            item = self.table.item(row, col_index)
            if item and item.text().strip():
                try:
                    # Пробуем преобразовать в число
                    value = float(item.text())
                    values.append(value)
                except ValueError:
                    # Если не число, сохраняем как строку
                    values.append(item.text())

        # Подсчет статистик
        total_rows = rows
        non_missing = len(values)
        missing = total_rows - non_missing
        missing_percent = (missing / total_rows) * 100 if total_rows > 0 else 0

        # Тип данных
        is_numeric = all(isinstance(v, float) for v in values) if values else False

        info = f"Информация о столбце: {column_name}\n"
        info += f"Всего значений: {total_rows}\n"
        info += f"Непустых значений: {non_missing}\n"
        info += f"Пропущенных значений: {missing}\n"
        info += f"Процент пропусков: {missing_percent:.2f}%\n"
        if is_numeric:
            info += f"Тип данных: Числовой\n"
        else:
            info += f"Тип данных: Текстовый\n"
        if is_numeric and values:
            np_values = np.array(values)
            info += "\nЧисловые характеристики:\n"
            info += f"Медиана: {np.median(np_values):.4f}\n"
            info += f"Минимум: {np.min(np_values):.4f}\n"
            info += f"Среднее: {np.mean(np_values):.4f}\n"
            info += f"Максимум: {np.max(np_values):.4f}\n"
            info += f"Стандартное отклонение: {np.std(np_values):.4f}\n"
        self.parent.open_info_window(info)

    def build_regression_model(self):
        try:
            # Получаем заголовки из таблицы
            headers = []
            for col in range(self.table.columnCount()):
                headers.append(self.table.horizontalHeaderItem(col).text())
            # Собираем актуальные данные из таблицы
            data = []
            for row in range(self.table.rowCount()):
                row_data = []
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item and item.text().strip():
                        try:
                            value = float(item.text())
                            row_data.append(value)
                        except ValueError:
                            row_data.append(np.nan)
                    else:
                        row_data.append(np.nan)
                data.append(row_data)
            df = pd.DataFrame(data, columns=headers)
            df = df.dropna()
            if len(df) < 10:
                raise ValueError("Недостаточно данных для построения модели (минимум 10 строк после очистки)")
            # Строим модель
            self.model, r2, rmse, plot_base64, self.feature_names, self.scaler = build_linear_regression_model(df)
            self.show_model_results(r2, rmse, plot_base64)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось построить модель:\n{str(e)}")

    def show_model_results(self, r2, rmse, plot_base64):
        # Результаты предиктов модели на данные введенных
        result_dialog = QDialog(self)
        result_dialog.setWindowTitle("Результаты модели")
        result_dialog.setFixedSize(1200, 800)

        layout = QVBoxLayout()
        metrics_label = QLabel(
            f"<h3>Метрики модели:</h3>"
            f"R2 (Коэффициент детерминации): {r2:.4f}<br>"
            f"RMSE (Среднеквадратичная ошибка): {rmse:.4f}"
        )
        layout.addWidget(metrics_label)

        # График
        image_data = base64.b64decode(plot_base64)
        image = QImage()
        image.loadFromData(image_data)
        pixmap = QPixmap(image)
        plot_label = QLabel()
        plot_label.setPixmap(pixmap)
        layout.addWidget(plot_label)
        result_dialog.setLayout(layout)
        result_dialog.exec_()

    def show_prediction_dialog(self):
        if not hasattr(self, 'model') or self.model is None:
            QMessageBox.warning(
                self,
                "Модель не построена",
                "Пожалуйста, сначала постройте модель, используя данные из таблицы."
            )
            return

        dialog = PredictionDialog(self.feature_names, self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                features = dialog.get_features()
                features_array = np.array(features).reshape(1, -1)
                features_scaled = self.scaler.transform(features_array)
                prediction = self.model.predict(features_scaled)[0]
                QMessageBox.information(self,
                                        "Результат предсказания", f"Предсказанное значение MEDV: {prediction:.2f}")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка предсказания: {str(e)}")


class PredictionDialog(QDialog):
    def __init__(self, feature_names, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Предсказание MEDV")
        self.setFixedSize(400, 500)

        self.feature_names = feature_names
        self.inputs = {}

        layout = QFormLayout()

        # Поля для ввода всех фич
        for feature in feature_names:
            self.inputs[feature] = QLineEdit()
            self.inputs[feature].setPlaceholderText(f"Введите значение {feature}")
            layout.addRow(feature, self.inputs[feature])

        # Кнопки
        btn_predict = QPushButton("Предсказать")
        btn_cancel = QPushButton("Отмена")
        btn_predict.clicked.connect(self.validate)
        btn_cancel.clicked.connect(self.reject)
        button_layout = QVBoxLayout()
        button_layout.addWidget(btn_predict)
        button_layout.addWidget(btn_cancel)
        layout.addRow(button_layout)

        self.setLayout(layout)

    def validate(self):
        try:
            # Проверка полей
            for name in self.feature_names:
                value = self.inputs[name].text()
                if not value:
                    raise ValueError(f"Поле {name} не заполнено")
                float(value)
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка ввода", str(e))

    def get_features(self):
        features = []
        for name in self.feature_names:
            value = self.inputs[name].text()
            features.append(float(value))
        return features
