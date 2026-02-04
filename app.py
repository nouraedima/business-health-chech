import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_analyzer import DataAnalyzer

# Configuration de la page
st.set_page_config(
    page_title="Business Data Health Check",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour un design moderne et pro
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Style général */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .block-container {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    /* Header principal */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .sub-header {
        font-size: 1.3rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Header avec créateur */
    .creator-header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .creator-name {
        font-size: 1.1rem;
        color: #333;
        margin-top: 0.5rem;
    }
    
    .creator-name a {
        color: #667eea;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .creator-name a:hover {
        color: #764ba2;
        text-decoration: underline;
    }
    
    /* Cards et alertes */
    .alert-critical {
        background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #f44336;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(244, 67, 54, 0.1);
        animation: slideInLeft 0.5s ease-out;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fffbf0 0%, #ffe8cc 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #ff9800;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(255, 152, 0, 0.1);
        animation: slideInLeft 0.5s ease-out;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #f0fdf4 0%, #d1fae5 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 5px solid #4caf50;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(76, 175, 80, 0.1);
        animation: slideInLeft 0.5s ease-out;
    }
    
    /* Dividers stylés */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    
    /* Boutons stylés */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .footer a {
        color: white;
        text-decoration: none;
        font-weight: 600;
        border-bottom: 2px solid white;
        transition: all 0.3s ease;
    }
    
    .footer a:hover {
        border-bottom: 2px solid #ffd700;
        color: #ffd700;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Section titles */
    h3 {
        color: #667eea;
        font-weight: 700;
        margin-top: 2rem;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 5px solid #667eea;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 10px;
        font-weight: 600;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    """Fonction principale de l'application"""
    
    # En-tête avec infos créateur
    st.markdown("""
        <div class="creator-header">
            <div class="main-header">📊 Business Data Health Check</div>
            <div class="sub-header">Comprenez vos données business en 5 minutes, sans être expert</div>
            <div class="creator-name">
                Créé par <a href="https://www.linkedin.com/in/noura-mboutto-babb1b330" target="_blank">Noura Edima Mboutto</a> | 
                Étudiante en Développement Web | Data & IA
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialiser la session state
    if 'analyzed' not in st.session_state:
        st.session_state.analyzed = False
    
    # Étape 1: Upload du fichier
    st.markdown("---")
    st.markdown("### 📁 Étape 1 : Importer vos données")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choisissez un fichier CSV ou Excel",
            type=['csv', 'xlsx'],
            help="Votre fichier doit contenir au minimum les colonnes : date, client_id, montant, statut"
        )
    
    with col2:
        st.info("**📋 Format attendu :**\n\n✓ date\n\n✓ client_id\n\n✓ montant\n\n✓ statut")
        
        # Bouton pour télécharger l'exemple
        try:
            with open('exemple_ventes.csv', 'rb') as f:
                st.download_button(
                    label="📥 Télécharger un exemple",
                    data=f,
                    file_name="exemple_ventes.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        except:
            st.warning("Fichier exemple non trouvé")
    
    if uploaded_file is not None:
        try:
            # Charger les données
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Vérifier les colonnes requises
            required_columns = ['date', 'client_id', 'montant', 'statut']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"❌ Colonnes manquantes : {', '.join(missing_columns)}")
                st.stop()
            
            st.success(f"✅ Fichier chargé avec succès ! **{len(df)} lignes** détectées")
            
            # Étape 2: Questions de contexte
            st.markdown("---")
            st.markdown("### 🎯 Étape 2 : Personnalisez votre analyse")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                activite = st.selectbox(
                    "🏢 Type d'activité",
                    ["E-commerce", "Service (SaaS, consulting...)", "Autre"]
                )
            
            with col2:
                objectif = st.selectbox(
                    "🎯 Objectif principal",
                    ["Augmenter les ventes", "Fidéliser les clients", "Optimiser la rentabilité"]
                )
            
            with col3:
                # Détecter automatiquement la période
                df_temp = df.copy()
                df_temp['date'] = pd.to_datetime(df_temp['date'])
                date_min = df_temp['date'].min().strftime('%m/%Y')
                date_max = df_temp['date'].max().strftime('%m/%Y')
                
                st.text_input(
                    "📅 Période analysée",
                    value=f"{date_min} - {date_max}",
                    disabled=True
                )
            
            # Bouton d'analyse
            st.markdown("---")
            if st.button("🚀 Analyser mes données", type="primary", use_container_width=True):
                st.session_state.analyzed = True
                st.session_state.df = df
                st.session_state.activite = activite
                st.session_state.objectif = objectif
                st.rerun()
            
            # Afficher les résultats si analysé
            if st.session_state.analyzed and 'df' in st.session_state:
                show_results(st.session_state.df, st.session_state.activite, st.session_state.objectif)
                
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement du fichier : {str(e)}")
    
    else:
        # Message d'accueil si pas de fichier
        st.markdown("---")
        st.info("👆 **Commencez par importer un fichier CSV ou Excel pour démarrer l'analyse**")
        
        # Exemple de données attendues
        with st.expander("💡 Voir un exemple de structure de données attendue"):
            st.code("""
date,client_id,montant,statut
2024-01-15,C001,120.50,complete
2024-01-18,C002,85.00,complete
2024-01-22,C001,95.30,complete
            """, language="csv")
    
    # Footer
    st.markdown("""
        <div class="footer">
            <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">💼 Vous recrutez un Data Analyst ?</p>
            <p style="font-size: 1rem;">
                Je suis <a href="https://www.linkedin.com/in/noura-mboutto-babb1b330" target="_blank">Noura Edima Mboutto</a>, 
                étudiante en Développement Web | Data & IA,<br>
                actuellement à la recherche d'une <strong>alternance en Data Analyst</strong>.
            </p>
            <p style="font-size: 0.9rem; margin-top: 1rem; opacity: 0.9;">
                📧 Contactez-moi via <a href="https://www.linkedin.com/in/noura-mboutto-babb1b330" target="_blank">LinkedIn</a>
            </p>
        </div>
    """, unsafe_allow_html=True)

def show_results(df, activite, objectif):
    """Affiche les résultats de l'analyse"""
    
    st.markdown("---")
    st.markdown("## 📊 Résultats de votre analyse")
    
    # Créer l'analyseur
    with st.spinner("🔍 Analyse en cours..."):
        analyzer = DataAnalyzer(df)
        kpis = analyzer.get_kpis()
        alerts = analyzer.detect_alerts(kpis)
        recommendations = analyzer.get_recommendations(kpis, alerts)
        score, statut = analyzer.get_health_score(kpis)
    
    # Score de santé global
    st.markdown("### 🎯 Santé Globale de votre Activité")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Jauge de score
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': statut, 'font': {'size': 24, 'color': '#667eea'}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 40], 'color': "#ffebee"},
                    {'range': [40, 60], 'color': "#fff3e0"},
                    {'range': [60, 80], 'color': "#e3f2fd"},
                    {'range': [80, 100], 'color': "#e8f5e9"}
                ],
                'threshold': {
                    'line': {'color': "#764ba2", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300, font={'family': 'Inter'})
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Indicateurs clés
    st.markdown("### 📈 Indicateurs Clés")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Chiffre d'Affaires",
            value=f"{kpis['ca_total']:,.0f} €",
            delta=f"{kpis['evolution_ca']:.1f}%" if kpis['evolution_ca'] != 0 else None
        )
    
    with col2:
        st.metric(
            label="🛒 Panier Moyen",
            value=f"{kpis['panier_moyen']:.2f} €",
            delta=f"{kpis['evolution_panier']:.1f}%" if kpis['evolution_panier'] != 0 else None
        )
    
    with col3:
        st.metric(
            label="🔁 Taux de Rétention",
            value=f"{kpis['taux_retention']:.0f} %"
        )
    
    with col4:
        st.metric(
            label="👥 Clients Uniques",
            value=f"{kpis['nb_clients']}"
        )
    
    # Graphiques
    st.markdown("---")
    st.markdown("### 📊 Évolution dans le Temps")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Évolution du CA mensuel
        ca_mensuel_df = kpis['ca_mensuel'].reset_index()
        ca_mensuel_df.columns = ['Mois', 'CA']
        ca_mensuel_df['Mois'] = ca_mensuel_df['Mois'].astype(str)
        
        fig = px.line(
            ca_mensuel_df,
            x='Mois',
            y='CA',
            title='📈 Évolution du Chiffre d\'Affaires Mensuel',
            markers=True
        )
        fig.update_traces(line_color='#667eea', line_width=3, marker=dict(size=8))
        fig.update_layout(
            xaxis_title="Mois",
            yaxis_title="CA (€)",
            hovermode='x unified',
            font={'family': 'Inter'},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Distribution des clients par nombre d'achats
        achats_par_client = analyzer.df.groupby('client_id').size().value_counts().sort_index()
        
        fig = px.bar(
            x=achats_par_client.index,
            y=achats_par_client.values,
            title='👥 Répartition des Clients par Nombre d\'Achats',
            labels={'x': 'Nombre d\'achats', 'y': 'Nombre de clients'}
        )
        fig.update_traces(marker_color='#764ba2')
        fig.update_layout(
            font={'family': 'Inter'},
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Alertes
    st.markdown("---")
    st.markdown("### 🚨 Alertes et Opportunités")
    
    # Alertes critiques
    if alerts['critiques']:
        for alert in alerts['critiques']:
            st.markdown(f"""
                <div class="alert-critical">
                    <strong>{alert['titre']}</strong><br>
                    {alert['description']}
                </div>
            """, unsafe_allow_html=True)
    
    # Warnings
    if alerts['warnings']:
        for alert in alerts['warnings']:
            st.markdown(f"""
                <div class="alert-warning">
                    <strong>{alert['titre']}</strong><br>
                    {alert['description']}
                </div>
            """, unsafe_allow_html=True)
    
    # Opportunités
    if alerts['opportunites']:
        for alert in alerts['opportunites']:
            st.markdown(f"""
                <div class="alert-success">
                    <strong>{alert['titre']}</strong><br>
                    {alert['description']}
                </div>
            """, unsafe_allow_html=True)
    
    if not alerts['critiques'] and not alerts['warnings'] and not alerts['opportunites']:
        st.info("✅ Aucune alerte détectée. Votre activité semble stable !")
    
    # Recommandations
    st.markdown("---")
    st.markdown("### 💡 Recommandations Actionnables")
    
    for i, reco in enumerate(recommendations, 1):
        priorite_emoji = "🔴" if reco['priorite'] == 'haute' else "🟡" if reco['priorite'] == 'moyenne' else "🟢"
        
        with st.expander(f"{priorite_emoji} {reco['action']}", expanded=(i == 1)):
            st.write(reco['details'])
    
    # Statistiques détaillées
    st.markdown("---")
    st.markdown("### 📋 Statistiques Détaillées")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📊 Métriques générales**")
        st.write(f"• Nombre total de transactions : **{kpis['nb_transactions']}**")
        st.write(f"• Fréquence d'achat moyenne : **{kpis['freq_achat_moyenne']:.2f}**")
        st.write(f"• Concentration du CA (top 20%) : **{kpis['concentration_ca']:.1f}%**")
    
    with col2:
        st.markdown("**📅 Période d'analyse**")
        date_min = analyzer.df['date'].min().strftime('%d/%m/%Y')
        date_max = analyzer.df['date'].max().strftime('%d/%m/%Y')
        st.write(f"• Début : **{date_min}**")
        st.write(f"• Fin : **{date_max}**")
        st.write(f"• Durée : **{(analyzer.df['date'].max() - analyzer.df['date'].min()).days} jours**")
    
    # Boutons d'action
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Nouvelle Analyse", use_container_width=True):
            st.session_state.analyzed = False
            st.rerun()
    
    with col2:
        st.button("💾 Télécharger le Rapport PDF", use_container_width=True, disabled=True, help="Fonctionnalité à venir")
    
    with col3:
        st.button("📤 Partager sur LinkedIn", use_container_width=True, disabled=True, help="Fonctionnalité à venir")

if __name__ == "__main__":
    main()