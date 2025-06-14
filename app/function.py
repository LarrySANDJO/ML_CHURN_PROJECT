import streamlit as st
import pandas as pd
import numpy as np
from css import *
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from streamlit_extras.stylable_container import stylable_container
import plotly.express as px
import folium
from folium.plugins import MarkerCluster, Fullscreen
from wordcloud import WordCloud
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


@st.cache_resource
def get_text(key):
    if 'language' not in st.session_state:
        return key
    if 'get_text' not in st.session_state:
        return key
    return st.session_state.get_text(key)


def afficher_guide_utilisateur():
    # CSS personnalisé pour l'expander
    st.markdown("""
    <style>
    .streamlit-expanderHeader {
        background-color: #1914B3 !important;
        color: white !important;
        font-weight: bold;
        font-size: 20 !important;
        border-radius: 5px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.expander("Guide d'utilisation complet"):
        st.markdown("""
        # Guide Utilisateur - Application d'Analyse Client et Prédiction de Churn

        Cette application permet d'analyser le comportement des clients et de prédire leur risque de résiliation (churn).

        ## Pages de l'Application

        ### 1. Page d'Analyse des Profils Clients

        Cette page fournit une analyse détaillée de la base client avec des visualisations interactives.

        **Indicateurs Clés (KPIs):**
        - **Nombre total de clients** : Volume de clients dans la sélection
        - **Âge moyen** : Âge moyen des clients
        - **Ancienneté moyenne** : Durée moyenne de relation avec les clients (en mois)
        - **Revenu total généré** : Chiffre d'affaires global
        - **Revenu minimal/maximal** : Fourchettes de revenus clients

        **Cartographie:**
        - Carte géographique interactive montrant la répartition géographique des clients

        **Indicateurs de Pourcentage:**
        - **Pourcentage dans le revenu total** : Contribution des clients sélectionnés
        - **Services téléphoniques** : Taux d'adoption des services voix
        - **Services internet** : Taux de pénétration des services data
        - **Services premium** : Proportion utilisant au moins un service optionnel

        **Visualisations Analytiques:**
        1. **Démographie Client**
        - Répartition par sexe (diagramme en donut)
        - Pyramide des âges
        - Statut marital
        - Nombre de personnes à charge

        2. **Comportement Client**
        - Types de contrats souscrits
        - Nombre de parrainages (références)
        - Méthodes de paiement préférées
        - Offres souscrites

        3. **Nuage de mots** des caractéristiques clients

        ### 2. Page de Prédiction de Churn

        Cette page permet de prédire le risque de départ des clients via deux méthodes:

        **A. Formulaire de Prédiction Individuelle**

        Sections du formulaire:
        1. **Identité du client** :
        - Informations personnelles (ID, sexe, âge, situation familiale)
        - Localisation géographique (ville, code postal, coordonnées)

        2. **Services souscrits** :
        - Ancienneté (en mois)
        - Offre commerciale
        - Services téléphoniques (détails des appels longue distance)
        - Services internet (type, consommation data)

        3. **Services optionnels** (si internet activé):
        - Sécurité en ligne
        - Backup cloud
        - Support technique premium
        - Services de streaming

        4. **Facturation** :
        - Type de contrat
        - Facturation dématérialisée
        - Mode de paiement
        - Détails des charges mensuelles/totales

        Après soumission, l'application affiche:
        - Probabilité de churn (en %)
        - Recommandation (action requise ou simple surveillance)
        - Détails techniques de la prédiction

        **B. Prédiction par Lot (CSV)**

        Fonctionnalités:
        - Téléversement d'un fichier CSV contenant les données clients
        - Prévisualisation des données
        - Lancement de l'analyse batch
        - Résultats téléchargeables incluant:
          * Probabilités de churn pour chaque client
          * Prédictions binaires (1=churn, 0=non-churn)
        - Visualisation du taux de churn global
        - Histogramme des probabilités

        ## Fonctionnalités Avancées

        - **Filtres interactifs** : Permettent d'affiner les analyses
        - **Design responsive** : Adapté à tous les écrans
        - **Visualisations interactives** : Zoom, survol pour détails
        - **Export des données** : Possibilité de télécharger les résultats

        ## Conseils d'Utilisation

        1. Pour l'analyse individuelle, complétez tous les champs obligatoires (marqués *)
        2. Pour les analyses segmentées, utilisez les filtres latéraux
        3. Exportez les résultats pour un reporting externe
        4. Surveillez particulièrement les clients avec >60% de risque
        5. Priorisez les actions sur les segments à haut risque identifiés
        """)
        
      
def write_metric_card(text, value, color1, color2):
    st.markdown(f"""
    <div class="metric-box " style="background: linear-gradient(135deg, white, white)";>
        <p><strong >{get_text(text)}</strong></p>
        <h1>{value}</h1>
    </div>
    """, unsafe_allow_html=True)
    

def option_jauge(text, value):
    return {
        "tooltip": {"formatter": '{a} <br/>{b} : {c}%'},
         "series": [
            {"name": "Progression",
             "type": "gauge",
                "startAngle": 180,
                "endAngle": 0,
                "radius": "90%",
                "itemStyle": {
                    "color": "#1914B3",
                    "shadowColor": "rgba(0,138,255,0.45)",
                    "shadowBlur": 10,
                    "shadowOffsetX": 2,
                    "shadowOffsetY": 2
                    },
                    "progress": {
                        "show": True,
                        "roundCap": True,
                        "width": 10
                    },
                    "pointer": {
                        "length": "60%",
                        "width": 3,
                        "offsetCenter": [0, "5%"]
                    },
                    "detail": {
                        "valueAnimation": True,
                        "formatter": "{value}%",
                        "backgroundColor": "#1914B3",
                        "color": "white",
                        "width": "100%",
                        "lineHeight": 25,
                        "height": 16,
                        "borderRadius": 188,
                        "offsetCenter": [0, "40%"],
                        "fontSize": 18
                    },
                    "data": [{
                        "value": value,  # Example value
                        "name": get_text(text),  # Label for the value"Eligibility Rate"
                    }]
                }
            ]
        }
    
# Stylable

def stylable_container_function(cle):
    return stylable_container(
                    key=cle,
                    css_styles=f"""
                        {{
                        width : 100%;
                        border: 1px solid #c0c0c0;
                        border-radius: 10px;
                        flex-direction: column;
                        background-color: #f8f9fa;
                        box-shadow: 0px 4px 6px  2px rgba(0, 0, 0, 0.8);
                        }}
                        
                        .card-title {{
                                font-weight: bold;
                                margin: 0px;
                                padding: 0px;
                                font-size: 1em;
                                text-align: center;
                                color: #8a2be2;  # Light purple color
                            }}
                    """ )
    
# Répartition genre

def plot_sex_donut_plotly(df, emoji="👫", titre_graphique="", height=500):
    # Comptage
    gender_counts = df['Gender'].value_counts()
    labels = gender_counts.index
    values = gender_counts.values

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=['#1914B3', "#A52271"]),
        textinfo='label+percent',
        insidetextorientation='radial',
        textfont_size=18
    )])

    fig.update_layout(
        title=dict(
            text=titre_graphique,
            font=dict(size=16, color='#1914B3', family='Arial Black'),
            x=0.5,
            xanchor='center',
            y=0.95,  # Titre positionné en haut
            yanchor='top'
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,  # Légende en bas
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=60, b=120, l=20, r=20),  # Grande marge en bas pour descendre le graphique
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(
            text=emoji, 
            x=0.5, 
            y=0.35,  # Position Y de l'emoji descendue
            font_size=60, 
            showarrow=False
        )],
        height=height  # Hauteur totale augmentée
    )
    
    # Ajustement spécifique pour descendre le cercle du donut
    fig.update_traces(
        textposition='inside',
        insidetextorientation='radial',
        domain=dict(y=[0.15, 0.85])  # Descend le cercle principal
    )
    
    return fig


# Pyramide des ages 
def plot_age_pyramid(df, age_col='Age', gender_col='Gender', bin_size=5, height=500):
    # Vérifier les valeurs uniques dans la colonne de genre
    unique_genders = df[gender_col].dropna().unique()

    # Détection automatique des genres à utiliser
    homme_label = "Homme" if "Homme" in unique_genders else "Male"
    femme_label = "Femme" if "Femme" in unique_genders else "Female"

    # Créer les tranches d'âge
    min_age = int(df[age_col].min())
    max_age = int(df[age_col].max())
    bin_edges = np.arange(min_age, max_age + bin_size, bin_size)
    bin_labels = [f"{age}-{age + bin_size - 1}" for age in bin_edges[:-1]]
    df['AgeGroup'] = pd.cut(df[age_col], bins=bin_edges, labels=bin_labels, right=False)

    # Comptage hommes et femmes
    hommes = df[df[gender_col] == homme_label].groupby('AgeGroup').size().reset_index(name='Count')
    femmes = df[df[gender_col] == femme_label].groupby('AgeGroup').size().reset_index(name='Count')

    hommes['Genre'] = 'Hommes'
    femmes['Genre'] = 'Femmes'

    data = pd.concat([hommes, femmes])
    data.loc[data['Genre'] == 'Femmes', 'Count'] *= -1  # Inverser les femmes pour pyramide

    # Création du graphique Plotly
    fig = px.bar(
        data,
        y='AgeGroup',
        x='Count',
        color='Genre',
        orientation='h',
        color_discrete_map={'Hommes': '#1914B3', 'Femmes': '#9F0A6E'},
        labels={'Count': 'Nombre de personnes', 'AgeGroup': 'Âge'}
    )

    fig.update_layout(
        title=dict(
            text="Pyramide des âges par sexe",
            font=dict(size=16, color="#1914B3", family="Arial Black"),
            x=0.5,
            xanchor='center'
        ),
        height=height,
        yaxis=dict(showgrid=True, categoryorder="category ascending"),
        xaxis=dict(title='Nombre de personnes', showgrid=True),
        plot_bgcolor='rgba(0,0,0,0)',
        barmode='overlay',
        bargap=0.1,
        legend=dict(orientation='h', yanchor='bottom', y=1, xanchor='right', x=1),
    )

    st.plotly_chart(fig, use_container_width=True)

   
def plot_dependents_horizontal_percent(df, dependents_col='Number of Dependents', height=500):
    # Calcul des pourcentages
    dependents_pct = (df[dependents_col].value_counts(normalize=True)
                        .sort_index()
                        .mul(100)
                        .round(1)
                        .reset_index())
    
    dependents_pct.columns = ['Number of Dependents', 'Percentage']
    dependents_pct['Number of Dependents'] = dependents_pct['Number of Dependents'].astype(str)
    
    # Création d'un dégradé à partir de #1914B3
    base_color = '#1914B3'
    n_categories = len(dependents_pct)
    color_sequence = [f'rgba(25, 20, 179, {1 - i/(2*n_categories)})' for i in range(n_categories)]
    
    # Création du graphique horizontal
    fig = px.bar(
        dependents_pct,
        y='Number of Dependents',
        x='Percentage',
        orientation='h',
        color='Number of Dependents',
        color_discrete_sequence=color_sequence,
        labels={'Percentage': 'Pourcentage de clients (%)', 'Number of Dependents': 'Personnes à charge'},
        title='Répartition des clients par nombre de personnes à charge (%)'
    )
    
    # Personnalisation avancée
    fig.update_layout(
        height=height,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title=dict(
            text='Répartition par nombre de personnes à charge (%)',
            font=dict(size=16, color='#1914B3', family='Arial Black'),
            x=0.5,
            xanchor='center',
            y=0.95
        ),
        yaxis=dict(
            title='Nombre de personnes à charge',
            categoryorder='total ascending'
        ),
        xaxis=dict(
            title='Pourcentage de clients (%)',
            gridcolor='lightgray',
            range=[0, 100]
        ),
        showlegend=False,
        margin=dict(l=100, r=50, b=80, t=100, pad=10)
    )
    
    # Ajout des étiquettes de pourcentage
    fig.update_traces(
        texttemplate='%{x:.1f}%',
        textposition='outside',
        textfont_size=14,
        marker_line_color='rgba(0,0,0,0.3)',
        marker_line_width=1
    )
    
    return fig


def plot_married_donut_plotly(df, emoji="💍", titre_graphique="", height=500):
    # Comptage
    married_counts = df['Married'].value_counts()
    labels = married_counts.index
    values = married_counts.values

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=['#1914B3', "#A52271"]),  # Vous pouvez changer les couleurs si besoin
        textinfo='label+percent',
        insidetextorientation='radial',
        textfont_size=18
    )])

    fig.update_layout(
        title=dict(
            text=titre_graphique,
            font=dict(size=16, color='#1914B3', family='Arial Black'),
            x=0.5,
            xanchor='center',
            y=0.95,
            yanchor='top'
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=60, b=120, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(
            text=emoji, 
            x=0.5, 
            y=0.35,
            font_size=60, 
            showarrow=False
        )],
        height=height
    )
    
    fig.update_traces(
        textposition='inside',
        insidetextorientation='radial',
        domain=dict(y=[0.15, 0.85])
    )
    
    return fig


def plot_contract_distribution(df, contract_col='Contract', height=500):
    # Préparation des données
    contract_data = df[contract_col].value_counts(normalize=True).mul(100).round(1).reset_index()
    contract_data.columns = ['Contract', 'Percentage']
    
    # Ordre personnalisé des catégories
    contract_order = ['Month-to-Month', 'One Year', 'Two Year']
    contract_data['Contract'] = pd.Categorical(contract_data['Contract'], categories=contract_order, ordered=True)
    contract_data = contract_data.sort_values('Contract')
    
    # Création du donut chart
    fig = px.pie(
        contract_data,
        names='Contract',
        values='Percentage',
        hole=0.5,
        color='Contract',
        color_discrete_map={
            'Month-to-Month': '#9F0A6E',  # Violet
            'One Year': '#1914B3',         # Bleu foncé
            'Two Year': '#00A8E8'          # Bleu clair
        },
        title='Répartition des clients par type de contrat'
    )
    
    # Personnalisation avancée
    fig.update_layout(
        height=height,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title=dict(
            text='Répartition par type de contrat',
            font=dict(size=16, color='#1914B3', family='Arial Black'),
            x=0.5,
            xanchor='center',
            y=0.95
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.2,
            xanchor='center',
            x=0.5
        ),
        margin=dict(t=80, b=80, l=40, r=40),
        annotations=[dict(
            text=f"Total: {len(df)} clients",
            x=0.5,
            y=0.5,
            font_size=14,
            showarrow=False
        )]
    )
    
    # Formatage des labels
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        insidetextorientation='radial',
        marker=dict(line=dict(color='#FFFFFF', width=1)),
        hovertemplate='<b>%{label}</b><br>%{percent} (%{value:.1f}%)<extra></extra>'
    )
    
    return fig



def plot_referrals_distribution(df, referrals_col='Number of Referrals', height=500):
    # Préparation des données
    referrals = df[referrals_col].value_counts().sort_index().reset_index()
    referrals.columns = ['Number of Referrals', 'Count']
    
    # Création d'un histogramme avec courbe de densité
    fig = px.histogram(
        df,
        x=referrals_col,
        nbins=20,
        color_discrete_sequence=['#1914B3'],
        opacity=0.8,
        marginal='rug',  # Affichage des points sous l'histogramme
        title='Distribution du nombre de références par client'
    )
    
    # Personnalisation avancée
    fig.update_layout(
        height=height,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title=dict(
            text='Nombre de clients par références effectuées',
            font=dict(size=16, color='#1914B3', family='Arial Black'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title='Nombre de références',
            gridcolor='lightgray',
            dtick=1  # Affiche tous les entiers sur l'axe X
        ),
        yaxis=dict(
            title='Nombre de clients',
            gridcolor='lightgray'
        ),
        bargap=0.1,
        hovermode='x unified'
    )
    
    # Ajout de la moyenne et médiane
    mean_val = df[referrals_col].mean()
    median_val = df[referrals_col].median()
    
    fig.add_vline(
        x=mean_val, 
        line_dash='dash', 
        line_color='#9F0A6E',
        annotation_text=f'Moyenne: {mean_val:.1f}',
        annotation_position='top'
    )
    
    fig.add_vline(
        x=median_val, 
        line_dash='dot', 
        line_color='#00A8E8',
        annotation_text=f'Médiane: {median_val:.1f}',
        annotation_position='bottom'
    )
    
    # Amélioration des tooltips
    fig.update_traces(
        hovertemplate='<b>%{x} références</b><br>%{y} clients<extra></extra>',
        marker_line_width=1,
        marker_line_color='white'
    )
    
    return fig


def plot_payment_methods(df, payment_col='Payment Method', height=500):
    # Préparation des données
    payment_data = df[payment_col].value_counts(normalize=True).mul(100).round(1).reset_index()
    payment_data.columns = ['Payment Method', 'Percentage']
    
    # Palette de couleurs dégradée à partir de #1914B3
    base_color = '#1914B3'
    color_sequence = [
        '#1914B3',  # Original
        '#4540C7',  # +20% luminosité
        '#716CDB',  # +40% luminosité
        '#9D98EF'   # +60% luminosité
    ]
    
    # Création du graphique barres empilées horizontales
    fig = px.bar(
        payment_data,
        x='Percentage',
        y='Payment Method',
        orientation='h',
        color='Payment Method',
        color_discrete_sequence=color_sequence,
        text='Percentage',
        title='Répartition des méthodes de paiement'
    )
    
    # Personnalisation avancée
    fig.update_layout(
        height=height,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title=dict(
            text='Méthodes de paiement utilisées',
            font=dict(size=18, color='#1914B3', family='Arial Black'),
            x=0.5,
            xanchor='center',
            y=0.95
        ),
        xaxis=dict(
            title='Pourcentage (%)',
            range=[0, 100],
            showgrid=True,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title='',
            categoryorder='total ascending'
        ),
        showlegend=False,
        hovermode='y unified',
        margin=dict(l=100, r=50, b=80, t=100)
    )
    
    # Ajout des étiquettes
    fig.update_traces(
        texttemplate='%{x:.1f}%',
        textposition='outside',
        marker_line_color='rgba(255,255,255,0.8)',
        marker_line_width=1.5,
        width=0.7  # Épaisseur des barres
    )
    
    # Ajout d'une annotation globale
    fig.add_annotation(
        x=0.95,
        y=1.1,
        xref='paper',
        yref='paper',
        text="<span style='color:#1914B3'><b>Méthodes de paiement</b></span>",
        showarrow=False,
        font=dict(size=14)
    )
    
    return fig

def plot_offer_distribution(df, offer_col='Offer', height=500):
    # Préparation des données
    offer_data = df[offer_col].value_counts().reset_index()
    offer_data.columns = ['Offer', 'Count']
    
    # Palette de couleurs dégradée
    base_color = '#1914B3'
    color_sequence = [
        '#1914B3',  # Original
        '#3A35C0', 
        '#5B56CD',
        '#7C77DA',
        '#9D98E7',
        '#BEB9F4'
    ]
    
    # Création du graphique radial
    fig = px.bar_polar(
        offer_data,
        r='Count',
        theta='Offer',
        color='Offer',
        color_discrete_sequence=color_sequence,
        template='plotly_white',
        title='Attractivité des différentes offres'
    )
    
    # Personnalisation avancée
    fig.update_layout(
        height=height,
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(
                visible=True,
                gridcolor='lightgray',
                linewidth=1
            ),
            angularaxis=dict(
                linewidth=2,
                linecolor='#1914B3'
            )
        ),
        title=dict(
            text='Répartition par type d\'offre',
            font=dict(size=20, color='#1914B3', family='Arial Black'),
            x=0.5,
            xanchor='center',
            y=0.95
        ),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.15,
            xanchor='center',
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Solution alternative pour afficher les valeurs
    for i, row in offer_data.iterrows():
        fig.add_annotation(
            x=row['Offer'],
            y=row['Count'],
            text=str(row['Count']),
            showarrow=False,
            font=dict(size=12, color='white'),
            xanchor='center',
            yanchor='middle'
        )
    
    # Ajout d'un cercle central informatif
    fig.add_annotation(
        text=f"Total: {len(df)}<br>clients",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=14, color='#1914B3'),
        align='center'
    )
    
    return fig


def create_folium_map(df):
    # Filtrer les données valides
    valid_df = df.dropna(subset=['Latitude', 'Longitude']).copy()
    
    # Créer la carte avec fond naturel
    m = folium.Map(
        location=[36.7783, -119.4179],
        zoom_start=6,
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri World Imagery'
    )
    
    # Ajouter le contrôle plein écran
    Fullscreen(
        position="topright",
        title="Plein écran",
        title_cancel="Quitter plein écran",
        force_separate_button=True
    ).add_to(m)
    
    # Groupes distincts
    city_labels = folium.FeatureGroup(name='Noms des villes', show=True)
    clients_layer = folium.FeatureGroup(name='Clients', show=True)
    
    # Dictionnaire pour éviter les doublons de villes
    added_cities = set()
    
    # 1. Ajouter les noms de villes
    for idx, row in valid_df.iterrows():
        city = row['City']
        if city not in added_cities:
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                icon=folium.DivIcon(
                    html=f'<div style="font-size: 11pt; font-weight: bold; color: white; text-shadow: 1px 1px 3px #000000">{city}</div>'
                ),
                tooltip=city
            ).add_to(city_labels)
            added_cities.add(city)
    
    # 2. Ajouter les clients avec clustering
    churn_cluster = MarkerCluster(name='Clients perdus').add_to(clients_layer)
    active_cluster = MarkerCluster(name='Clients actifs').add_to(clients_layer)
    
    for idx, row in valid_df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            icon=folium.Icon(
                color='red' if row['Customer Status'] == 'Churned' else 'green',
                icon='user' if row['Customer Status'] == 'Churned' else 'user-check',
                prefix='fa'
            ),
            popup=folium.Popup(
                f"<b>{row['City']}</b><br>"
                f"Client: {row['Customer ID']}<br>"
                f"Statut: {row['Customer Status']}<br>"
                f"Revenu: ${row['Monthly Charge']:.2f}",
                max_width=250
            )
        ).add_to(churn_cluster if row['Customer Status'] == 'Churned' else active_cluster)
    
    # Ajouter les couches à la carte
    city_labels.add_to(m)
    clients_layer.add_to(m)
    
    # Contrôle des calques
    folium.LayerControl(collapsed=False).add_to(m)
    
    return m



def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    # Nettoyage du texte
    text_clean = re.sub(r'[^a-z\s]', '', text.lower())
    # Lemmatisation et suppression stopwords
    words = [lemmatizer.lemmatize(w) for w in text_clean.split() if w not in stop_words and len(w) > 2]
    return " ".join(words)

# Téléchargement des ressources NLP
nltk.download('stopwords')
nltk.download('wordnet')

# Configuration des outils NLP
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    # Nettoyage du texte
    text_clean = re.sub(r'[^a-z\s]', '', text.lower())
    # Lemmatisation et suppression stopwords
    words = [lemmatizer.lemmatize(w) for w in text_clean.split() if w not in stop_words and len(w) > 2]
    return " ".join(words)

def generate_enhanced_wordcloud(filtered_df, height=500):
    # Filtrer et prétraiter les données
    churn_reasons = filtered_df[filtered_df['Customer Status'] == 'Churned']['Churn Reason'].dropna()
    
    if churn_reasons.empty:
        st.warning("Aucune donnée de churn disponible")
        return
    
    # Prétraitement du texte
    processed_text = " ".join(churn_reasons.apply(preprocess_text))
    
    if not processed_text.strip():
        st.warning("Aucun terme significatif après prétraitement")
        return
    
    # Configuration du WordCloud
    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color='white',
        colormap='viridis',
        max_words=150,
        min_font_size=8,
        max_font_size=120,
        collocations=False,
        prefer_horizontal=0.8,
        margin=0,
        scale=2,
        random_state=42
    ).generate(processed_text)
    
    # Affichage Streamlit
    st.markdown("""
    <h2 style='text-align: center; margin-bottom: 20px; color: #1914B3'>
        Analyse Lexicale des Raisons de Churn
    </h2>
    """, unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(4, 2))

    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    
    st.pyplot(fig, use_container_width=True)