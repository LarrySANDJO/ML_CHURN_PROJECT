import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import time
from datetime import datetime
import io

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Churn Telecom",
    page_icon="📞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration de l'API
API_BASE_URL = "https://projet-ml2-api.onrender.com/"

# Custom CSS pour améliorer l'apparence
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .risk-high {
        background-color: #ffebee;
        border-left-color: #f44336;
    }
    .risk-medium {
        background-color: #fff3e0;
        border-left-color: #ff9800;
    }
    .risk-low {
        background-color: #e8f5e8;
        border-left-color: #4caf50;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Fonctions utilitaires
@st.cache_data
def check_api_status():
    """Vérifier si l'API est accessible"""
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_risk_color(risk_level):
    """Retourner la couleur selon le niveau de risque"""
    colors = {
        "Très Élevé": "#d32f2f",
        "Élevé": "#f57c00", 
        "Moyen": "#ffa000",
        "Faible": "#388e3c",
        "Très Faible": "#1976d2"
    }
    return colors.get(risk_level, "#757575")

def predict_single_customer(customer_data):
    """Faire une prédiction pour un client individuel"""
    try:
        response = requests.post(f"{API_BASE_URL}/predict", json=customer_data)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Erreur API: {response.status_code}"
    except Exception as e:
        return None, f"Erreur de connexion: {str(e)}"

def upload_csv_for_prediction(file_data):
    """Upload CSV pour prédictions en lot"""
    try:
        files = {"file": ("data.csv", file_data, "text/csv")}
        response = requests.post(f"{API_BASE_URL}/predict/csv", files=files)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Erreur API: {response.status_code}"
    except Exception as e:
        return None, f"Erreur de connexion: {str(e)}"

def download_results():
    """Télécharger les résultats de prédiction"""
    try:
        response = requests.get(f"{API_BASE_URL}/download/results")
        if response.status_code == 200:
            return response.content, None
        else:
            return None, f"Erreur API: {response.status_code}"
    except Exception as e:
        return None, f"Erreur de connexion: {str(e)}"

# Interface principal
def main():
    # Header
    st.title("📞 Dashboard Prédiction Churn Telecom")
    st.markdown("---")
    
    # Vérification du statut de l'API
    api_status = check_api_status()
    if api_status:
        st.success("✅ API connectée et fonctionnelle")
    else:
        st.error("❌ API non accessible. Vérifiez que l'API est démarrée sur http://localhost:8000")
        st.stop()
    
    # Sidebar pour la navigation
    st.sidebar.title("🎛️ Navigation")
    tab_selection = st.sidebar.radio(
        "Choisissez une option:",
        ["🏠 Accueil", "👤 Prédiction Individuelle", "📊 Prédiction en Lot", "📈 Analyses"]
    )
    
    if tab_selection == "🏠 Accueil":
        show_home_page()
    elif tab_selection == "👤 Prédiction Individuelle":
        show_individual_prediction()
    elif tab_selection == "📊 Prédiction en Lot":
        show_batch_prediction()
    elif tab_selection == "📈 Analyses":
        show_analytics()

def show_home_page():
    """Page d'accueil avec informations générales"""
    st.header("🏠 Bienvenue sur le Dashboard de Prédiction de Churn")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>👤 Prédiction Individuelle</h3>
            <p>Analysez le risque de churn pour un client spécifique en saisissant ses informations détaillées.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>📊 Prédiction en Lot</h3>
            <p>Uploadez un fichier CSV pour analyser plusieurs clients simultanément et télécharger les résultats.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>📈 Analyses</h3>
            <p>Visualisez les tendances et statistiques des prédictions pour une meilleure prise de décision.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Informations sur les niveaux de risque
    st.subheader("📊 Niveaux de Risque de Churn")
    
    risk_col1, risk_col2, risk_col3, risk_col4, risk_col5 = st.columns(5)
    
    with risk_col1:
        st.markdown("""
        <div class="metric-card risk-high">
            <h4 style="color: #d32f2f;">Très Élevé</h4>
            <p style="color: #d32f2f;">≥ 80%</p>
            <small>Action immédiate requise</small>
        </div>
        """, unsafe_allow_html=True)
    
    with risk_col2:
        st.markdown("""
        <div class="metric-card risk-high">
            <h4 style="color: #f57c00;">Élevé</h4>
            <p style="color: #f57c00;">60-79%</p>
            <small>Surveillance étroite</small>
        </div>
        """, unsafe_allow_html=True)
    
    with risk_col3:
        st.markdown("""
        <div class="metric-card risk-medium">
            <h4 style="color: #ffa000;">Moyen</h4>
            <p style="color: #ffa000;">40-59%</p>
            <small>Attention modérée</small>
        </div>
        """, unsafe_allow_html=True)
    
    with risk_col4:
        st.markdown("""
        <div class="metric-card risk-low">
            <h4 style="color: #388e3c;">Faible</h4>
            <p style="color: #388e3c;">20-39%</p>
            <small>Risque contrôlé</small>
        </div>
        """, unsafe_allow_html=True)
    
    with risk_col5:
        st.markdown("""
        <div class="metric-card risk-low">
            <h4 style="color: #1976d2;">Très Faible</h4>
            <p style="color: #1976d2;">< 20%</p>
            <small>Client fidèle</small>
        </div>
        """, unsafe_allow_html=True)

def show_individual_prediction():
    """Interface pour la prédiction individuelle"""
    st.header("👤 Prédiction Individuelle")
    st.markdown("Saisissez les informations du client pour prédire son risque de churn.")
    
    with st.form("customer_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📋 Informations Personnelles")
            customer_id = st.text_input("ID Client (optionnel)", value="")
            gender = st.selectbox("Genre", ["Male", "Female"])
            age = st.number_input("Âge", min_value=18, max_value=100, value=35)
            married = st.selectbox("Marié", ["Yes", "No"])
            dependents = st.number_input("Nombre de dépendants", min_value=0, max_value=10, value=0)
            
            st.subheader("📍 Localisation")
            city = st.text_input("Ville (optionnel)", value="")
            zip_code = st.text_input("Code postal (optionnel)", value="")
            latitude = st.number_input("Latitude (optionnel)", value=0.0)
            longitude = st.number_input("Longitude (optionnel)", value=0.0)
        
        with col2:
            st.subheader("📞 Services Téléphone")
            phone_service = st.selectbox("Service téléphonique", ["Yes", "No"])
            multiple_lines = st.selectbox("Lignes multiples", ["Yes", "No", "No phone service"])
            long_distance_charges = st.number_input("Frais longue distance mensuels moyens", min_value=0.0, value=0.0)
            
            st.subheader("🌐 Services Internet")
            internet_service = st.selectbox("Service internet", ["DSL", "Fiber optic", "No"])
            internet_type = st.selectbox("Type internet", ["DSL", "Fiber Optic", "Cable", "None"])
            monthly_gb = st.number_input("GB téléchargés mensuellement", min_value=0.0, value=0.0)
            
            st.subheader("🔒 Services Additionnels")
            online_security = st.selectbox("Sécurité en ligne", ["Yes", "No", "No internet service"])
            online_backup = st.selectbox("Sauvegarde en ligne", ["Yes", "No", "No internet service"])
            device_protection = st.selectbox("Protection d'appareil", ["Yes", "No", "No internet service"])
            tech_support = st.selectbox("Support technique premium", ["Yes", "No", "No internet service"])
        
        with col3:
            st.subheader("🎬 Services Streaming")
            streaming_tv = st.selectbox("TV streaming", ["Yes", "No", "No internet service"])
            streaming_movies = st.selectbox("Films streaming", ["Yes", "No", "No internet service"])
            streaming_music = st.selectbox("Musique streaming", ["Yes", "No", "No internet service"])
            unlimited_data = st.selectbox("Données illimitées", ["Yes", "No"])
            
            st.subheader("💳 Facturation")
            contract = st.selectbox("Type de contrat", ["Month-to-month", "One year", "Two year"])
            paperless_billing = st.selectbox("Facturation dématérialisée", ["Yes", "No"])
            payment_method = st.selectbox("Méthode de paiement", 
                                        ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
            monthly_charge = st.number_input("Frais mensuels", min_value=0.0, value=50.0)
            total_charges = st.number_input("Frais totaux", min_value=0.0, value=500.0)
            
            st.subheader("🔢 Informations Supplémentaires")
            referrals = st.number_input("Nombre de références", min_value=0, value=0)
            tenure_months = st.number_input("Ancienneté (mois)", min_value=0, value=12)
        
        submitted = st.form_submit_button("🔮 Prédire le Churn", use_container_width=True)
        
        if submitted:
            # Préparer les données
            customer_data = {
                "Customer_ID": customer_id if customer_id else None,
                "Gender": gender,
                "Age": age,
                "Married": married,
                "Number_of_Dependents": dependents,
                "City": city if city else None,
                "Zip_Code": zip_code if zip_code else None,
                "Latitude": latitude if latitude != 0.0 else None,
                "Longitude": longitude if longitude != 0.0 else None,
                "Number_of_Referrals": referrals,
                "Tenure_in_Months": tenure_months,
                "Phone_Service": phone_service,
                "Avg_Monthly_Long_Distance_Charges": long_distance_charges,
                "Multiple_Lines": multiple_lines,
                "Internet_Service": internet_service,
                "Internet_Type": internet_type,
                "Avg_Monthly_GB_Download": monthly_gb,
                "Online_Security": online_security,
                "Online_Backup": online_backup,
                "Device_Protection_Plan": device_protection,
                "Premium_Tech_Support": tech_support,
                "Streaming_TV": streaming_tv,
                "Streaming_Movies": streaming_movies,
                "Streaming_Music": streaming_music,
                "Unlimited_Data": unlimited_data,
                "Contract": contract,
                "Paperless_Billing": paperless_billing,
                "Payment_Method": payment_method,
                "Monthly_Charge": monthly_charge,
                "Total_Charges": total_charges,
                "Offer": None,
                "Total_Refunds": 0.0,
                "Total_Extra_Data_Charges": 0.0,
                "Total_Long_Distance_Charges": 0.0,
                "Total_Revenue": None,
                "Customer_Status": None,
                "Churn_Category": None,
                "Churn_Reason": None
            }
            
            with st.spinner("Analyse en cours..."):
                result, error = predict_single_customer(customer_data)
                
                if error:
                    st.error(f"Erreur: {error}")
                else:
                    # Afficher les résultats
                    st.success("✅ Prédiction réalisée avec succès!")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        prediction_text = "🔴 CHURN" if result['prediction'] == 1 else "🟢 FIDÈLE"
                        st.metric("Prédiction", prediction_text)
                    
                    with col2:
                        st.metric("Probabilité de Churn", f"{result['probability']:.1%}")
                    
                    with col3:
                        risk_color = get_risk_color(result['risk_level'])
                        st.markdown(f"**Niveau de Risque**")
                        st.markdown(f"<span style='color: {risk_color}; font-size: 1.2em; font-weight: bold;'>{result['risk_level']}</span>", 
                                  unsafe_allow_html=True)
                    
                    with col4:
                        st.metric("Timestamp", result['timestamp'][:19])
                    
                    # Jauge de probabilité
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = result['probability'] * 100,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Probabilité de Churn (%)"},
                        delta = {'reference': 50},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 20], 'color': "lightgreen"},
                                {'range': [20, 40], 'color': "yellow"},
                                {'range': [40, 60], 'color': "orange"},
                                {'range': [60, 80], 'color': "red"},
                                {'range': [80, 100], 'color': "darkred"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        }
                    ))
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)

def show_batch_prediction():
    """Interface pour les prédictions en lot"""
    st.header("📊 Prédiction en Lot")
    st.markdown("Uploadez un fichier CSV pour analyser plusieurs clients simultanément.")
    
    # Section d'upload
    st.subheader("📁 Upload du fichier CSV")
    
    with st.expander("ℹ️ Format requis du fichier CSV", expanded=False):
        st.markdown("""
        **Colonnes essentielles requises:**
        - Gender, Age, Married, Number_of_Dependents, Number_of_Referrals
        - Tenure_in_Months, Phone_Service, Avg_Monthly_Long_Distance_Charges
        - Multiple_Lines, Internet_Service, Internet_Type, Avg_Monthly_GB_Download
        - Online_Security, Online_Backup, Device_Protection_Plan, Premium_Tech_Support
        - Streaming_TV, Streaming_Movies, Streaming_Music, Unlimited_Data
        - Contract, Paperless_Billing, Payment_Method, Monthly_Charge, Total_Charges
        
        **Colonnes optionnelles:**
        - Customer_ID, City, Zip_Code, Latitude, Longitude, Offer
        - Total_Refunds, Total_Extra_Data_Charges, Total_Long_Distance_Charges
        - Total_Revenue, Customer_Status, Churn_Category, Churn_Reason
        """)
    
    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type=['csv'])
    
    if uploaded_file is not None:
        # Prévisualisation des données
        try:
            df_preview = pd.read_csv(uploaded_file)
            
            st.subheader("👀 Aperçu des données")
            st.dataframe(df_preview.head(10), use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Nombre de lignes", len(df_preview))
            with col2:
                st.metric("Nombre de colonnes", len(df_preview.columns))
            with col3:
                st.metric("Taille du fichier", f"{uploaded_file.size / 1024:.1f} KB")
            
            # Bouton de prédiction
            if st.button("🚀 Lancer les prédictions", use_container_width=True):
                # Reset file pointer
                uploaded_file.seek(0)
                file_data = uploaded_file.read()
                
                with st.spinner("Traitement en cours... Cela peut prendre quelques minutes."):
                    result, error = upload_csv_for_prediction(file_data)
                    
                    if error:
                        st.error(f"Erreur: {error}")
                    else:
                        st.success("✅ Prédictions réalisées avec succès!")
                        
                        # Afficher les résultats
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Total clients", result['total_customers'])
                        with col2:
                            st.metric("Prédictions réussies", result['successful_predictions'])
                        with col3:
                            st.metric("Échecs", result['failed_predictions'])
                        with col4:
                            st.metric("Temps de traitement", f"{result['processing_time']:.1f}s")
                        
                        # Bouton de téléchargement
                        if st.button("📥 Télécharger les résultats", use_container_width=True):
                            with st.spinner("Préparation du téléchargement..."):
                                csv_data, download_error = download_results()
                                
                                if download_error:
                                    st.error(f"Erreur de téléchargement: {download_error}")
                                else:
                                    st.download_button(
                                        label="💾 Télécharger le fichier CSV",
                                        data=csv_data,
                                        file_name=f"churn_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                        mime="text/csv",
                                        use_container_width=True
                                    )
        
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier: {str(e)}")

def show_analytics():
    """Page d'analyse des résultats"""
    st.header("📈 Analyses et Statistiques")
    
    # Simuler des données d'analyse (en production, récupérer depuis une base de données)
    st.info("📊 Cette section afficherait les analyses des prédictions historiques")
    
    # Graphiques de démonstration
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution des niveaux de risque (exemple)
        risk_data = {
            'Niveau de Risque': ['Très Faible', 'Faible', 'Moyen', 'Élevé', 'Très Élevé'],
            'Nombre de Clients': [150, 120, 80, 60, 40]
        }
        df_risk = pd.DataFrame(risk_data)
        
        fig = px.pie(df_risk, values='Nombre de Clients', names='Niveau de Risque',
                     title="Distribution des Niveaux de Risque",
                     color_discrete_map={
                         'Très Faible': '#1976d2',
                         'Faible': '#388e3c',
                         'Moyen': '#ffa000',
                         'Élevé': '#f57c00',
                         'Très Élevé': '#d32f2f'
                     })
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Évolution temporelle (exemple)
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='M')
        churn_rates = [15, 18, 12, 20, 25, 22, 19, 16, 14, 21, 23, 17]
        
        df_trend = pd.DataFrame({
            'Mois': dates,
            'Taux de Churn (%)': churn_rates
        })
        
        fig = px.line(df_trend, x='Mois', y='Taux de Churn (%)',
                      title="Évolution du Taux de Churn Prédit",
                      markers=True)
        fig.update_layout(xaxis_title="Mois", yaxis_title="Taux de Churn (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Métriques clés
    st.subheader("📊 Métriques Clés")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Prédictions Totales", "2,450", delta="12%")
    with col2:
        st.metric("Taux de Churn Moyen", "18.5%", delta="-2.1%")
    with col3:
        st.metric("Clients à Risque Élevé", "245", delta="5%")
    with col4:
        st.metric("Précision du Modèle", "89.2%", delta="1.3%")

if __name__ == "__main__":
    main()