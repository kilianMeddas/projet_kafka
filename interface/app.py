import streamlit as st
import pandas as pd
import altair as alt
import requests
from datetime import datetime
import base64
import random
from streamlit_autorefresh import st_autorefresh  # Importer st_autorefresh

# Configuration de la page
st.set_page_config(page_title="Dashboard de Noël", layout="wide")

# Rafraîchissement automatique toutes les 10 secondes (10000 millisecondes)
count = st_autorefresh(interval=10000, limit=None, key="datarefresh")

# Fonction pour récupérer les données depuis l'API (sans mise en cache)
def get_data_from_api():
    response = requests.get("http://stats_api:8000/stats")# URL de l'API
    data = response.json()
    return data

# Charger les données
api_data = get_data_from_api()

# Préparer les données
total_revenue = api_data["total revenue"]
average_revenue = api_data["average revenue"]

# Revenu par produit
revenue_by_product_df = pd.DataFrame(
    list(api_data["revenue by product"].items()),
    columns=["Produit", "Revenu (€)"]
)

# Ventes par jour
sales_by_day_data = api_data["sales by day and month"][0]  # Premier élément est 'by day'
sales_by_day_df = pd.DataFrame(
    list(sales_by_day_data.items()),
    columns=["Date", "Nombre de Ventes"]
)
sales_by_day_df["Date"] = pd.to_datetime(sales_by_day_df["Date"])

# Revenu par jour
revenue_by_day_data = api_data["revenue by day and month"]["by day"]
revenue_by_day_df = pd.DataFrame(
    list(revenue_by_day_data.items()),
    columns=["Date", "Revenu (€)"]
)
revenue_by_day_df["Date"] = pd.to_datetime(revenue_by_day_df["Date"])

# Fonction pour charger l'image et la convertir en base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return encoded

# Gestion de l'état pour basculer entre les pages
if "page" not in st.session_state:
    st.session_state.page = "intro"

# **Page d'introduction festive**
if st.session_state.page == "intro":
    image_base64 = get_base64_image("noelbd.jpg")  # Assurez-vous que le chemin est correct

    # Générer le CSS pour les flocons de neige avec des propriétés aléatoires
    snowflake_css = ''
    for i in range(1, 51):
        left = random.randint(0, 100)
        animation_duration = random.uniform(5, 15)
        animation_delay = random.uniform(0, 10)
        size = random.uniform(0.8, 1.5)
        opacity = random.uniform(0.5, 1)
        snowflake_css += f'''
        .snowflake:nth-child({i}) {{
            left: {left}%;
            animation-duration: {animation_duration}s;
            animation-delay: {animation_delay}s;
            font-size: {size}rem;
            opacity: {opacity};
        }}
        '''

    # CSS et HTML pour l'effet de Noël
    st.markdown(
        f"""
        <style>
        /* Fond d'écran */
        .stApp {{
            background-image: url("data:image/jpg;base64,{image_base64}");
            background-size: cover;
            background-position: center;
            font-family: 'Arial', sans-serif;
            color: white;
            overflow: hidden;
        }}

        /* Flocons de neige */
        .snowflakes {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 9999;
        }}

        .snowflake {{
            position: absolute;
            top: -10px;
            color: white;
            animation: fall infinite linear;
        }}

        @keyframes fall {{
            0% {{
                transform: translateY(-10px);
                opacity: 1;
            }}
            100% {{
                transform: translateY(100vh);
                opacity: 0.7;
            }}
        }}

        /* Ajouter le CSS des flocons avec des propriétés aléatoires */
        {snowflake_css}

        /* Centrer le contenu */
        .container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            height: 90vh;
            text-align: center;
            padding-top: 15vh;
            z-index: 1;
            position: relative;
        }}

        .title {{
            font-size: 4rem;
            font-weight: bold;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        }}

        .subtitle {{
            font-size: 1.8rem;
            margin-bottom: 1rem;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.7);
        }}

        /* Bouton stylé */
        .stButton > button {{
            background-color: #FF4500;
            border: none;
            color: white;
            padding: 15px 30px;
            font-size: 1.5rem;
            border-radius: 10px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }}

        .stButton > button:hover {{
            background-color: #FF6347;
            transform: scale(1.05);
        }}

        /* Centrer le bouton */
        .stButton {{
            text-align: center;
        }}
        </style>
        """, unsafe_allow_html=True
    )

    # Générer le HTML des flocons de neige
    snowflakes_html = '<div class="snowflakes" aria-hidden="true">'
    for _ in range(50):
        snowflakes_html += '<div class="snowflake">❄</div>'
    snowflakes_html += '</div>'

    # Afficher les flocons de neige
    st.markdown(snowflakes_html, unsafe_allow_html=True)

    # HTML pour le contenu
    st.markdown(
        """
        <div class="container">
            <h1 class="title">Bienvenue sur le Tableau de Bord Festif de votre Boutique de Noël</h1>
            <p class="subtitle">Découvrez nos analyses de données interactives.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Bouton pour accéder au Dashboard
    if st.button("Accéder au Dashboard"):
        st.session_state.page = "dashboard"
        st.experimental_rerun()

# **Dashboard principal**
elif st.session_state.page == "dashboard":
    # Titre
    st.title("🎄 Dashboard des Ventes de Noël 🎄")

    # CSS pour personnaliser le dashboard
    st.markdown(
        """
        <style>
        /* Couleur de fond du dashboard */
        .stApp {
            background-color: #FDF6E3;
            color: #333333;
        }

        /* Titre principal */
        h1 {
            color: #B22222; /* Rouge bordeaux */
        }

        /* Sous-titres */
        h2, h3 {
            color: #006400; /* Vert sapin */
        }

        /* Texte */
        p {
            color: #333333;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Statistiques clés
    st.header("Statistiques Clés")
    col1, col2 = st.columns(2)
    col1.metric("Revenu Total (€)", f"{total_revenue:,.2f}", delta_color="off")
    col2.metric("Revenu Moyen (€)", f"{average_revenue:,.2f}", delta_color="off")

    # Graphique 1 : Revenu par produit (barres rouges)
    st.subheader("🎁 Revenu par Produit")
    bars = alt.Chart(revenue_by_product_df).mark_bar().encode(
        x=alt.X("Revenu (€):Q", title="Revenu (€)"),
        y=alt.Y("Produit:N", sort='-x', title="Produit"),
        color=alt.value("#B22222"),  # Rouge bordeaux
        tooltip=["Produit:N", "Revenu (€):Q"]
    )
    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=5,  # Décalage horizontal
        fontSize=12,
        color='black'
    ).encode(
        text=alt.Text("Revenu (€):Q", format=",.0f")
    )
    chart1 = (bars + text).properties(
        height=400,
        width=700
    )
    st.altair_chart(chart1, use_container_width=True)

    # Graphique 2 : Répartition du revenu par produit (camembert)
    st.subheader("🧁 Répartition du Revenu par Produit")
    noel_colors = ["#B22222", "#006400", "#FFD700", "#8B0000", "#228B22", "#FFA500", "#FF6347", "#2E8B57", "#CD5C5C", "#ADFF2F"]
    chart2 = alt.Chart(revenue_by_product_df).mark_arc(innerRadius=50).encode(
        theta=alt.Theta("Revenu (€):Q", stack=True),
        color=alt.Color("Produit:N", scale=alt.Scale(domain=revenue_by_product_df["Produit"], range=noel_colors), legend=None),
        tooltip=["Produit:N", "Revenu (€):Q"]
    ).properties(
        height=400,
        width=400
    )
    st.altair_chart(chart2, use_container_width=True)

    # Ajouter une légende visuelle
    st.markdown("#### Légende des Produits")
    legend_html = "<div style='display: flex; flex-wrap: wrap; gap: 10px;'>"
    for product, color in zip(revenue_by_product_df["Produit"], noel_colors):
        legend_html += f"<div style='display: flex; align-items: center; gap: 5px;'>"
        legend_html += f"<div style='width: 20px; height: 20px; background-color: {color}; border-radius: 50%;'></div>"
        legend_html += f"<span>{product}</span>"
        legend_html += "</div>"
    legend_html += "</div>"
    st.markdown(legend_html, unsafe_allow_html=True)

    # Graphique 3 : Revenu par jour (ligne)
    st.subheader("📅 Revenu par Jour")
    if not revenue_by_day_df.empty:
        chart3 = alt.Chart(revenue_by_day_df).mark_line(point=True).encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("Revenu (€):Q", title="Revenu (€)"),
            color=alt.value("#006400"),  # Vert sapin
            tooltip=["Date:T", "Revenu (€):Q"]
        ).properties(
            height=400
        )
        st.altair_chart(chart3, use_container_width=True)
    else:
        st.info("Données insuffisantes pour afficher le revenu par jour.")

    # Graphique 4 : Nombre de ventes par jour (barres)
    st.subheader("📈 Nombre de Ventes par Jour")
    if not sales_by_day_df.empty:
        chart4 = alt.Chart(sales_by_day_df).mark_bar().encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("Nombre de Ventes:Q", title="Nombre de Ventes"),
            color=alt.value("#DAA520"),  # Doré
            tooltip=["Date:T", "Nombre de Ventes:Q"]
        ).properties(
            height=400
        )
        st.altair_chart(chart4, use_container_width=True)
    else:
        st.info("Données insuffisantes pour afficher le nombre de ventes par jour.")

    # Graphique 5 : Revenu moyen par vente
    st.subheader("💰 Revenu Moyen par Vente")
    average_revenue_df = pd.DataFrame({
        "Type": ["Revenu Moyen"],
        "Revenu (€)": [average_revenue]
    })
    chart5 = alt.Chart(average_revenue_df).mark_bar().encode(
        x=alt.X("Type:N", title=""),
        y=alt.Y("Revenu (€):Q", title="Revenu (€)"),
        color=alt.value("#B22222"),  # Rouge bordeaux
        tooltip=["Revenu (€):Q"]
    ).properties(
        height=200
    )
    st.altair_chart(chart5, use_container_width=True)

    # Bouton pour revenir à la page d'intro
    if st.sidebar.button("⬅️ Retour à l'accueil"):
        st.session_state.page = "intro"
        st.experimental_rerun()
