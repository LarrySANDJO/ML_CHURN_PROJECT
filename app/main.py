from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import joblib
import pandas as pd
import numpy as np
import logging
from datetime import datetime
import uvicorn
import io
import csv

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modèles Pydantic pour la validation des données
class CustomerData(BaseModel):
    Customer_ID: Optional[str] = Field(None, description="ID du client")
    Gender: str = Field(..., description="Genre du client")
    Age: int = Field(..., ge=18, le=100, description="Âge du client") 
    Married: str = Field(..., description="Statut marital")
    Number_of_Dependents: int = Field(0, ge=0, description="Nombre de dépendants")
    City: Optional[str] = Field(None, description="Ville du client")
    Zip_Code: Optional[str] = Field(None, description="Code postal")
    Latitude: Optional[float] = Field(None, description="Latitude")
    Longitude: Optional[float] = Field(None, description="Longitude")
    Number_of_Referrals: int = Field(0, ge=0, description="Nombre de références")
    Tenure_in_Months: int = Field(..., ge=0, description="Ancienneté en mois")
    Offer: Optional[str] = Field(None, description="Offre souscrite")
    Phone_Service: str = Field(..., description="Service téléphonique")
    Avg_Monthly_Long_Distance_Charges: float = Field(0.0, description="Frais longue distance moyens")
    Multiple_Lines: str = Field(..., description="Lignes multiples")
    Internet_Service: str = Field(..., description="Service internet")
    Internet_Type: str = Field(..., description="Type d'internet")
    Avg_Monthly_GB_Download: float = Field(0.0, description="GB téléchargés moyens")
    Online_Security: str = Field(..., description="Sécurité en ligne")
    Online_Backup: str = Field(..., description="Sauvegarde en ligne")
    Device_Protection_Plan: str = Field(..., description="Plan de protection")
    Premium_Tech_Support: str = Field(..., description="Support technique premium")
    Streaming_TV: str = Field(..., description="TV en streaming")
    Streaming_Movies: str = Field(..., description="Films en streaming")
    Streaming_Music: str = Field(..., description="Musique en streaming")
    Unlimited_Data: str = Field(..., description="Données illimitées")
    Contract: str = Field(..., description="Type de contrat")
    Paperless_Billing: str = Field(..., description="Facturation dématérialisée")
    Payment_Method: str = Field(..., description="Méthode de paiement")
    Monthly_Charge: float = Field(..., description="Frais mensuels")
    Total_Charges: float = Field(..., description="Frais totaux")
    Total_Refunds: Optional[float] = Field(0.0, description="Remboursements totaux")
    Total_Extra_Data_Charges: Optional[float] = Field(0.0, description="Frais données supplémentaires")
    Total_Long_Distance_Charges: Optional[float] = Field(0.0, description="Frais longue distance totaux")
    Total_Revenue: Optional[float] = Field(None, description="Revenus totaux")
    Customer_Status: Optional[str] = Field(None, description="Statut du client")
    Churn_Category: Optional[str] = Field(None, description="Catégorie de churn")
    Churn_Reason: Optional[str] = Field(None, description="Raison du churn")

class BatchPredictionRequest(BaseModel):
    customers: List[CustomerData] = Field(..., description="Liste des clients")

class PredictionResponse(BaseModel):
    prediction: int = Field(..., description="Prédiction (0=Stay, 1=Churn)")
    probability: float = Field(..., description="Probabilité de churn")
    risk_level: str = Field(..., description="Niveau de risque")
    timestamp: str = Field(..., description="Timestamp de la prédiction")

class BatchPredictionResponse(BaseModel):
    success: bool
    results: List[Dict[str, Any]]
    total_processed: int
    processing_time: float

class CSVUploadResponse(BaseModel):
    success: bool
    total_customers: int
    successful_predictions: int
    failed_predictions: int
    processing_time: float
    download_url: str = "/download/results"

# Classe pour la gestion des prédictions
class ChurnPredictionAPI:
    def __init__(self):
        self.model_data = None
        self.last_results = None  # Pour stocker les derniers résultats
        self.load_model()
    
    def load_model(self, model_path: str = 'model/telecom_churn_model.pkl'):
        """Charger le modèle pré-entraîné"""
        try:
            self.model_data = joblib.load(model_path)
            logger.info("Modèle chargé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle: {e}")
            self.model_data = None
    
    def validate_csv_columns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Valider les colonnes du CSV"""
        required_columns = {
            'Customer_ID', 'Gender', 'Age', 'Married', 'Number_of_Dependents', 
            'City', 'Zip_Code', 'Latitude', 'Longitude', 'Number_of_Referrals',
            'Tenure_in_Months', 'Offer', 'Phone_Service', 'Avg_Monthly_Long_Distance_Charges',
            'Multiple_Lines', 'Internet_Service', 'Internet_Type', 'Avg_Monthly_GB_Download',
            'Online_Security', 'Online_Backup', 'Device_Protection_Plan', 'Premium_Tech_Support',
            'Streaming_TV', 'Streaming_Movies', 'Streaming_Music', 'Unlimited_Data',
            'Contract', 'Paperless_Billing', 'Payment_Method', 'Monthly_Charge',
            'Total_Charges', 'Total_Refunds', 'Total_Extra_Data_Charges', 
            'Total_Long_Distance_Charges', 'Total_Revenue', 'Customer_Status',
            'Churn_Category', 'Churn_Reason'
        }
        
        # Normaliser les noms de colonnes (enlever espaces, remplacer par underscores)
        df_columns = set(df.columns)
        normalized_df_columns = {col.replace(' ', '_').replace('-', '_') for col in df_columns}
        
        # Colonnes obligatoires pour les prédictions (exclure les colonnes optionnelles)
        essential_columns = {
            'Gender', 'Age', 'Married', 'Number_of_Dependents', 'Number_of_Referrals',
            'Tenure_in_Months', 'Phone_Service', 'Avg_Monthly_Long_Distance_Charges',
            'Multiple_Lines', 'Internet_Service', 'Internet_Type', 'Avg_Monthly_GB_Download',
            'Online_Security', 'Online_Backup', 'Device_Protection_Plan', 'Premium_Tech_Support',
            'Streaming_TV', 'Streaming_Movies', 'Streaming_Music', 'Unlimited_Data',
            'Contract', 'Paperless_Billing', 'Payment_Method', 'Monthly_Charge', 'Total_Charges'
        }
        
        missing_essential = essential_columns - normalized_df_columns
        extra_columns = normalized_df_columns - required_columns
        
        return {
            'missing_columns': list(missing_essential),
            'extra_columns': list(extra_columns),
            'is_valid': len(missing_essential) == 0,
            'all_columns': list(required_columns)
        }
    
    def preprocess_csv_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Préprocesser les données CSV"""
        # Normaliser les noms de colonnes
        df.columns = [col.replace(' ', '_').replace('-', '_') for col in df.columns]
        
        # Convertir les types de données numériques
        numeric_columns = [
            'Age', 'Number_of_Dependents', 'Latitude', 'Longitude', 'Number_of_Referrals',
            'Tenure_in_Months', 'Avg_Monthly_Long_Distance_Charges', 'Avg_Monthly_GB_Download',
            'Monthly_Charge', 'Total_Charges', 'Total_Refunds', 'Total_Extra_Data_Charges',
            'Total_Long_Distance_Charges', 'Total_Revenue'
        ]
        
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Nettoyer les données textuelles
        string_columns = df.select_dtypes(include=['object']).columns
        for col in string_columns:
            df[col] = df[col].astype(str).str.strip()
        
        # Remplir les valeurs manquantes pour les colonnes optionnelles
        optional_columns = ['City', 'Zip_Code', 'Offer', 'Total_Refunds', 
                           'Total_Extra_Data_Charges', 'Total_Long_Distance_Charges',
                           'Total_Revenue', 'Customer_Status', 'Churn_Category', 'Churn_Reason']
        
        for col in optional_columns:
            if col not in df.columns:
                if col in ['Total_Refunds', 'Total_Extra_Data_Charges', 'Total_Long_Distance_Charges', 'Total_Revenue']:
                    df[col] = 0.0
                else:
                    df[col] = 'Unknown'
        
        return df
    
    def preprocess_input(self, data: Dict[str, Any]) -> np.ndarray:
        """Préprocesser les données d'entrée"""
        if self.model_data is None:
            raise ValueError("Modèle non chargé")
        
        # Convertir les noms des champs (remplacer _ par des espaces si nécessaire)
        processed_data = {}
        for key, value in data.items():
            # Garder le format avec underscores pour la cohérence
            processed_data[key] = value
        
        # Convertir en DataFrame
        df = pd.DataFrame([processed_data])
        
        # Encoder les variables catégorielles
        for col, encoder in self.model_data['label_encoders'].items():
            if col in df.columns:
                try:
                    df[col] = encoder.transform(df[col].astype(str))
                except ValueError:
                    # Si valeur inconnue, utiliser la classe la plus fréquente
                    df[col] = 0
        
        # Gérer les colonnes manquantes
        for col in self.model_data['feature_names']:
            if col not in df.columns:
                df[col] = 0
        
        # Réorganiser les colonnes selon l'ordre d'entraînement
        available_features = [col for col in self.model_data['feature_names'] if col in df.columns]
        df = df[available_features]
        
        # Gérer les valeurs manquantes
        df = df.fillna(0)
        
        # Normaliser
        df_scaled = self.model_data['scaler'].transform(df)
        
        return df_scaled
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Faire une prédiction"""
        try:
            processed_data = self.preprocess_input(data)
            
            # Prédiction
            prediction = self.model_data['model'].predict(processed_data)[0]
            probability = self.model_data['model'].predict_proba(processed_data)[0, 1]
            
            return {
                'prediction': int(prediction),
                'probability': float(probability),
                'risk_level': self.get_risk_level(probability),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Erreur lors de la prédiction: {e}")
            raise

    def predict_batch_csv(self, df: pd.DataFrame) -> pd.DataFrame:
        """Faire des prédictions en lot sur un DataFrame"""
        start_time = datetime.now()
        results = []
        
        for index, row in df.iterrows():
            try:
                customer_data = row.to_dict()
                prediction_result = self.predict(customer_data)
                
                result = {
                    'customer_id': row.get('Customer_ID', index),
                    'prediction': prediction_result['prediction'],
                    'probability': prediction_result['probability'],
                    'risk_level': prediction_result['risk_level'],
                    'status': 'success'
                }
                results.append(result)
                
            except Exception as e:
                results.append({
                    'customer_id': row.get('Customer_ID', index),
                    'prediction': None,
                    'probability': None,
                    'risk_level': None,
                    'status': 'error',
                    'error_message': str(e)
                })
        
        results_df = pd.DataFrame(results)
        
        # Combiner avec les données originales
        final_df = pd.concat([df.reset_index(drop=True), results_df], axis=1)
        
        # Sauvegarder pour téléchargement
        self.last_results = final_df
        
        return final_df

    def get_risk_level(self, probability: float) -> str:
        """Déterminer le niveau de risque"""
        if probability >= 0.8:
            return "Très Élevé"
        elif probability >= 0.6:
            return "Élevé"
        elif probability >= 0.4:
            return "Moyen"
        elif probability >= 0.2:
            return "Faible"
        else:
            return "Très Faible"

# Initialisation de FastAPI
app = FastAPI(
    title="Telecom Churn Prediction API",
    description="API pour prédire le churn des clients télécoms avec support CSV complet",
    version="2.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instance globale de l'API
predictor_api = ChurnPredictionAPI()

# Endpoints

@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
async def predict(customer: CustomerData):
    """
    Prédire le churn pour un client individuel
    
    - **customer**: Données du client à analyser (toutes les variables supportées)
    
    Retourne la prédiction, la probabilité et le niveau de risque
    """
    try:
        if predictor_api.model_data is None:
            raise HTTPException(status_code=500, detail="Modèle non chargé")
        
        # Convertir le modèle Pydantic en dictionnaire
        customer_data = customer.dict()
        
        # Faire la prédiction
        result = predictor_api.predict(customer_data)
        
        return PredictionResponse(**result)
        
    except Exception as e:
        logger.error(f"Erreur dans /predict: {e}")
        raise HTTPException(status_code=500, detail=str(e))





@app.post("/predict/csv", response_model=CSVUploadResponse, tags=["Predictions"])
async def predict_csv(file: UploadFile = File(...)):
    """
    Prédictions en lot via upload CSV
    
    - **file**: Fichier CSV contenant les données des clients avec toutes les variables
    
    Upload un fichier CSV avec les colonnes requises et retourne un résumé.
    Les résultats détaillés peuvent être téléchargés via /download/results
    """
    try:
        if predictor_api.model_data is None:
            raise HTTPException(status_code=500, detail="Modèle non chargé")
        
        # Vérifier le type de fichier
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Le fichier doit être au format CSV")
        
        start_time = datetime.now()
        
        # Lire le fichier CSV
        content = await file.read()
        if not content.strip():
            raise HTTPException(status_code=400, detail="Fichier vide ou non lisible")
        
        try:
            df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erreur lors de la lecture CSV : {e}")

        
        # Valider les colonnes
        validation = predictor_api.validate_csv_columns(df)
        if not validation['is_valid']:
            raise HTTPException(
                status_code=400, 
                detail=f"Colonnes essentielles manquantes: {validation['missing_columns']}"
            )
        
        # Préprocesser les données
        df = predictor_api.preprocess_csv_data(df)
        
        # Faire les prédictions
        results_df = predictor_api.predict_batch_csv(df)
        
        # Calculer les statistiques
        successful_predictions = len(results_df[results_df['status'] == 'success'])
        failed_predictions = len(results_df[results_df['status'] == 'error'])
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return CSVUploadResponse(
            success=True,
            total_customers=len(df),
            successful_predictions=successful_predictions,
            failed_predictions=failed_predictions,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Erreur dans /predict/csv: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/results", tags=["Results"])
async def download_results():
    """
    Télécharger les résultats de la dernière prédiction en lot
    
    Retourne un fichier CSV avec toutes les données et prédictions
    """
    try:
        if predictor_api.last_results is None:
            raise HTTPException(status_code=404, detail="Aucun résultat disponible")
        
        # Créer un buffer pour le CSV
        output = io.StringIO()
        predictor_api.last_results.to_csv(output, index=False)
        output.seek(0)
        
        # Générer le nom du fichier avec timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"churn_predictions_{timestamp}.csv"
        
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        logger.error(f"Erreur dans /download/results: {e}")
        raise HTTPException(status_code=500, detail=str(e))
# Point d'entrée pour le développement
if __name__ == "__main__":
    print("🚀 Démarrage de l'API FastAPI de Prédiction de Churn Telecom...")
    print("📚 Documentation disponible sur: http://localhost:8000/docs")
    print("🔄 ReDoc disponible sur: http://localhost:8000/redoc")
    print("\n🔗 Endpoints principaux:")
    print("- GET / : Page d'accueil")
    print("- POST /predict : Prédiction individuelle")
    #print("- POST /predict/batch : Prédictions en lot (JSON)")
    print("- POST /predict/csv : Upload CSV pour prédictions en lot")
    print("- GET /download/results : Télécharger les résultats")
    #print("- GET /template/csv : Télécharger template CSV")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
