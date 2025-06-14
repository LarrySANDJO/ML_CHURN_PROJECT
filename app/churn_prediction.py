import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
from function import *
from streamlit_extras.colored_header import colored_header


def churn_prediction(df):
    df = df

    # Style CSS personnalisé
    st.markdown(f"""
        <style>
            .stForm {{
                border: 2px solid #1914B3;
                border-radius: 10px;
                padding: 20px;
                background-color: #F8F9FA;
            }}
            .stButton>button {{
                background-color: #1914B3;
                color: white;
                border-radius: 5px;
                padding: 10px 24px;
                font-weight: bold;
                border: none;
                width: 100%;
                transition: all 0.3s ease;
            }}
            .stButton>button:hover {{
                background-color: #0A04AA;
                transform: scale(1.02);
            }}
            .stSelectbox, .stNumberInput, .stTextInput {{
                border: 1px solid #1914B3 !important;
                border-radius: 5px !important;
            }}
            .st-bb {{ background-color: white; }}
            .st-at {{ background-color: #1914B3; }}
            div[data-baseweb="select"] > div {{
                border-color: #1914B3 !important;
            }}
        </style>
    """, unsafe_allow_html=True)

    # Header stylisé
    colored_header(
        label="🔮 Prédiction de Churn Client",
        description="Renseignez les informations du client pour évaluer le risque de départ",
        color_name="blue-70"
    )

    # Formulaire de prédiction
    with st.form("prediction_form"):
        cols = st.columns(2)
        
        with cols[0]:
            st.subheader("📊 Données Démographiques")
            age = st.number_input("Âge", min_value=18, max_value=100, value=45)
            gender = st.selectbox("Genre", ["Homme", "Femme"])
            married = st.selectbox("Statut Marital", ["Marié(e)", "Célibataire", "Divorcé(e)"])
            dependents = st.number_input("Nombre de Personnes à Charge", min_value=0, max_value=10)
        
        with cols[1]:
            st.subheader("📱 Données de Consommation")
            monthly_charge = st.number_input("Revenu Mensuel ($)", min_value=0, value=50)
            tenure = st.number_input("Ancienneté (mois)", min_value=1, value=12)
            contract = st.selectbox("Type de Contrat", ["Mensuel", "Annuel", "Biannuel"])
            internet_service = st.selectbox("Service Internet", ["DSL", "Fibre Optique", "Aucun"])
        
        st.subheader("💎 Options Supplémentaires")
        add_ons = st.multiselect(
            "Services Optionnels",
            options=["Sécurité en ligne", "Sauvegarde en ligne", "Support technique premium", "Protection appareil"]
        )
        
        # Bouton de soumission
        submit_button = st.form_submit_button("Prédire le Risque de Churn", type="primary")

    # Résultats de prédiction (exemple)
    if submit_button:
        st.success("Analyse terminée avec succès !")
        
        # Exemple de résultat
        with st.expander("📈 Résultats de la Prédiction", expanded=True):
            cols_result = st.columns([1, 3])
            
            with cols_result[0]:
                st.metric("Probabilité de Churn", "72%", delta_color="inverse")
                st.metric("Catégorie Risque", "Élevé", delta="+15% vs moyenne")
            
            with cols_result[1]:
                st.progress(72)
                st.caption("Recommandation : Offre de fidélisation recommandée (réduction de 15% pour 12 mois)")
                
            # Graphique exemple (remplacer par votre vrai modèle)
            chart_data = {
                "Facteurs": ["Ancienneté", "Revenu", "Contrat", "Services"],
                "Importance": [45, 30, 15, 10]
            }
            st.bar_chart(chart_data, x="Facteurs", y="Importance", color="#1914B3")
