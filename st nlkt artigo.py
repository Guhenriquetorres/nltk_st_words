import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np

# 🔥 Configurar o Streamlit
st.set_page_config(page_title="Dashboard", layout="wide")

# 🔥 Função para definir a cor das fontes
def set_font_color(color="#D3D3D3"):
    """Define globalmente a cor das fontes no Streamlit."""
    st.markdown(f"""
    <style>
    body {{
        background-color: black;
        color: {color};
    }}
    [data-testid="stAppViewContainer"] {{
        background-color: black;
    }}
    [data-testid="stHeader"] {{
        background-color: black;
    }}
    [data-testid="stSidebar"] {{
        background-color: black;
    }}
    .stDataFrame {{
        background-color: black !important;
        color: {color} !important;
    }}
    h1, h2, h3, h4, h5, h6, p, label, span {{
        color: {color} !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# Chamar a função para definir a cor da fonte
set_font_color("#1d4851")  # Você pode alterar essa cor facilmente

# Carregar os dados diretamente do pickle
df = pd.read_pickle(r"C:\Users\guhen\programas\NLTK\NLTKfrequencia_palavras.pkl")

# Criar o dashboard no Streamlit
st.markdown("<h1 style='text-align: center;'> Dashboard de Frequência de Palavras</h1>", unsafe_allow_html=True)

# Criar um layout com três colunas
col1, col2 = st.columns([2,2])

# **Gráfico de barras interativo no modo escuro**
with col1:
     # **Divisão interna para melhor organização**
    stat_col, wordcloud_col = st.columns([1, 1])  

    st.subheader("Gráfico de Frequência de Palavras")
    fig = px.bar(
        df, 
        x="Palavra", 
        y="Frequência", 
        title="Frequência das Palavras", 
        text="Frequência", 
        color="Frequência",
        color_continuous_scale=["#1d4851", "#00ffff"],  # 🔥 Cores: ciano escuro -> ciano claro
        template="plotly_dark"
    )
    fig.update_layout(
        title_font=dict(size=20, color="#1d4851"), 
        xaxis=dict(title="Palavras", tickangle=-45),
        yaxis=dict(title="Frequência"),
        plot_bgcolor="black",  
        paper_bgcolor="black",
    )
    st.plotly_chart(fig, use_container_width=False)

 # **Divisão interna para melhor organização**
    stat_col, wordcloud_col = st.columns([1, 2])  # Divide a área da estatística e da nuvem de palavras

# **🌎 Nuvem de Palavras com fundo preto**

    st.subheader("Nuvem de Palavras")

    if df.empty:
        st.error("O DataFrame está vazio! Verifique os dados.")
    else:
        freq_dict = dict(zip(df["Palavra"], df["Frequência"]))

        # Gerar a nuvem de palavras com fundo preto
        wordcloud = WordCloud(
            width=800, height=400,
            background_color="black",
            colormap="cool",
            contour_color="#black",
            contour_width=2,
        ).generate_from_frequencies(freq_dict)

        fig, ax = plt.subplots(figsize=(20, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.set_facecolor("black")
        ax.axis("off")
        st.pyplot(fig)



# **🥧 Gráfico de Pizza das palavras mais frequentes**
with col2:
    stat_col, wordcloud_col = st.columns([2, 2])  # Divide a área da estatística e da nuvem de palavras
    st.subheader("Gráfico de Pizza")
    
    df_top10 = df.nlargest(10, "Frequência")
    
    fig_pizza = px.pie(df_top10, 
                       names="Palavra", 
                       values="Frequência", 
                       title="Top 10 Palavras Mais Frequentes",
                       color_discrete_sequence=px.colors.sequential.Teal)
    fig_pizza.update_layout(
        title_font=dict(size=20, color="#1d4851"),
        paper_bgcolor="black",
        font_color="white"
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

    stat_col, wordcloud_col = st.columns([2, 2])  # Divide a área da estatística e da nuvem de palavras
    # 📊 **Análise Estatística da Frequência das Palavras**
    st.subheader("📊 Análise Estatística")

    # Calcular estatísticas
    media = np.mean(df["Frequência"])
    mediana = np.median(df["Frequência"])
    moda_valor = df["Frequência"].mode()[0]
    desvio_padrao = np.std(df["Frequência"])

    # Identificar as palavras associadas a cada estatística
    palavra_media = df.iloc[(df["Frequência"] - media).abs().idxmin()]["Palavra"]
    palavra_mediana = df.iloc[(df["Frequência"] - mediana).abs().idxmin()]["Palavra"]
    palavras_moda = df[df["Frequência"] == moda_valor]["Palavra"].tolist()


    # 📊 **Exibir os resultados com as palavras associadas (AUMENTANDO A FONTE)**
    st.markdown(f"""
        <p style="font-size:25px; font-weight:bold;">
        📈 <b>Média da Frequência:</b> `{media:.2f}` → Palavra mais próxima: <span style="color:#00ffff;">{palavra_media}</span>  <br>
        📊 <b>Mediana:</b> `{mediana}` → Palavra mais próxima: <span style="color:#00ffff;">{palavra_mediana}</span>  <br>
        🎯 <b>Moda:</b> `{moda_valor}` → Palavras: <span style="color:#00ffff;">{', '.join(palavras_moda)}</span>  <br>
        </p>
        """, unsafe_allow_html=True)



# **📜 Tabela de Dados com fundo preto**
st.subheader("Tabela de Dados")
st.dataframe(df.style.set_properties(**{
    "background-color": "black", 
    "color": "#D3D3D3"
}))
