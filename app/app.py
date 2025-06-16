import streamlit as st

# Configuration de la page------------------------------------------------------

st.set_page_config(
    page_title="California Telecom", 
    page_icon="📞", 
    layout="wide",
    initial_sidebar_state="expanded"
) 



import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
from function import *
from css import *
from exploration import *
from churn_prediction import *
from dashboard import *
from main import *



# Application des styles=====================================================================================================
styles_css()

# Logo de l'appli-------------------------------------------------------------

st.sidebar.image(
        "app/logo.png",
        caption="CALIFORNIA TELECOM"
    )

# Filtres====================================================================================================================

def sidebar_filters(df):
    st.sidebar.markdown("""
        <div class="dashboard-header animate-fade-in">
            <h3 style="font-weight: bold;">Filtres</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # 1. Filtre par catégorie de client (Gros, Moyen, Petit)
    # Création de la catégorie client
    df['Client_Category'] = pd.cut(
        df['Monthly_Revenue'],
        bins=[0, 30, 100, float('inf')],
        labels=['Petit', 'Moyen', 'Gros'],
        right=False
    )
    
    client_category_filter = st.sidebar.multiselect(
        "Catégorie de client", 
        options=['Petit', 'Moyen', 'Gros'], 
        default=['Petit', 'Moyen', 'Gros'],
        help="Catégorie basée sur les revenus mensuels"
    )
    
    # 2. Filtre par statut de churn (Customer Status)
    churn_statuses = df['Customer Status'].unique()
    churn_filter = st.sidebar.multiselect(
        "Statut du client", 
        options=sorted(churn_statuses), 
        default=sorted(churn_statuses),
        help="Choisir parmi: Churned, Stayed, Joined"
    )
    
    # 3. Filtre par ville (City) - version liste déroulante
    cities = ['Toutes les villes'] + sorted(df['City'].unique().tolist())
    selected_city = st.sidebar.selectbox(
        "Ville",
        options=cities,
        index=0,  # "Toutes les villes" sélectionnée par défaut
        help="Sélectionnez une ville spécifique"
    )
    
    # Application des filtres
    filtered_df = df[
        (df['Client_Category'].isin(client_category_filter)) &
        (df['Customer Status'].isin(churn_filter))
    ]
    
    # Filtrage supplémentaire par ville si une ville spécifique est sélectionnée
    if selected_city != 'Toutes les villes':
        filtered_df = filtered_df[filtered_df['City'] == selected_city]
    
       
    return filtered_df

def main():
    st.markdown(
            f"""
            <div class="metric-box" style="background-color: white; height : 120px">
                <div class="metric-title" style="text-align: center; font-size: 60px; font-weight: bold; color: #1914B3;">{get_text("CHURN ANALYSIS DASHBOARD")}
                        </div>
    </div>
            
            """,
            unsafe_allow_html=True
        )  
    
    # Base de donnees----------------------------------------------------------------------------
    df = pd.read_csv("data/data_clean_churn1.csv", header=0, sep=";")
    # Définir les bornes des tranches d’âge
    bornes = list(range(15, 85, 5))  # de 15 à 80 (80 exclusif à droite dans pd.cut)

    # Créer des labels pour chaque tranche
    labels = [f"{i}-{i+4}" for i in bornes[:-1]]  # ex : 15-19, 20-24, ...

    # Créer la nouvelle colonne 'Tranche âge'
    df['Tranche âge'] = pd.cut(df['Age'], bins=bornes, labels=labels, right=False, include_lowest=True)
    
    filter_df = sidebar_filters(df)

    # Pages de navigation---------------------------------------------------------------------
        
    page = option_menu( # voir help du package streamlit_option_menu
        menu_title=None,
        options=["Analyse des clients", "Churn Prediction"],
        icons=["globe", "search"],
        menu_icon=None,
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important"},
            "icon": {"font-size": "1.3rem"},
            "nav-link": {"font-size": "1.2em", "text-align": "center", "margin": "0px"},
            "nav-link-selected": {"background-color": "#1914B3"},
        }
    )
    
    st.markdown("---")

    # Affichage des pages------------------------------------
    
    if page == "Churn Prediction":
        churn_prediction(filter_df)
    else:
        exploration(filter_df, df)
    
    # Insérer l'appel à cette fonction sur la page d'accueil
    afficher_guide_utilisateur()
    
    # Pied de page
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>ENSAE 2024/2025- Projet Machine Learning 2<br>
            - Fama
            - Josette
            - Kpakou
            - Larry
            </p>
            <img src="https://ensai.fr/wp-content/uploads/2019/07/ENSAE-Dakar-logo.png" alt="Image du produit" style="width:5%; height:auto; border-radius: 8px;">
    </div>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__": 
    main()        
