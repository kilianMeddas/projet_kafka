# Importing necessary libraries
import streamlit as st
import pandas as pd
import altair as alt
import requests
from datetime import datetime
import base64
import random
from streamlit_autorefresh import st_autorefresh

# Initial configuration of the Streamlit page
st.set_page_config(page_title="Dashboard de Noël", layout="wide")

# Initialize the page state if not already set
if "page" not in st.session_state:
    st.session_state.page = "intro"

# Auto-refresh for the dashboard page
if st.session_state.page == "dashboard":
    count = st_autorefresh(interval=1000, limit=None, key="datarefresh")

# Caching API data retrieval with a time-to-live (TTL) of 10 seconds
# Refresh every 10 secondes
@st.cache_data(ttl=10)
def get_data_from_api():
    response = requests.get("http://stats_api:8000/stats")# URL de l'API
    return response.json()

# Fetching API data
api_data = get_data_from_api()

# Extracting data from API
total_revenue = api_data.get("total revenue", 0)
average_revenue = api_data.get("average revenue", 0)

# Preparing a DataFrame for product revenue analysis
revenue_by_product_df = pd.DataFrame(
    list(api_data.get("revenue by product", {}).items()),
    columns=["Produit", "Revenu (€)"]
).sort_values(by="Revenu (€)", ascending=False).reset_index(drop=True)

# Adding a percentage of total revenue if the DataFrame is not empty
if not revenue_by_product_df.empty:
    revenue_by_product_df["% du Revenu Total"] = (
        revenue_by_product_df["Revenu (€)"] / total_revenue * 100
    )

# Assigning Christmas themed colors to products
noel_colors = [
    "#FF0000", "#FF4500", "#FFD700", "#ADFF2F", "#32CD32", "#006400",
    "#008000", "#7CFC00", "#FFFF00", "#FF6347"
]

revenue_by_product_df["Couleur"] = noel_colors[:len(revenue_by_product_df)]


# Function to encode an image in base64 format
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return encoded


if st.session_state.page == "intro":
    # Encoding the background image
    image_base64 = get_base64_image("noelbd.jpg")

    # Generating CSS for falling snowflakes animation
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

    # Applying styles to the intro page
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{image_base64}");
            background-size: cover;
            background-position: center;
            font-family: 'Arial', sans-serif;
            color: white;
            overflow: hidden;
        }}

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

        {snowflake_css}

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

        .stButton {{
            text-align: center;
        }}
        </style>
        """, unsafe_allow_html=True
    )

    # Generating snowflake HTML
    snowflakes_html = '<div class="snowflakes" aria-hidden="true">'
    for _ in range(50):
        snowflakes_html += '<div class="snowflake">❄</div>'
    snowflakes_html += '</div>'

    st.markdown(snowflakes_html, unsafe_allow_html=True)


    # Adding welcome message and button to switch to the dashboard
    st.markdown(
        """
        <div class="container">
            <h1 class="title">Bienvenue sur le Tableau de Bord Festif de votre Boutique de Noël</h1>
            <p class="subtitle">Découvrez nos analyses de données interactives.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Button to navigate to the dashboard
    if st.button("Accéder au Dashboard"):
        st.session_state.page = "dashboard"
        st.experimental_rerun()

elif st.session_state.page == "dashboard":
    st.title("🎄 Dashboard des Ventes de Noël 🎄")

    # Applying styles to the dashboard page
    st.markdown(
        """
        <style>
        .stApp {{
            background-color: #FDF6E3;
            color: #333333;
        }}

        h1 {{
            color: #B22222;
        }}

        h2, h3 {{
            color: #006400;
        }}

        p {{
            color: #333333;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Displaying main informations
    st.header("Statistiques Clés")
    col1, col2 = st.columns(2)
    col1.metric("Revenu Total (€)", f"{total_revenue:,.0f} €", delta_color="off")
    col2.metric("Revenu Moyen (€)", f"{average_revenue:,.0f} €", delta_color="off")

    # Sidebar legend for products with their associated colors
    st.sidebar.title("🌺 Légende des Produits")
    for product, color in zip(revenue_by_product_df["Produit"], revenue_by_product_df["Couleur"]):
        # Display each product with its corresponding color in the sidebar
        st.sidebar.markdown(f"<span style='color:{color};'>■</span> {product}", unsafe_allow_html=True)

    # Check if the DataFrame for product revenue is not empty
    if not revenue_by_product_df.empty:
 
        # Subheader for revenue by product chart
        st.subheader("🎁 Revenu par Produit")

        # Create different chart using Altair
        chart1 = alt.Chart(revenue_by_product_df).mark_bar().encode(
            x=alt.X("Revenu (€):Q", title="Revenu (€)"),
            y=alt.Y("Produit:N", sort=alt.EncodingSortField(field='Revenu (€)', order='descending'), title="Produit"),
            color=alt.Color("Couleur:N", scale=None),
            tooltip=["Produit:N", "Revenu (€):Q"]
        ).properties(
            height=400
        )

        text_chart1 = alt.Chart(revenue_by_product_df).mark_text(align='left', dx=3).encode(
            x=alt.X("Revenu (€):Q"),
            y=alt.Y("Produit:N"),
            text=alt.Text("Revenu (€):Q", format="# ##0 €")
        )

        chart1_combined = chart1 + text_chart1
        st.altair_chart(chart1_combined, use_container_width=True)

        st.subheader("📊 Contribution de chaque Produit au Revenu Total (%)")
        chart2_updated = alt.Chart(revenue_by_product_df).mark_bar().encode(
            x=alt.X("Produit:N", sort="-y", title="Produit", axis=alt.Axis(labelAngle=-90)),
            y=alt.Y("% du Revenu Total:Q", title="% du Revenu Total"),
            color=alt.Color("% du Revenu Total:Q", scale=alt.Scale(domain=[revenue_by_product_df["% du Revenu Total"].min(), revenue_by_product_df["% du Revenu Total"].max()], range=['red', 'yellow', 'green'])),
            tooltip=["Produit:N", "% du Revenu Total:Q"]
        ).properties(
            height=400
        )

        text = alt.Chart(revenue_by_product_df).mark_text(dy=-10, color='black').encode(
            x=alt.X("Produit:N", sort="-y"),
            y=alt.Y("% du Revenu Total:Q"),
            text=alt.Text("% du Revenu Total:Q", format="0.2f%%")
        )

        chart2_combined = chart2_updated + text
        st.altair_chart(chart2_combined, use_container_width=True)

    st.subheader("🍰 Répartition des Revenus par Catégorie")
    categories = {
        "Décorations": ["Boules de Noël", "Guirlandes lumineuses", "Ornements de table", "Sapins de Noël"],
        "Accessoires Festifs": ["Chaussettes de Noël", "Tasses festives"],
        "Cadeaux et Emballages": ["Bougies parfumées", "Calendriers de l'Avent", "Peluches de Noël", "Papiers cadeaux"]
    }

    revenue_by_category = {}
    for category, products in categories.items():
        revenue_by_category[category] = revenue_by_product_df[revenue_by_product_df["Produit"].isin(products)]["Revenu (€)"].sum()

    revenue_by_category_df = pd.DataFrame(list(revenue_by_category.items()), columns=["Catégorie", "Revenu (€)"])
    revenue_by_category_df["Produits Inclus"] = revenue_by_category_df["Catégorie"].apply(lambda x: ', '.join(categories[x]))

    if not revenue_by_category_df.empty:
        christmas_pie_colors = ["#FFB6C1", "#FF69B4", "#8B0000"]  # Adding new Christmas-themed colors

        venn_chart = alt.Chart(revenue_by_category_df).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Revenu (€)", type="quantitative"),
            color=alt.Color(field="Catégorie", type="nominal", scale=alt.Scale(range=christmas_pie_colors)),
            tooltip=["Catégorie:N", "Revenu (€):Q", "Produits Inclus:N"]
        ).properties(
            height=400
        )

        st.altair_chart(venn_chart, use_container_width=True)

    st.subheader("🗓️ Revenus et Ventes par Jour")
    revenue_by_day = api_data.get("revenue by day and month", {}).get("by day", {})
    sales_by_day = api_data.get("sales by day and month", [])[0]

    if revenue_by_day and sales_by_day:
        daily_sales_df = pd.DataFrame(
            [{"Date": date, "Revenu (€)": revenue, "Ventes": sales_by_day.get(date, 0)} for date, revenue in revenue_by_day.items()]
        )
        daily_sales_df["Date"] = pd.to_datetime(daily_sales_df["Date"])

        if not daily_sales_df.empty:
            daily_revenue_chart = alt.Chart(daily_sales_df).mark_bar().encode(
                x=alt.X("Date:T", title="Date"),
                y=alt.Y("Revenu (€):Q", title="Revenu (€)"),
                color=alt.value("#FF4500"),
                tooltip=["Date:T", "Revenu (€):Q"]
            ).properties(
                height=400
            )

            daily_sales_chart = alt.Chart(daily_sales_df).mark_bar().encode(
                x=alt.X("Date:T", title="Date"),
                y=alt.Y("Ventes:Q", title="Ventes"),
                color=alt.value("#1E90FF"),
                tooltip=["Date:T", "Ventes:Q"]
            ).properties(
                height=400
            )

            st.altair_chart(daily_revenue_chart, use_container_width=True)
            st.altair_chart(daily_sales_chart, use_container_width=True)
    else:
        # Warning message if no daily data is available
        st.warning("Les données de ventes journalières ne sont pas disponibles, impossible de générer les graphiques.")

    if st.sidebar.button("⬅️ Retour à l'accueil"):
        st.session_state.page = "intro"
        st.experimental_rerun()
