# Sistema de Evaluación de Proyectos 📝

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat&logo=python)](https://www.python.org/downloads/) 
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green?style=flat&logo=qt)](https://riverbankcomputing.com/software/pyqt/intro)
[![Pandas](https://img.shields.io/badge/Data-Pandas-orange?style=flat&logo=pandas)](https://pandas.pydata.org/)

Este sistema permite cargar y procesar dos archivos Excel: uno con variables para calificar proyectos y sus pesos porcentuales, y otro con una lista de ideas de proyectos. El sistema pondera las ideas y muestra un ranking de acuerdo a los puntajes obtenidos.

## Características

- **Carga de dos archivos Excel.**
- **Previsualización de los datos cargados.**
- **Procesamiento de evaluación para ponderar ideas de proyectos.**
- **Interfaz gráfica usando PyQt6.**
- **Visualización de los resultados en una matriz de evaluación.**

## Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instaladas las siguientes dependencias:

- 🐍 Python 3.9 o superior
- 🪟 PyQt6
- 🧮 Pandas
- 📂 OpenPyXL

Puedes instalar las dependencias con el siguiente comando:

```bash
pip install -r requirements.txt
```

 
## Instalación

Clona el repositorio:
```bash
git clone https://github.com/tu_usuario/nombre_del_proyecto.git
```

Ejecuta la aplicación:
```bash
python src/main.py
```