# Proyecto

## Análisis Interactivo de Datos con Streamlit


**Objetivo:** Desarrollar una aplicación interactiva en **Streamlit** que cargue, analice y visualice un conjunto de datos estándar, aplicando conceptos de manipulación de datos con **Pandas** e integración de *widgets* interactivos.



## Dataset Seleccionado: Boston House Prices

Utilizaremos el *dataset* de precios de viviendas de California, un conjunto de datos clásico de regresión (que reemplazó al de Boston)

* **Librería de Origen:** `sklearn.datasets`
* **Nombre de la Función:** `sklearn.datasets.fetch_california_housing()`
* **Fuente:** Este dataset fue creado a partir de datos del censo de 1990 en California.
* **Documentación:** https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html

### Descripción del Dataset

El *dataset* de California contiene datos sobre la mediana de ingresos, la edad de las casas y otras métricas geográficas y socioeconómicas a nivel de grupo de bloques (la unidad geográfica más pequeña para la que la Oficina del Censo de EE. UU. publica datos de muestra).

| Característica | Descripción |
| :--- | :--- |
| HouseAge | Mediana de la edad de las casas dentro del grupo de bloques. |
| AveRooms | Promedio de habitaciones por hogar.|
| AveBedrms | Promedio de dormitorios por hogar. |
| Population | Población del grupo de bloques. |
| Latitude | Latitud del centro geográfico del grupo de bloques. |
| Longitude | Longitud del centro geográfico del grupo de bloques. |
| MedHouseVal (Target) | Mediana del valor de la vivienda (en cientos de miles de dólares). |

---

## Actividades Requeridas del Proyecto

El proyecto se dividirá en cuatro fases: 
- Carga y Preparación de Datos (Pandas), 
- Análisis Descriptivo Interactivo (Streamlit), y 
- Visualización Dinámica.
- Despliegue en la Nube

### Fase 1: Carga y Preparación de Datos con Pandas

Deberás cargar el *dataset* desde `sklearn.datasets` y convertirlo en un único **Pandas DataFrame** llamado `df_california`.

1.  **Carga y Estructura:** Cargar las características (`data`) y la variable objetivo (`target`) utilizando `fetch_california_housing()`. Combinar ambas en un único `df_california`, asegurando que las columnas tengan los nombres correctos proporcionados por el dataset (`feature_names`).
2.  **Preparación Inicial (Pandas):**
    * Verificar si hay valores faltantes.
    * Mostrar las **primeras 5 filas** y el **tipo de dato** de cada columna utilizando `st.dataframe()` y `st.write()` en Streamlit.

### Fase 2: Análisis Descriptivo Interactivo (Streamlit Widgets)

Esta fase se centra en usar los *widgets* de Streamlit para permitir al usuario explorar los datos.

1.  **Sidebar de Control (`st.sidebar`):**
    * Implementar un `st.sidebar.markdown()` para el título y descripción de los filtros.
2.  **Filtro por Estilo de Vivienda (`st.slider`):**
    * Crear un **slider** que permita al usuario seleccionar un rango de la Edad Mediana de la Casa (HouseAge).
    * Rango: El rango del slider debe ir desde el mínimo hasta el máximo de la columna HouseAge.
    * Filtrar el DataFrame para incluir solo las viviendas cuya edad mediana caiga dentro del rango seleccionado por el usuario.
3.  **Filtro de Vecindario (`st.checkbox`):**
    * Implementar un campo de entrada numérico (`st.number_input`) que permita al usuario establecer la Latitud Mínima.
    * Filtrar el DataFrame para incluir solo los grupos de bloques con una Latitude mayor o igual al valor ingresado.
4.  **Resumen Descriptivo:**
    * Mostrar la mediana y el rango (Máximo - Mínimo) del valor de la vivienda MedHouseVal del DataFrame resultante después de aplicar todos los filtros.

### Fase 3: Visualización Dinámica

Deberás mostrar la relación entre las variables utilizando gráficos que se actualicen automáticamente con los filtros de la Fase 2.

1.  **Gráfico de Distribución del Target (`st.pyplot` o `st.plotly_chart`):**
    * Crear un **histograma** de la variable objetivo (**MedHouseVal**) utilizando una librería externa (como Matplotlib o Plotly).
    * **Requisito:** El gráfico debe reflejar la distribución de los datos **después** de aplicar los filtros del usuario.
2.  **Gráfico de Dispersión (Regresión):**
    * Crear Crear un gráfico de dispersión (scatter plot) que muestre la relación entre la Mediana de Ingresos (MedInc) (eje X) y el Valor Mediano de la Vivienda (MedHouseVal) (eje Y).
    * **Requisito:** Este gráfico también debe actualizarse con los datos filtrados y ser lo suficientemente informativo (ej. incluir etiquetas y un título).
3.  ** Opcional - Mapa Geográfico** (Streamlit Nativo o Plotly):
    * Utilizar la función nativa de Streamlit (st.map()) o un gráfico de dispersión de Plotly con st.plotly_chart() para mapear los grupos de bloques filtrados usando las columnas Latitude y Longitude.
    * Requisito: El mapa debe mostrar la distribución geográfica de las viviendas filtradas por el usuario.

---

## Fase 4: Despliegue en la Nube

Deberás preparar tu proyecto para el despliegue.

1.  **Git/GitHub:** Crear un **repositorio público** en GitHub a partir de este template.

2.  **Estructura de Carpeta:**
    * `app.py` (código de Streamlit).
    * `notebooks/practice.ipynb` en este archivo puedes realizar un análisis previo del dataset propuesto
    * `requirements.txt` (listado de dependencias: `streamlit`, `pandas`, `scikit-learn`, `matplotlib` o `plotly`).

3.  **Despliegue:** Desplegar la aplicación final utilizando **Streamlit Community Cloud** (share.streamlit.io).

Deberás entregar: 
- el **enlace a la aplicación desplegada** y 
- el **enlace al repositorio de GitHub**.
