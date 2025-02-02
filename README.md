# Reconocimiento en Tiempo Real de Dígitos Escritos

Este repositorio contiene la implementación de un sistema de reconocimiento de dígitos en tiempo real utilizando técnicas de visión por computadora y aprendizaje automático. El proyecto aprovecha un clasificador de máquina de vectores de soporte (SVM) y un análisis de componentes principales (PCA) para un reconocimiento de dígitos eficiente y preciso.

## Autores
- Chiara Valenzuela.
- Mitchell Bermín.
  
## Tabla de Contenidos

- [Descripción general](#Descripción-general)
- [Características](#Características)
- [Instalación](#Instalación)
- [Uso](#Uso)
- [Estructura del Proyecto](#Estructura-del-Proyecto)
- [Contribuciones](#Contribuciones)

## Descripción general

El proyecto tiene como objetivo desarrollar un sistema que reconozca dígitos escritos a mano en tiempo real mediante una cámara web. Utiliza el conjunto de datos MNIST para entrenar el modelo SVM, aplica PCA para la reducción de dimensionalidad y procesa transmisión de video en vivo para detectar y reconocer dígitos.

## Características

- Reconocimiento de dígitos en tiempo real mediante una cámara web
- Alta precisión lograda con el clasificador SVM
- Procesamiento eficiente con PCA para reducción de dimensionalidad
- Interfaz sencilla e intuitiva para reconocimiento de dígitos en vivo

## Instalación

1. Clonar el repositorio:
   ```sh
   git clone https://github.com/ChiaraVL/ReconocimientoNo.git
   cd ReconocimientoNo
   ```

2. Cree y active un entorno virtual (opcional pero recomendado):
   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows usar `venv\Scripts\activate`
   ```

3. Instalar las dependencias requeridas:
   ```sh
   pip install -r requirements.txt
   ```

## Uso

Por favor verifique que las rutas coincidan con las usadas.

1. **Entrenamiento del Modelo:**

   Ejecute el script de entrenamiento para entrenar el modelo SVM y guarde los componentes necesarios:
   ```sh
   python train/model.py
   python train/model_pca.py
   ```

2. **Reconocimiento en Tiempo Real:**

   Ejecute el script de reconocimiento para iniciar el reconocimiento de dígitos en tiempo real usando su cámara web:
   ```sh
   python test/final_recognition.py
   ```

## Estructura del Proyecto

```
ReconocimientoNo/
│
├── documents/                   # En la carpeta encontrará los documentos de investigación
│
├── train/
│   └── model.py                 # Script para entrenar el modelo SVM
│   └── model_pca.py             # Script para entrenar el modelo SVM y aplicar PCA
│   └── model_optimize.py        # Script para entrenar el modelo SVM, aumento de datos y aplicar PCA automático 
│
├── test/
│   └── recognize.py             # Script para reconocimiento de dígitos en tiempo real
│   └── recognize_pca.py         # Script para reconocimiento de dígitos en tiempo real con PCA
│   └── final_recognition.py     # Script para reconocimiento de dígitos y de trazos en tiempo real
│   └── recognize_canva.py       # Script para reconocimiento de trazos de dígitos en tiempo real
│   └── soft_margin.py           # Script para calculo de márgenes de la SVC
│
├── pytest/
│   └── test_recognition.py      # Script de pruebas unitarias y de integración
│
├── models/                      # En la carpeta encontrará los modelos entrenados
│
├── graphs/                      # En la carpeta encontrará los gráficos calculados
|
├── README.md
├── requirements.txt             # Lista de dependencias
└── .gitignore                     # Archivo git ignore
```

## Contribuciones

!Las contribuciones son bienvenidas!
