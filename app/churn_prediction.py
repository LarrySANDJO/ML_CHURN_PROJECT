import streamlit as st
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
from function import *
from css import *
from streamlit_extras.colored_header import colored_header
from dashboard import *
from main import *


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
                        Internet_Type = st.selectbox("Internet Type*", options=['DSL', 'Fiber Optic', 'Cable'])
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
    
    def show_prediction_form(form):
        if form is not None:
            # Vérification de l'API
            if not check_api_status():
                st.error("L'API de prédiction n'est pas disponible")
                return
            
            # Prédiction
            with st.spinner("Prédiction en cours..."):
                prediction, error = predict_single_customer(form.to_dict(orient='records')[0])
                
            if error:
                st.error(f"Erreur: {error}")
            else:
                # Affichage des résultats
                st.success("Prédiction terminée !")
                
                # Création des colonnes pour l'affichage
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Probabilité de churn", 
                            f"{prediction['probability']:.1%}",
                            delta_color="inverse")
                    
                with col2:
                    st.metric("Recommandation",
                            "Action requise" if prediction['prediction'] == 1 else "Surveillance",
                            delta="⚠️" if prediction['prediction'] == 1 else "✅")
                
                # Détails supplémentaires
                with st.expander("Détails techniques"):
                    st.json(prediction)
                    
                # Bouton d'action
                if prediction['prediction'] == 1:
                    st.warning("Ce client présente un risque élevé de churn")
                    if st.button("📞 Planifier un appel préventif"):
                        st.success("Action enregistrée dans le CRM")
    
    show_prediction_form(form_data)
                        
    def show_batch_prediction():
        st.header("Prédiction par lot (CSV)")
        uploaded_file = st.file_uploader("Téléverser un fichier CSV", type=["csv"])
        
        if uploaded_file is not None:
            # Vérification API
            if not check_api_status():
                st.error("L'API de prédiction n'est pas disponible")
                return
            
            # Prévisualisation
            df_preview = pd.read_csv(uploaded_file)
            st.write("Aperçu des données :")
            st.dataframe(df_preview.head(3))
            
            if st.button("Lancer les prédictions"):
                with st.spinner("Analyse en cours..."):
                    # Envoi du fichier
                    results, error = upload_csv_for_prediction(uploaded_file.getvalue())
                    
                    if error:
                        st.error(f"Erreur: {error}")
                    else:
                        st.success(f"Analyse terminée pour {len(results)} clients")
                        
                        # Téléchargement des résultats
                        st.download_button(
                            label="📥 Télécharger les résultats",
                            data=pd.DataFrame(results).to_csv(index=False),
                            file_name="predictions_results.csv",
                            mime="text/csv"
                        )
                        
                        # Visualisation
                        df_results = pd.DataFrame(results)
                        
                        # KPI globaux
                        churn_rate = df_results['prediction'].mean()
                        st.metric("Taux de churn prédit", f"{churn_rate:.1%}")
                        
                        # Histogramme des probabilités
                        fig = px.histogram(df_results, 
                                        x="probability",
                                        nbins=20,
                                        color_discrete_sequence=['#1914B3'])
                        st.plotly_chart(fig)
    
    show_batch_prediction()
        
    
    