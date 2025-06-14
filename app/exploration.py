import streamlit as st
import pandas as pd
import numpy as np
from function import *
from css import *
from streamlit_echarts import st_echarts
from streamlit_extras.stylable_container import stylable_container
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static


@st.cache_resource
def exploration(df, full_df):
    df = df
    df_selection = df
    
    full_df = full_df
    # Les KPIs=====================================================================
    
    # Chiffres brutes et Carte---------------------------------------------------------
    
    # Nombre total de clients uniques
    nombre_total_clients = df["Customer ID"].nunique()
    # Âge minimal
    age_min = df['Age'].min()
    # Âge maximal
    age_max = df['Age'].max()
    # Âge moyen (arrondi à l'entier)
    age_moyen = int(df['Age'].mean())
    # Ancienneté moyenne (Tenure), en mois
    anciennete_moyenne = int(df['Tenure in Months'].mean())
    # Revenu total généré par tous les clients
    revenu_total = int(df['Total Revenue'].sum())
    # Revenu minimal
    revenu_min = int(df['Total Revenue'].min())
    # Revenu max
    revenu_max = int(df['Total Revenue'].max())
    
    col = st.columns([1,4,1])
    with col[0]:
        write_metric_card("Nombre total de clients", nombre_total_clients, "#022C86", "#0B54F1")
        write_metric_card("Âge moyen", age_moyen, "#72055C", "#F812CB")
        write_metric_card("Ancienneté moyenne", f"{anciennete_moyenne} mois", "#0A5F63", "#12E3EF")
    with col[1]:
        with stylable_container_function('1999'):
            st.markdown("""
                <h2 style='color: #1914B3; font-weight: bold; text-align: center;'>
                    Carte géographique des clients
                </h2>
            """, unsafe_allow_html=True)
            customer_map = create_folium_map(df)
            folium_static(customer_map, width=1300, height=450)
    with col[2]:
        write_metric_card("Revenu total généré", f"{revenu_total} €", "#185207", "#3FE611")
        write_metric_card("Revenu minimal généré", f"{revenu_min} €", "#960909", "#F63434")
        write_metric_card("Revenu maximal généré", f"{revenu_max} €", "#185207", "#3FE611")

    
    # Pourcentages-----------------------------------------------
    # % dans le revenu total
    revenu_selection = df_selection['Total Revenue'].sum()
    revenu_total = full_df['Total Revenue'].sum()
    pourcent_revenu_selection = int(revenu_selection / revenu_total * 100)
    # % services tel
    pourcent_phone_service = int(df[df['Phone Service'] == 'Yes'].shape[0] / df.shape[0] * 100)
    # % internet
    pourcent_internet = int(df[df['Internet Service'] != 'No'].shape[0] / df.shape[0] * 100)
    # Liste des services premium
    premium_services = [
        "Online Security", "Online Backup", "Device Protection Plan",
        "Premium Tech Support", "Streaming TV", "Streaming Movies"
    ]
    # Création d'un masque booléen : au moins un service premium activé
    mask_premium = df[premium_services].eq('Yes').any(axis=1)
    # Calcul du pourcentage
    pourcent_premium = int(mask_premium.sum() / df.shape[0] * 100)

    
    princ_col = st.columns(1)
    
    with princ_col[0]:
        with stylable_container_function('0'):
            st.markdown(f"""<div class="card-title" style="text-align: center; font-size: 22px; font-weight: bold; color:#1914B3">{get_text("Keys Rate")}</div> """,  unsafe_allow_html=True)
            cols = st.columns(4)
            with cols[0]:
                st_echarts(options=option_jauge("Pourcentage dans le revenu total", pourcent_revenu_selection), key="0")
            with cols[1]:
                st_echarts(options=option_jauge("Pourcentage utilisant des services telephoniques", pourcent_phone_service), key="1") 
            with cols[2]:
                st_echarts(options=option_jauge("Pourcentage utilisant les services internet", pourcent_internet), key="2")
            with cols[3]:
                st_echarts(options=option_jauge("Pourcentage utilisant au moins un service premium", pourcent_premium), key="3")
                        
    cols1 = st.columns(4)
    with cols1[0]:
        with stylable_container_function('1'):
            st.plotly_chart(plot_sex_donut_plotly(df, titre_graphique="Répartition des clients par sexe"), use_container_width=True)
    with cols1[1]:
        with stylable_container_function('2'):
            plot_age_pyramid(df)
    with cols1[2]:  # Adaptez à votre layout
        with stylable_container_function('3'):
            st.plotly_chart(plot_dependents_horizontal_percent(df), use_container_width=True)
    with cols1[3]:  # Adaptez à votre layout
        with stylable_container_function('4'):
            st.plotly_chart(plot_married_donut_plotly(df, titre_graphique="Répartition des clients par statut marital"), use_container_width=True)
    
    cols2 = st.columns(4)
    with cols2[0]:
        with stylable_container_function('5'):
            st.plotly_chart(plot_contract_distribution(df), use_container_width=True)
    with cols2[1]:
        with stylable_container_function('6'):
            st.plotly_chart(plot_referrals_distribution(df), use_container_width=True)
    with cols2[2]:
        with stylable_container_function('7'):
            st.plotly_chart(plot_payment_methods(df), use_container_width=True)
    with cols2[3]:
        with stylable_container_function('8'):
            st.plotly_chart(plot_offer_distribution(df), use_container_width=True)
    
    cols3 = st.columns(1)
    with cols3[0]:
        with stylable_container_function('9'):
            # Utilisation dans votre app
            generate_enhanced_wordcloud(df)
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
          
    return