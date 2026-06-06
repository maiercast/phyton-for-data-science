# Análisis Interactivo de Hogares – Censo Uruguay 2023

Aplicación Streamlit para el análisis exploratorio e interactivo del dataset de **hogares** del Censo Nacional de Población, Hogares y Viviendas 2023 (INE Uruguay).

## 🗂️ Estructura del proyecto

```
├── app.py                          # Aplicación Streamlit
├── requirements.txt                # Dependencias
├── notebooks/
│   └── practice.ipynb              # EDA en Jupyter Notebook (Fase 1)
└── data/
    ├── raw/
    │   ├── hogares_ext_26_02.csv
    │   ├── Diccionario de variables 2023.xlsx
    │   ├── Localidades_Censo2023.xlsx
    │   └── Departamentos_Censo2023.xlsx
    └── processed/
        └── censo_hogares_2023_limpio.csv
```

## 🚀 Correr localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📊 Dataset

- **Fuente:** Instituto Nacional de Estadística (INE) – Uruguay
- **Censo:** 2023
- **Registros:** ~1.255.000 hogares
- **Variables clave:** tenencia de vivienda, habitaciones, acceso a servicios, bienes del hogar, personas por hogar

## 🔗 Despliegue

La aplicación está desplegada en [Streamlit Community Cloud](https://share.streamlit.io).
