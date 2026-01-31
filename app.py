import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title= "Dashboard Vendas de Jogos em 3 Regiões",
    page_icon= "https://www.flaticon.com/free-icon/dashboard_11279858",
    layout="wide"
)
st.title("🎮 Dashboard de Vendas de Jogos")

st.markdown("""
Este dashboard apresenta uma análise exploratória das vendas globais de videogames,
com foco em top jogos, plataformas, editoras e distribuição regional.

📌 As vendas regionais são agregadas (América do Norte, União Europeia e Japão).
""")

df_limpo = pd.read_csv("df_limpo.csv")

st.sidebar.header("Filtros")

# Filtros aplicados
anos = st.sidebar.multiselect(
    "Ano de lançamento",
    options=sorted(df_limpo["Ano"].dropna().unique()),
    default=sorted(df_limpo["Ano"].dropna().unique())
)

plataformas = st.sidebar.multiselect(
    "Plataforma",
    options=sorted(df_limpo["Plataforma"].unique()),
    default=sorted(df_limpo["Plataforma"].unique())
)

generos = st.sidebar.multiselect(
    "Gênero",
    options=sorted(df_limpo["Genero"].unique()),
    default=sorted(df_limpo["Genero"].unique())
)

editoras = st.sidebar.multiselect(
    "Editora",
    options=sorted(df_limpo["Editoras_preenchidas"].unique()),
    default=sorted(df_limpo["Editoras_preenchidas"].unique())
)

if not anos or not plataformas or not generos or not editoras:
    st.warning("Selecione pelo menos uma opção em cada filtro para visualizar os dados.")
    st.stop()

#Filtragem
df_filtrado = df_limpo[
    (df_limpo['Ano'].isin(anos))&
    (df_limpo["Genero"].isin(generos)) &
    (df_limpo['Editoras_preenchidas'].isin(editoras))&
    (df_limpo['Plataforma'].isin(plataformas))
]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total de Jogos",
    df_filtrado["Nome"].nunique()
)

col2.metric(
    "Vendas Globais (milhões)",
    round(df_filtrado["Vendas_Globais"].sum(), 2)
)

col3.metric(
    "Editoras",
    df_filtrado["Editoras_preenchidas"].nunique()
)

top_jogos = (
    df_filtrado
    .sort_values("Vendas_Globais", ascending=False)
    .head(10)
)

fig_top = px.bar(
    top_jogos,
    x="Vendas_Globais",
    y="Nome",
    orientation="h",
    title="🏆 Top 10 Jogos Mais Vendidos",
    labels={"Vendas_Globais": "Vendas (milhões)"}
)

fig_top.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig_top, use_container_width=True)

vendas_plataforma = (
    df_filtrado
    .groupby("Plataforma")["Vendas_Globais"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_plat = px.bar(
    vendas_plataforma,
    x="Plataforma",
    y="Vendas_Globais",
    title="🎮 Vendas por Plataforma",
    labels={"Vendas_Globais": "Vendas (milhões)"}
)

st.plotly_chart(fig_plat, use_container_width=True)

vendas_editora = (
    df_filtrado
    .groupby("Editoras_preenchidas")["Vendas_Globais"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_editora = px.bar(
    vendas_editora,
    x="Vendas_Globais",
    y="Editoras_preenchidas",
    orientation="h",
    title="🏢 Top 10 Editoras",
    labels={"Vendas_Globais": "Vendas (milhões)", "Editoras_preenchidas": "Editora"}
)

st.plotly_chart(fig_editora, use_container_width=True)

vendas_regiao = pd.DataFrame({
    "Regiao": ["América do Norte", "União Europeia", "Japão"],
    "Vendas": [
        df_filtrado["Vendas_America_Norte"].sum(),
        df_filtrado["Vendas_Uniao_Europeia"].sum(),
        df_filtrado["Vendas_Japao"].sum()
    ]
})

fig_pizza = px.pie(
    vendas_regiao,
    values="Vendas",
    names="Regiao",
    hole=0.45,
    title="🌍 Participação de Vendas por Região"
)

fig_pizza.update_traces(
    textinfo="percent+label",
    pull=[0.05, 0.05, 0.1]
)

fig_pizza.update_layout(
    legend_title_text="Região",
    title_x=0.5
)

st.plotly_chart(fig_pizza, use_container_width=True)


if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop()
