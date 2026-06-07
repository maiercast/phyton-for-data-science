import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Censo Uruguay 2023 – Hogares",
    page_icon="🏠",
    layout="wide",
)

# ── Carga de datos ───────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
    import gdown
    url = "https://drive.google.com/uc?id=14hoGUYsbePQ2MqDmusHlCt1J8O9H3wFY"
    gdown.download(url, "censo_hogares_2023_limpio.csv", quiet=False)
    df = pd.read_csv("censo_hogares_2023_limpio.csv", low_memory=False)
    return df
except Exception as e:
        st.error(f"Error cargando datos: {e}")
        st.stop()

df = load_data()

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏠 Censo Uruguay 2023")
    st.markdown(
        "Explorá los datos de **hogares** del Censo Nacional de Población, "
        "Hogares y Viviendas 2023. Usá los filtros para segmentar el análisis."
    )
    st.markdown("---")
    st.markdown("### 🎛️ Filtros")

    # Filtro departamento
    deps = sorted(df["departamento_nombre"].dropna().unique())
    dep_sel = st.multiselect(
        "Departamento",
        options=deps,
        default=deps,
        help="Seleccioná uno o más departamentos.",
    )

    # Filtro área
    areas = sorted(df["area_nombre"].dropna().unique())
    area_sel = st.multiselect("Área", options=areas, default=areas)

    # Slider: personas en el hogar
    p_min = int(df["personas_en_hogar"].min())
    p_max = int(df["personas_en_hogar"].clip(upper=15).max())
    rango_personas = st.slider(
        "Personas en el hogar",
        min_value=p_min,
        max_value=p_max,
        value=(p_min, p_max),
        help="Filtrá hogares según la cantidad de personas que los integran.",
    )

    # Slider: índice de confort
    c_min = int(df["indice_confort"].min())
    c_max = int(df["indice_confort"].max())
    rango_confort = st.slider(
        "Índice de confort (0–8 bienes)",
        min_value=c_min,
        max_value=c_max,
        value=(c_min, c_max),
        help="Suma de bienes del hogar: heladera, internet, computadora, streaming, etc.",
    )

    st.markdown("---")
    st.caption("Fuente: INE Uruguay – Censo 2023")

# ── FILTRADO ─────────────────────────────────────────────────────────────────
mask = (
    df["departamento_nombre"].isin(dep_sel)
    & df["area_nombre"].isin(area_sel)
    & df["personas_en_hogar"].between(rango_personas[0], rango_personas[1])
    & df["indice_confort"].between(rango_confort[0], rango_confort[1])
)
dff = df[mask].copy()

# ── TÍTULO ───────────────────────────────────────────────────────────────────
st.title("🏠 Análisis Interactivo de Hogares – Censo Uruguay 2023")
st.markdown(
    f"Mostrando **{len(dff):,}** hogares de un total de **{len(df):,}** "
    f"({len(dff)/len(df)*100:.1f}% del total)."
)
st.markdown("---")

# ── MÉTRICAS RÁPIDAS ─────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Hogares filtrados", f"{len(dff):,}")
col2.metric("Promedio personas/hogar", f"{dff['personas_en_hogar'].mean():.2f}")
col3.metric("Mediana habitaciones", f"{dff['habitaciones_totales'].median():.0f}")
col4.metric("Confort promedio", f"{dff['indice_confort'].mean():.2f} / 8")

st.markdown("---")

# ── RESUMEN DESCRIPTIVO ──────────────────────────────────────────────────────
st.subheader("📊 Resumen Descriptivo")

cols_desc = ["personas_en_hogar", "habitaciones_totales", "habitaciones_dormir", "indice_confort", "cant_autos"]
stats_df = dff[cols_desc].describe(percentiles=[0.25, 0.5, 0.75]).T
stats_df["rango"] = stats_df["max"] - stats_df["min"]
stats_df = stats_df.rename(columns={
    "count": "n", "mean": "media", "std": "desv_std",
    "min": "mínimo", "25%": "Q1", "50%": "mediana", "75%": "Q3", "max": "máximo"
})
stats_df.index = [
    "Personas en hogar", "Habitaciones totales",
    "Habitaciones p/ dormir", "Índice de confort", "Automóviles"
]

st.dataframe(
    stats_df[["n", "media", "desv_std", "mínimo", "Q1", "mediana", "Q3", "máximo", "rango"]]
    .style.format({
        "n": "{:,.0f}", "media": "{:.2f}", "desv_std": "{:.2f}",
        "mínimo": "{:.0f}", "Q1": "{:.1f}", "mediana": "{:.1f}",
        "Q3": "{:.1f}", "máximo": "{:.0f}", "rango": "{:.0f}",
    }),
    use_container_width=True,
)

st.markdown("---")

# ── GRÁFICOS ─────────────────────────────────────────────────────────────────
st.subheader("📈 Visualizaciones")

tab1, tab2, tab3 = st.tabs(["Distribución del Target", "Dispersión", "Por Departamento"])

# ── TAB 1: Histograma de personas por hogar (variable objetivo) ──────────────
with tab1:
    st.markdown("#### Distribución de Personas por Hogar")
    st.markdown(
        "Histograma de la variable objetivo: **cantidad de personas por hogar**. "
        "Refleja el tamaño familiar típico en los hogares seleccionados."
    )

    personas_plot = dff["personas_en_hogar"].clip(upper=15)
    fig_hist = px.histogram(
        personas_plot,
        nbins=15,
        labels={"value": "Personas en el hogar", "count": "Cantidad de hogares"},
        title="Distribución de Personas por Hogar (filtrado)",
        color_discrete_sequence=["#1976D2"],
    )
    fig_hist.update_layout(
        xaxis_title="Personas en el hogar",
        yaxis_title="Cantidad de hogares",
        showlegend=False,
        bargap=0.05,
    )
    fig_hist.add_vline(
        x=dff["personas_en_hogar"].median(),
        line_dash="dash",
        line_color="red",
        annotation_text=f"Mediana: {dff['personas_en_hogar'].median():.1f}",
        annotation_position="top right",
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# ── TAB 2: Scatter – Habitaciones vs Índice de Confort ───────────────────────
with tab2:
    st.markdown("#### Habitaciones Totales vs Índice de Confort")
    st.markdown(
        "Relación entre el **tamaño del hogar** (habitaciones totales) y su "
        "**nivel de equipamiento** (índice de confort). Se espera una correlación "
        "positiva: hogares más grandes tienden a tener más bienes."
    )

    # Sample para no sobrecargar el gráfico
    sample_size = min(30_000, len(dff))
    dff_sample = dff.sample(n=sample_size, random_state=42)

    fig_scatter = px.scatter(
        dff_sample,
        x="habitaciones_totales",
        y="indice_confort",
        color="region_nombre",
        opacity=0.4,
        size_max=6,
        labels={
            "habitaciones_totales": "Habitaciones totales",
            "indice_confort": "Índice de confort (0–8)",
            "region_nombre": "Región",
        },
        title=f"Habitaciones vs Confort – muestra de {sample_size:,} hogares",
        trendline="ols",
        trendline_scope="overall",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_scatter.update_layout(
        xaxis=dict(range=[0, 15]),
        yaxis=dict(range=[-0.5, 8.5]),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Correlación
    corr = dff[["habitaciones_totales", "indice_confort"]].dropna().corr().iloc[0, 1]
    st.info(f"**Correlación de Pearson** entre habitaciones y confort: **{corr:.3f}**")

# ── TAB 3: Barras por departamento ───────────────────────────────────────────
with tab3:
    st.markdown("#### Indicadores Promedio por Departamento")

    metrica = st.selectbox(
        "Seleccioná la métrica a visualizar:",
        options={
            "personas_en_hogar": "Personas promedio por hogar",
            "indice_confort": "Índice de confort promedio",
            "habitaciones_totales": "Habitaciones totales promedio",
        },
        format_func=lambda x: {
            "personas_en_hogar": "Personas promedio por hogar",
            "indice_confort": "Índice de confort promedio",
            "habitaciones_totales": "Habitaciones totales promedio",
        }[x],
    )

    dep_stats = (
        dff.groupby("departamento_nombre")[metrica]
        .mean()
        .sort_values(ascending=True)
        .reset_index()
    )

    label_map = {
        "personas_en_hogar": "Personas promedio",
        "indice_confort": "Índice de confort promedio",
        "habitaciones_totales": "Habitaciones promedio",
    }

    fig_bar = px.bar(
        dep_stats,
        x=metrica,
        y="departamento_nombre",
        orientation="h",
        labels={
            metrica: label_map[metrica],
            "departamento_nombre": "Departamento",
        },
        title=f"{label_map[metrica]} por Departamento",
        color=metrica,
        color_continuous_scale="Blues",
    )
    fig_bar.update_layout(coloraxis_showscale=False, height=600)
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")
st.caption("Proyecto de Análisis Interactivo de Datos | Censo Uruguay 2023 – INE")
