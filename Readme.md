# 📊 ML_CHURN_PROJECT — Prédiction de la résiliation client avec le Machine Learning

### 📌 Contexte

Ce projet a été réalisé dans le cadre d’un travail académique à l’ENSAE de Dakar, dans une optique de mise en pratique des compétences en Data Science et Machine Learning sur une problématique métier réelle : la **prédiction de la résiliation client (churn)**. 
Il s'inscrit dans la dynamique Business Intelligence et vise à fournir des outils concrets et exploitables pour l’anticipation du départ des clients.

---

## 📑 Table des matières

- [🎯 Objectifs](#-objectifs)
- [🧠 Méthodologie](#-méthodologie)
- [🚀 Lancement du projet](#-lancement-du-projet)
- [📊 Résultats](#-résultats)
- [🖥️ Application et API](#-application-api)
- [🧑‍💻 Auteur](#-auteur)
- [📝 Licence](#-licence)

---

## 🎯 Objectifs

La problématique centrale de ce projet est de savoir s’il est possible, à partir des données disponibles sur les clients, de **prédire leur probabilité de résiliation**. Cela permettrait à une entreprise de télécommunications (ou tout autre service par abonnement) de mieux cibler ses actions de fidélisation.

L’objectif opérationnel est double :

- **Modéliser le risque de churn** en exploitant des données clients structurées (profil, contrat, usage, support, etc.).
- **Fournir des outils accessibles** (API et application web) aux utilisateurs non techniques, afin qu’ils puissent exploiter facilement les prédictions dans une logique de pilotage.

---

## 🧠 Méthodologie

Le projet suit une démarche rigoureuse et structurée en cinq étapes majeures :

### 🔎 Exploration des données (EDA)

Analyse initiale pour comprendre la structure des données, visualiser les corrélations, détecter les valeurs aberrantes ou les classes déséquilibrées. Cela a permis d’identifier les variables influentes dans le churn.

### 🧹 Prétraitement

- Traitement des valeurs manquantes
- Encodage des variables catégorielles (Label Encoding, One-Hot Encoding)
- Normalisation des variables numériques

### 🤖 Modélisation

Plusieurs modèles ont été testés et comparés :

- Régression Logistique
- SVM
- LigthGBM
- Random Forest
- etc.
- **XGBoost** (modèle final retenu pour sa précision et robustesse)

Les modèles ont été évalués via une **validation croisée** (K-Fold) avec ajustement des hyperparamètres via **GridSearchCV** et une optimisation du seuil de prédiction

### 🧮 Évaluation

Les performances ont été mesurées à l’aide de :

- F1-score, Accuracy, ROC-AUC
- Matrice de confusion

### ⚙️ Déploiement

Deux outils ont été conçus pour rendre le modèle exploitable :

- Une **API REST** avec FastAPI
- Une **interface utilisateur** via Streamlit

---

## 🚀 Lancement du projet

### 1. Cloner le dépôt

```bash
git clone https://github.com/LarrySANDJO/ML_CHURN_PROJECT.git
cd ML_CHURN_PROJECT
```

### 2. Créer et activer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate     # Linux / MacOS
venv\Scripts\activate        # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```


### 4. Lancer l'application Streamlit

```bash
streamlit run app/app.py
```

---

## 📊 Résultats

Le modèle XGBoost a été sélectionné pour ses performances :

| Métrique     | Score     |
|--------------|-----------|
| Accuracy     | 84 %    |
| Precision    | 68 %    |
| Recall       | 78 %    |
| F1-score     | 72 %    |
| ROC-AUC      | 91 %    |


## 🖥️ Application et API

L’application Streamlit permet aux utilisateurs de visualiser des indicateurs, soumettre des cas client et recevoir une prédiction instantanée de churn avec un score de probabilité.

L’API FastAPI permet l’intégration dans des outils tiers ou pipelines automatisés.

- ⚙️ **Lien vers l’API FastAPI déployée** : *https://projet-ml2-api.onrender.com/docs* (lancer d'abord l'api avant le dashboard pour pouvoir faire des prédictions)
- 🌐 **Lien vers l’application Streamlit** : *https://californiatelecom.streamlit.app/*  


---

## 🧑‍💻 Auteur

**Josette MATANG**

**Kpakou N'MOUNENE**

**Fama DIOP**

**Larry SANDJO**  
*Élèves Ingénieurs Statisticiens Économistes — ENSAE Dakar (ISE2 2024-2025)*
📧 Contact : [larrysandjo337@gmail.com]  

---

## 📝 Licence

Ce projet est distribué sous licence **MIT**. Voir le fichier [LICENSE](./LICENSE) pour plus de détails.
