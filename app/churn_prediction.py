import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
from function import *
from css import *
from streamlit_extras.colored_header import colored_header
from dashboard import *
from main import *

@st.cache_data
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

def churn_prediction(df):
    df = df

    def prediction_form(df):
        st.header("Formulaire de prédiction de churn")
        
        with st.form("prediction_form"):
            # ============= SECTION 1 - IDENTITÉ =============
            with st.container():
                st.markdown("### 📝 Informations client")
                col1, col2 = st.columns(2)
                with col1:
                    Customer_ID = st.text_input("Customer ID*", value=f"CLT_{len(df)+1:04d}")
                    Gender = st.selectbox("Gender*", options=['Male', 'Female'])
                    Age = st.slider("Age*", min_value=18, max_value=100, value=30)
                    Married = st.radio("Married*", options=['Yes', 'No'], horizontal=True)
                    Number_of_Dependents = st.slider("Number of Dependents", min_value=0, max_value=10, value=0)
                    
                with col2:
                    City = st.selectbox("City", options=sorted(df['City'].unique()))
                    Zip_Code = st.text_input("Zip Code", max_chars=5)
                    Latitude = st.number_input("Latitude", format="%.6f")
                    Longitude = st.number_input("Longitude", format="%.6f")
                    Number_of_Referrals = st.slider("Number of Referrals", min_value=0, max_value=10, value=0)

            # ============= SECTION 2 - SERVICES =============
            with st.container():
                st.markdown("### 📡 Services")
                col3, col4 = st.columns(2)
                with col3:
                    Tenure_in_Months = st.slider("Tenure in Months*", min_value=0, max_value=72, value=12)
                    Offer = st.selectbox("Offer", options=['None', 'Offer A', 'Offer B', 'Offer C', 'Offer D', 'Offer E'])
                    Phone_Service = st.radio("Phone Service*", options=['Yes', 'No'], horizontal=True)
                    
                    if Phone_Service == 'Yes':
                        Avg_Monthly_Long_Distance_Charges = st.number_input(
                            "Avg Monthly Long Distance Charges ($)",
                            min_value=0.0,
                            value=10.0,
                            step=0.1
                        )
                        Multiple_Lines = st.selectbox("Multiple Lines", options=['Yes', 'No'])
                    else:
                        Avg_Monthly_Long_Distance_Charges = 0.0
                        Multiple_Lines = 'No'
                        
                with col4:
                    Internet_Service = st.radio("Internet Service*", options=['Yes', 'No'], horizontal=True)
                    if Internet_Service == 'Yes':
                        Internet_Type = st.selectbox("Internet Type*", options=['DSL', 'Fiber Optic', 'Cable', 'No'])
                        Avg_Monthly_GB_Download = st.slider(
                            "Avg Monthly GB Download",
                            min_value=0,
                            max_value=100,
                            value=10
                        )
                    else:
                        Internet_Type = 'None'
                        Avg_Monthly_GB_Download = 0

            # ============= SECTION 3 - SERVICES OPTIONNELS =============
            if Internet_Service == 'Yes':
                with st.container():
                    st.markdown("### 🔐 Services optionnels")
                    cols = st.columns(4)
                    with cols[0]:
                        Online_Security = st.selectbox("Online Security", options=['Yes', 'No'])
                        Online_Backup = st.selectbox("Online Backup", options=['Yes', 'No'])
                    with cols[1]:
                        Device_Protection_Plan = st.selectbox("Device Protection Plan", options=['Yes', 'No'])
                        Premium_Tech_Support = st.selectbox("Premium Tech Support", options=['Yes', 'No'])
                    with cols[2]:
                        Streaming_TV = st.selectbox("Streaming TV", options=['Yes', 'No'])
                        Streaming_Movies = st.selectbox("Streaming Movies", options=['Yes', 'No'])
                    with cols[3]:
                        Streaming_Music = st.selectbox("Streaming Music", options=['Yes', 'No'])
                        Unlimited_Data = st.selectbox("Unlimited Data", options=['Yes', 'No'])
            else:
                Online_Security = Online_Backup = Device_Protection_Plan = Premium_Tech_Support = 'No'
                Streaming_TV = Streaming_Movies = Streaming_Music = Unlimited_Data = 'No'

            # ============= SECTION 4 - FACTURATION =============
            with st.container():
                st.markdown("### 💰 Facturation")
                col5, col6 = st.columns(2)
                with col5:
                    Contract = st.selectbox("Contract*", options=['Month-to-Month', 'One Year', 'Two Year'])
                    Paperless_Billing = st.radio("Paperless Billing*", options=['Yes', 'No'], horizontal=True)
                    Payment_Method = st.selectbox(
                        "Payment Method*",
                        options=['Bank Withdrawal', 'Credit Card', 'Mailed Check']
                    )
                with col6:
                    Monthly_Charge = st.number_input("Monthly Charge ($)*", min_value=0.0, value=50.0, step=0.1)
                    Total_Charges = st.number_input("Total Charges ($)", min_value=0.0, value=0.0, step=0.1)
                    Total_Refunds = st.number_input("Total Refunds ($)", min_value=0.0, value=0.0, step=0.1)
                    Total_Extra_Data_Charges = st.number_input("Total Extra Data Charges ($)", min_value=0.0, value=0.0, step=0.1)
                    Total_Long_Distance_Charges = st.number_input("Total Long Distance Charges ($)", min_value=0.0, value=0.0, step=0.1)

            # Calcul automatique du Total_Revenue
            Total_Revenue = Monthly_Charge * Tenure_in_Months - Total_Refunds + Total_Extra_Data_Charges + Total_Long_Distance_Charges

            # Champs cachés avec valeurs par défaut
            Customer_Status = "Unknown"
            Churn_Category = None
            Churn_Reason = None

            # Bouton de soumission
            submitted = st.form_submit_button("🚀 Lancer la prédiction", type="primary")
            
            if submitted:
                # Validation des champs obligatoires
                required_fields = {
                    "Gender": Gender,
                    "Age": Age,
                    "Married": Married,
                    "Tenure_in_Months": Tenure_in_Months,
                    "Phone_Service": Phone_Service,
                    "Internet_Service": Internet_Service,
                    "Contract": Contract,
                    "Paperless_Billing": Paperless_Billing,
                    "Payment_Method": Payment_Method,
                    "Monthly_Charge": Monthly_Charge
                }
                
                missing_fields = [field for field, value in required_fields.items() if not value]
                
                if missing_fields:
                    st.error(f"Champs obligatoires manquants : {', '.join(missing_fields)}")
                    return None
                
                # Construction du dictionnaire de données
                input_data = {
                    "Customer_ID": Customer_ID,
                    "Gender": Gender,
                    "Age": Age,
                    "Married": Married,
                    "Number_of_Dependents": Number_of_Dependents,
                    "City": City,
                    "Zip_Code": Zip_Code,
                    "Latitude": Latitude,
                    "Longitude": Longitude,
                    "Number_of_Referrals": Number_of_Referrals,
                    "Tenure_in_Months": Tenure_in_Months,
                    "Offer": Offer,
                    "Phone_Service": Phone_Service,
                    "Avg_Monthly_Long_Distance_Charges": Avg_Monthly_Long_Distance_Charges,
                    "Multiple_Lines": Multiple_Lines,
                    "Internet_Service": Internet_Service,
                    "Internet_Type": Internet_Type,
                    "Avg_Monthly_GB_Download": Avg_Monthly_GB_Download,
                    "Online_Security": Online_Security,
                    "Online_Backup": Online_Backup,
                    "Device_Protection_Plan": Device_Protection_Plan,
                    "Premium_Tech_Support": Premium_Tech_Support,
                    "Streaming_TV": Streaming_TV,
                    "Streaming_Movies": Streaming_Movies,
                    "Streaming_Music": Streaming_Music,
                    "Unlimited_Data": Unlimited_Data,
                    "Contract": Contract,
                    "Paperless_Billing": Paperless_Billing,
                    "Payment_Method": Payment_Method,
                    "Monthly_Charge": Monthly_Charge,
                    "Total_Charges": Total_Charges,
                    "Total_Refunds": Total_Refunds,
                    "Total_Extra_Data_Charges": Total_Extra_Data_Charges,
                    "Total_Long_Distance_Charges": Total_Long_Distance_Charges,
                    "Total_Revenue": Total_Revenue,
                    "Customer_Status": Customer_Status,
                    "Churn_Category": Churn_Category,
                    "Churn_Reason": Churn_Reason
                }
                
                # Conversion en DataFrame
                return pd.DataFrame([input_data])
        
        return None

    
    form_data = prediction_form(df)
    
    def show_prediction_form(form_data):
        if form_data is not None:
            # Vérification de l'API
            if not check_api_status():
                st.error("🚨 L'API de prédiction n'est pas disponible")
                return
            
            # Prédiction
            with st.spinner("🔍 Analyse du profil client en cours..."):
                prediction, error = predict_single_customer(form_data.to_dict(orient='records')[0])
                
            if error:
                st.error(f"❌ Erreur: {error}")
            else:
                proba = prediction['probability']
                prediction_class = prediction['prediction']
                
                # ============= SECTION VISUALISATION =============
                st.success("✅ Analyse terminée avec succès")
                st.markdown("---")
                
                # Jauge de probabilité
                st.markdown(f"### Probabilité de churn: {proba:.1%}")
                gauge_html = f"""
                <div style="width: 100%; background: #f0f2f6; border-radius: 10px; padding: 3px; margin: 10px 0;">
                    <div style="width: {proba*100}%; height: 20px; background: linear-gradient(90deg, #2ecc71 {max(0, 50-proba*100)}%, #f39c12 {max(0, 70-proba*100)}%, #e74c3c {max(0, 90-proba*100)}%); border-radius: 8px; transition: width 0.5s ease;">
                    </div>
                </div>
                """
                st.markdown(gauge_html, unsafe_allow_html=True)
                
                # ============= ALERTE DE RISQUE =============
                risk_level = ""
                alert_type = ""
                recommendations = []
                
                if proba < 0.3:
                    risk_level = "Risque Faible"
                    alert_type = "success"
                    recommendations = [
                        "Maintenir la relation client standard",
                        "Proposer des offres de fidélisation basiques"
                    ]
                elif proba < 0.6:
                    risk_level = "Risque Modéré"
                    alert_type = "warning"
                    recommendations = [
                        "Contacter le client pour feedback",
                        "Proposer une offre spéciale",
                        "Vérifier la satisfaction sur les services utilisés"
                    ]
                elif proba < 0.8:
                    risk_level = "Haut Risque"
                    alert_type = "error"
                    recommendations = [
                        "Action immédiate requise",
                        "Offrir un entretien personnalisé",
                        "Évaluer les raisons potentielles de mécontentement"
                    ]
                else:
                    risk_level = "Risque Critique"
                    alert_type = "error"
                    recommendations = [
                        "Intervention urgente du service client",
                        "Offre exceptionnelle de rétention",
                        "Analyse approfondie des motifs de churn"
                    ]
                
                st.markdown(f"""
                <div class="alert alert-{alert_type}" style="padding: 15px; border-radius: 5px; background: {'#d4edda' if alert_type == 'success' else '#fff3cd' if alert_type == 'warning' else '#f8d7da'}; color: {'#155724' if alert_type == 'success' else '#856404' if alert_type == 'warning' else '#721c24'}; border: 1px solid {'#c3e6cb' if alert_type == 'success' else '#ffeeba' if alert_type == 'warning' else '#f5c6cb'}; margin: 10px 0;">
                    <strong>Niveau de risque:</strong> {risk_level}
                </div>
                """, unsafe_allow_html=True)
                
                # ============= RECOMMANDATIONS PERSONNALISÉES =============
                st.markdown("### 🔍 Recommandations spécifiques")
                
                # Recommandations basées sur les caractéristiques du client
                if form_data['Internet_Service'].iloc[0] == 'Yes' and form_data['Internet_Type'].iloc[0] == 'Fiber Optic':
                    recommendations.append("Vérifier la qualité de la connexion fibre")
                
                if form_data['Contract'].iloc[0] == 'Month-to-Month':
                    recommendations.append("Proposer un contrat à engagement pour réduire le risque")
                
                if form_data['Number_of_Referrals'].iloc[0] > 3:
                    recommendations.append("Mettre en avant le programme de parrainage")
                
                # Affichage des recommandations
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"""
                    <div style="padding: 10px; margin: 5px 0; background: #f8f9fa; border-left: 4px solid #1914B3; border-radius: 0 4px 4px 0;">
                        <span style="font-weight: bold; color: #1914B3;">{i}.</span> {rec}
                    </div>
                    """, unsafe_allow_html=True)
                
                # ============= ACTIONS IMMÉDIATES =============
                if prediction_class == 1:
                    st.markdown("---")
                    st.markdown("### 🚀 Actions immédiates")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📞 Planifier un appel préventif", use_container_width=True):
                            st.success("Appel programmé dans le CRM")
                    
                    with col2:
                        if st.button("✉️ Envoyer une offre spéciale", use_container_width=True):
                            st.success("Offre envoyée au client")
                
                # ============= DONNÉES TECHNIQUES =============
                with st.expander("🔧 Détails techniques"):
                    st.json(prediction)

    # Utilisation
    show_prediction_form(form_data)
                        
    def show_batch_prediction():
        st.header("📊 Prédiction par lot (CSV)")
        
        # Section de téléchargement
        with st.expander("ℹ️ Instructions", expanded=True):
            st.markdown("""
            **Format requis :**
            - Le fichier CSV doit contenir les mêmes colonnes que le formulaire individuel
            - Format des colonnes : `Customer_ID, Gender, Age, Married,...` (respecter la casse)
            - Taille maximale : 100MB
            """)
        
        uploaded_file = st.file_uploader("Déposer votre fichier CSV ici", type=["csv"], 
                                    accept_multiple_files=False)
        
        if uploaded_file is not None:
            # Vérification API
            if not check_api_status():
                st.error("🚨 L'API de prédiction n'est pas disponible")
                return
            
            # Prévisualisation
            try:
                df_preview = pd.read_csv(uploaded_file)
                
                with st.expander("👀 Aperçu des données (5 premières lignes)", expanded=True):
                    st.dataframe(df_preview.head(), use_container_width=True)
                    
                    # Validation des colonnes
                    required_columns = ['Gender', 'Age', 'Contract', 'Internet_Service']
                    missing_cols = [col for col in required_columns if col not in df_preview.columns]
                    
                    if missing_cols:
                        st.error(f"Colonnes obligatoires manquantes : {', '.join(missing_cols)}")
                        return
                    
                # Bouton de lancement
                if st.button("🚀 Lancer l'analyse prédictive", type="primary"):
                    with st.spinner(f"🔍 Analyse de {len(df_preview)} clients en cours..."):
                        results, error = upload_csv_for_prediction(uploaded_file.getvalue())
                        
                        if error:
                            st.error(f"❌ {error}")
                        else:
                            df_results = pd.DataFrame(results)
                            st.success(f"✅ Analyse terminée pour {len(df_results)} clients")
                            
                            # ============= SECTION RÉSULTATS =============
                            st.markdown("---")
                            st.subheader("📋 Résultats détaillés par client")
                            
                            # Configuration de l'affichage
                            st.markdown("""
                            <style>
                                .dataframe td {
                                    font-size: 13px;
                                }
                                .positive {
                                    color: #e74c3c;
                                    font-weight: bold;
                                }
                                .negative {
                                    color: #2ecc71;
                                }
                            </style>
                            """, unsafe_allow_html=True)
                            
                            # Fonction de formatage conditionnel
                            def color_proba(val):
                                color = '#e74c3c' if val > 0.7 else '#f39c12' if val > 0.5 else '#2ecc71'
                                return f'color: {color}; font-weight: bold'
                            
                            # Affichage du dataframe interactif
                            st.dataframe(
                                df_results.style
                                    .format({
                                        'probability': '{:.1%}',
                                        'Monthly_Charge': '${:.2f}'
                                    })
                                    .applymap(color_proba, subset=['probability'])
                                    .bar(subset=['probability'], color='#1914B3')
                                    .set_properties(**{
                                        'background-color': '#f8f9fa',
                                        'border': '1px solid #ddd'
                                    }),
                                use_container_width=True,
                                height=500
                            )
                            
                            # Options d'export
                            st.download_button(
                                label="📥 Exporter les résultats complets",
                                data=df_results.to_csv(index=False),
                                file_name="churn_predictions.csv",
                                mime="text/csv"
                            )
                            
                            # ============= ANALYSE GLOBALE =============
                            st.markdown("---")
                            st.subheader("📈 Analyse globale")
                            
                            # KPIs
                            kpi1, kpi2, kpi3 = st.columns(3)
                            with kpi1:
                                churn_rate = df_results['prediction'].mean()
                                st.metric("Taux de churn", f"{churn_rate:.1%}")
                            
                            with kpi2:
                                high_risk = (df_results['probability'] > 0.7).mean()
                                st.metric("Clients à haut risque", f"{high_risk:.1%}")
                            
                            with kpi3:
                                avg_proba = df_results['probability'].mean()
                                st.metric("Probabilité moyenne", f"{avg_proba:.1%}")
                            
                            # Visualisations
                            tab1, tab2 = st.tabs(["Distribution", "Segmentation"])
                            
                            with tab1:
                                fig = px.histogram(df_results, x="probability", nbins=20,
                                                title="Distribution des probabilités de churn",
                                                color_discrete_sequence=['#1914B3'])
                                fig.add_vline(x=0.7, line_dash="dash", line_color="red")
                                st.plotly_chart(fig, use_container_width=True)
                            
                            with tab2:
                                fig = px.box(df_results, x="Contract", y="probability",
                                        color="Internet_Service",
                                        title="Probabilité par type de contrat")
                                st.plotly_chart(fig, use_container_width=True)
            
            except Exception as e:
                st.error(f"Erreur de lecture du fichier : {str(e)}")

    # Utilisation
    show_batch_prediction()