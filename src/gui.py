import pandas as pd
from PyQt6.QtWidgets import (QMainWindow, QLabel, QPushButton, QFileDialog, QTableWidget,
                              QTableWidgetItem, QMessageBox, QTextEdit, QGridLayout, QWidget)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Evaluación de Proyectos")
        self.setGeometry(100, 100, 1280, 900)

        layout = QGridLayout()

        self.file1_button = QPushButton("Cargar archivo de Variables y Pesos")
        self.file1_button.clicked.connect(self.load_file1)
        layout.addWidget(self.file1_button, 0, 0)

        self.file2_button = QPushButton("Cargar archivo de Ideas de Proyectos")
        self.file2_button.clicked.connect(self.load_file2)
        layout.addWidget(self.file2_button, 0, 1)

        self.file1_table = QTableWidget()
        layout.addWidget(self.file1_table, 1, 0)

        self.file2_table = QTableWidget()
        layout.addWidget(self.file2_table, 1, 1)

        self.process_button = QPushButton("Procesar Evaluación")
        self.process_button.clicked.connect(self.process_evaluation)
        layout.addWidget(self.process_button, 2, 0, 1, 2)

        self.evaluation_table = QTableWidget()
        layout.addWidget(self.evaluation_table, 3, 0, 1, 2)

        self.calculate_button = QPushButton("Calcular Puntaje")
        self.calculate_button.clicked.connect(self.calculate_scores)
        layout.addWidget(self.calculate_button, 4, 0, 1, 2)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text, 5, 0, 1, 2)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.file1_path = None
        self.file2_path = None

    def load_file1(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de Variables y Pesos", "", "Excel Files (*.xlsx *.xls)")
        if file_name:
            self.file1_path = file_name
            self.preview_file(file_name, self.file1_table)

    def load_file2(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de Ideas de Proyectos", "", "Excel Files (*.xlsx *.xls)")
        if file_name:
            self.file2_path = file_name
            self.preview_file(file_name, self.file2_table)

    def preview_file(self, file_path, table_widget):
        try:
            df = pd.read_excel(file_path)
            table_widget.setColumnCount(len(df.columns))
            table_widget.setRowCount(len(df))
            table_widget.setHorizontalHeaderLabels(df.columns)
            for row in range(len(df)):
                for col in range(len(df.columns)):
                    item = QTableWidgetItem(str(df.iat[row, col]))
                    table_widget.setItem(row, col, item)
            table_widget.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al cargar el archivo: {e}")

    def process_evaluation(self):
        if not self.file1_path or not self.file2_path:
            QMessageBox.warning(self, "Advertencia", "Debe cargar ambos archivos antes de procesar la evaluación.")
            return

        try:
            variables_df = pd.read_excel(self.file1_path)
            ideas_df = pd.read_excel(self.file2_path)

            if 'Variable' not in variables_df.columns or 'Peso (%)' not in variables_df.columns:
                raise ValueError("El archivo de Variables y Pesos debe tener las columnas 'Variable' y 'Peso (%)'.")
            if 'Idea' not in ideas_df.columns:
                raise ValueError("El archivo de Ideas de Proyectos debe tener una columna 'Idea'.")

            num_variables = len(variables_df)
            num_ideas = len(ideas_df)
            self.evaluation_table.setColumnCount(num_variables + 1)
            self.evaluation_table.setRowCount(num_ideas)

            headers = ['Idea'] + [f"{v} ({p}%)" for v, p in zip(variables_df['Variable'], variables_df['Peso (%)'])]
            self.evaluation_table.setHorizontalHeaderLabels(headers)

            for row in range(num_ideas):
                self.evaluation_table.setItem(row, 0, QTableWidgetItem(ideas_df['Idea'][row]))
                for col in range(1, num_variables + 1):
                    self.evaluation_table.setItem(row, col, QTableWidgetItem())

            self.evaluation_table.resizeColumnsToContents()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error durante el procesamiento: {e}")

    def calculate_scores(self):
        if not self.file1_path or not self.file2_path:
            QMessageBox.warning(self, "Advertencia", "Debe cargar ambos archivos antes de calcular los puntajes.")
            return

        try:
            variables_df = pd.read_excel(self.file1_path)
            num_variables = len(variables_df)
            num_ideas = self.evaluation_table.rowCount()

            scores = []

            for row in range(num_ideas):
                total_score = 0
                idea = self.evaluation_table.item(row, 0).text()
                for col in range(1, num_variables + 1):
                    score_item = self.evaluation_table.item(row, col)
                    if score_item:
                        try:
                            score = float(score_item.text())
                            weight = variables_df['Peso (%)'][col - 1]
                            total_score += score * (weight / 100)
                        except ValueError:
                            continue

                scores.append((idea, total_score))

            scores.sort(key=lambda x: x[1], reverse=True)

            result_text = "Resultados de la Evaluación (de mayor a menor):\n\n"
            for idea, score in scores:
                result_text += f"{idea}: {score:.2f}\n"

            self.result_text.setText(result_text)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error durante el cálculo de puntajes: {e}")
