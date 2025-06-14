import streamlit as st

def styles_css():
    # Classes pour les styles CSS
    st.markdown("""
                <style>
                .main {
                    background-color: #f8f9fa; /* Blanc cassé élégant */
                    padding: 20px;
                }
                h1, h2 {
                    color: #c0392b; /* Rouge sang pour les titres */
                    font-family: 'Helvetica Neue', sans-serif;
                    font-weight: bold;
                    font-size: 32px;
                    text-align: center;
                }
                .stMarkdown {
                    font-family: 'Helvetica Neue', sans-serif;
                    color: #333333; /* Gris anthracite doux */
                }
                .metric-card {
                    border-radius: 10px;
                    padding: 25px;
                    margin: 15px 0;
                    text-align: center;
                    background-color: #ffffff;
                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
                    transition: all 0.3s ease;
                    border: 1px solid #e0e0e0;
                }
                .metric-card:hover {
                    transform: translateY(-8px);
                    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
                    border: 1px solid #c0392b; /* Rouge au survol */
                }
                .metric-title {
                    font-size: 22px;
                    font-weight: bold;
                    margin-bottom: 12px;
                    color: #333333;
                }
                .metric-value {
                    font-size: 32px;
                    font-weight: bold;
                    color: #ffffff;
                    border-radius: 8px;
                    padding: 8px 16px;
                    display: inline-block;
                }
                </style>
            """, unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        /* Sidebar */
        .sidebar .sidebar-content {
            background-color: white;
            padding: 1rem;
        }

        .sidebar-logo {
            padding: 1rem;
            margin-bottom: 2rem;
        }

        .sidebar-logo img {
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-sm);
            transition: transform 0.3s ease;
        }

        .sidebar-logo img:hover {
            transform: scale(1.02);
        }

        .sidebar-logo .caption {
            text-align: center;
            margin-top: 0.5rem;
            color: #0A04AA;
            font-weight: 500;
        }
        .metric-box {
            border-radius: 30px;
            padding: 1px;
            margin: 10px;
            text-align: center;
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
            transition: all 0.5s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            height: 160px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
        .metric-box:hover {
            transform: scale(1.1) rotate(0deg);
            box-shadow: 0 20px 50px rgba(0,0,0,0.4);
        }
        .metric-box h1 {
            font-size: 40px;
            color: #1914B3;
            text-shadow: 2px 2px 6px rgba(0,0,0,0.4);
        }
        .metric-box p {
            font-size: 22px;
            color: #1914B3;
            margin: 15px 0 0 0;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.3);
            z-index: 1;
            font-weight: bold;
        }
        /* Pied de page */
        .footer {
            background-color: white;
            padding: 1.5rem;
            margin-top: 2rem;
            border-radius: var(--border-radius) var(--border-radius) 0 0;
            box-shadow: var(--shadow-sm);
            text-align: center;
        }
        /* Style général des labels de filtre */
        .stMultiSelect [data-baseweb="tag"] {
            background-color: #0A04AA !important;
            color: white !important;
            font-weight: bold !important;
        }
        .dashboard-header h3 {
            text-align: center;
            font-size: 1.5rem;
            color: #0A04AA;
            font-weight: 600;
            margin: 0;
            text-transform: uppercase;
        }
        /* ============ RADIO BUTTONS ============ */
        div[role="radiogroup"] > :first-child {
            border-color: #1914B3 !important;
            color: #1914B3 !important;
        }
        
        div[role="radiogroup"] > label > div:first-child {
            background-color: #1914B3 !important;
        }
        
        /* ============ NUMBER INPUT ============ */
        input[type="number"] {
            border-color: #1914B3 !important;
            color: #1914B3 !important;
        }
        
        /* ============ SELECTBOX ============ */
        div[data-baseweb="select"] > div {
            border-color: #1914B3 !important;
        }
        
        div[data-baseweb="select"] svg {
            color: #1914B3 !important;
        }
        
        /* ============ SLIDER ============ */
        div[data-testid="stSlider"] > div > div > div > div {
            background-color: #1914B3 !important;
        }
        
        div[data-testid="stSlider"] > div > div > div > div[role="slider"] {
            box-shadow: 0 0 0 1px #1914B3 !important;
        }
        
        /* ============ TEXT INPUT ============ */
        input[type="text"], input[type="password"] {
            border-color: #1914B3 !important;
            color: #1914B3 !important;
        }
        
        /* ============ ÉTATS COMMUNS (HOVER/FOCUS) ============ */
        div[role="radiogroup"] > label:hover > div:first-child,
        input[type="number"]:focus,
        div[data-baseweb="select"]:hover > div,
        input[type="text"]:focus,
        input[type="password"]:focus {
            box-shadow: 0 0 0 1px #1914B3 !important;
            border-color: #1914B3 !important;
        }
        
        /* ============ LABELS COMMUNS ============ */
        .stRadio > label,
        .stNumberInput > label,
        .stSelectbox > label,
        .stSlider > label,
        .stTextInput > label {
            color: #1914B3 !important;
            font-weight: 500 !important;
        }
        
        /* ============ STREAMLIT SPÉCIFIQUE ============ */
        .stNumberInput > div > div > input,
        .stTextInput > div > div > input {
            color: #1914B3 !important;
        }
        
        .stSelectbox > div > div > div > div {
            color: #1914B3 !important;
        }
        :root {
        --slider-primary: #1914B3;
        --slider-inactive: #E0E0E0;
        --slider-handle: white;
        }
        
        div[data-testid="stSlider"] > div > div > div > div {
            background-color: var(--slider-primary) !important;
        }
        
        div[data-testid="stSlider"] > div > div > div > div[role="slider"] {
            background-color: var(--slider-primary) !important;
            border-color: var(--slider-handle) !important;
        }
        
        div[data-testid="stSlider"] > div > div > div > div > div {
            background-color: var(--slider-inactive) !important;
        }
        
            /* ============ HEADERS ============ */
        h1, h2, h3, h4, h5, h6 {
            color: #1914B3 !important;
        }
        
        /* Cible spécifiquement les composants Streamlit */
        .stHeader, .stSubheader, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #1914B3 !important;
            font-family: 'Arial Black', sans-serif !important;
        }
        
        /* ============ BOUTON SUBMIT ============ */
        div.stButton > button:first-child {
            background-color: #1914B3 !important;
            color: white !important;
            border-radius: 8px !important;
            border: 1px solid #1914B3 !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
        }
        
        div.stButton > button:first-child:hover {
            background-color: #100A8C !important;
            border-color: #100A8C !important;
            transform: scale(1.02) !important;
        }
        
        div.stButton > button:first-child:focus {
            box-shadow: 0 0 0 0.2rem rgba(25, 20, 179, 0.5) !important;
        }
        
        /* ============ FORMULAIRE ============ */
        div.stForm {
            border: 1px solid rgba(25, 20, 179, 0.2) !important;
            border-radius: 10px !important;
            padding: 1.5rem !important;
            background-color: rgba(25, 20, 179, 0.03) !important;
        }
        
        /* Style pour le bouton dans un formulaire */
        div.stForm form > div:last-child > div > button {
            width: 100% !important;
            padding: 0.5rem !important;
            font-size: 1.1rem !important;
        }
            </style>
        """,
        unsafe_allow_html=True
    )
  