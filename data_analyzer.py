import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class DataAnalyzer:
    """Classe pour analyser les données business et générer des insights"""
    
    def __init__(self, df):
        """
        Initialise l'analyseur avec un DataFrame
        
        Args:
            df: DataFrame pandas avec colonnes [date, client_id, montant, statut]
        """
        self.df = df.copy()
        self._prepare_data()
        
    def _prepare_data(self):
        """Prépare les données pour l'analyse"""
        # Convertir la colonne date en datetime
        self.df['date'] = pd.to_datetime(self.df['date'])
        
        # Filtrer uniquement les transactions complètes
        self.df = self.df[self.df['statut'] == 'complete'].copy()
        
        # Trier par date
        self.df = self.df.sort_values('date')
        
        # Extraire mois et année
        self.df['mois'] = self.df['date'].dt.to_period('M')
        
    def get_kpis(self):
        """
        Calcule les KPIs principaux
        
        Returns:
            dict: Dictionnaire contenant tous les KPIs
        """
        kpis = {}
        
        # 1. Chiffre d'affaires total
        kpis['ca_total'] = self.df['montant'].sum()
        
        # 2. Nombre de transactions
        kpis['nb_transactions'] = len(self.df)
        
        # 3. Panier moyen
        kpis['panier_moyen'] = self.df['montant'].mean()
        
        # 4. Nombre de clients uniques
        kpis['nb_clients'] = self.df['client_id'].nunique()
        
        # 5. Fréquence d'achat moyenne
        achats_par_client = self.df.groupby('client_id').size()
        kpis['freq_achat_moyenne'] = achats_par_client.mean()
        
        # 6. CA par mois
        kpis['ca_mensuel'] = self.df.groupby('mois')['montant'].sum()
        
        # 7. Évolution CA (dernier mois vs avant-dernier)
        if len(kpis['ca_mensuel']) >= 2:
            dernier_mois = kpis['ca_mensuel'].iloc[-1]
            avant_dernier = kpis['ca_mensuel'].iloc[-2]
            kpis['evolution_ca'] = ((dernier_mois - avant_dernier) / avant_dernier) * 100
        else:
            kpis['evolution_ca'] = 0
            
        # 8. Taux de rétention (clients qui achètent plusieurs fois)
        clients_recurrents = (achats_par_client > 1).sum()
        kpis['taux_retention'] = (clients_recurrents / kpis['nb_clients']) * 100
        
        # 9. Concentration du CA (part des top 20%)
        ca_par_client = self.df.groupby('client_id')['montant'].sum().sort_values(ascending=False)
        nb_top_clients = max(1, int(len(ca_par_client) * 0.2))
        ca_top_clients = ca_par_client.head(nb_top_clients).sum()
        kpis['concentration_ca'] = (ca_top_clients / kpis['ca_total']) * 100
        
        # 10. Évolution du panier moyen (2 derniers mois)
        if len(kpis['ca_mensuel']) >= 2:
            dernier_mois_dates = self.df[self.df['mois'] == self.df['mois'].iloc[-1]]
            avant_dernier_mois_dates = self.df[self.df['mois'] == self.df['mois'].iloc[-2]]
            
            panier_dernier = dernier_mois_dates['montant'].mean()
            panier_avant = avant_dernier_mois_dates['montant'].mean()
            
            kpis['evolution_panier'] = ((panier_dernier - panier_avant) / panier_avant) * 100
        else:
            kpis['evolution_panier'] = 0
            
        return kpis
    
    def detect_alerts(self, kpis):
        """
        Détecte les alertes et opportunités
        
        Args:
            kpis: Dictionnaire des KPIs calculés
            
        Returns:
            dict: Alertes et opportunités détectées
        """
        alerts = {
            'critiques': [],
            'warnings': [],
            'opportunites': []
        }
        
        # Alerte 1: Baisse du CA
        if kpis['evolution_ca'] < -10:
            alerts['critiques'].append({
                'titre': ' Baisse significative du CA',
                'description': f"Le CA a baissé de {abs(kpis['evolution_ca']):.1f}% sur le dernier mois"
            })
        
        # Alerte 2: Baisse du panier moyen
        if kpis['evolution_panier'] < -5:
            alerts['warnings'].append({
                'titre': ' Diminution du panier moyen',
                'description': f"Le panier moyen a baissé de {abs(kpis['evolution_panier']):.1f}% sur le dernier mois"
            })
        
        # Alerte 3: Faible taux de rétention
        if kpis['taux_retention'] < 30:
            alerts['warnings'].append({
                'titre': ' Taux de rétention faible',
                'description': f"Seulement {kpis['taux_retention']:.0f}% de vos clients reviennent acheter"
            })
        
        # Alerte 4: Forte concentration du CA
        if kpis['concentration_ca'] > 70:
            alerts['warnings'].append({
                'titre': ' Concentration du CA élevée',
                'description': f"Les 20% meilleurs clients génèrent {kpis['concentration_ca']:.0f}% du CA (risque de dépendance)"
            })
        
        # Opportunité 1: Bonne rétention
        if kpis['taux_retention'] > 50:
            alerts['opportunites'].append({
                'titre': ' Excellente fidélité client',
                'description': f"{kpis['taux_retention']:.0f}% de clients fidèles : investir dans un programme de fidélité pourrait maximiser leur valeur"
            })
        
        # Opportunité 2: Croissance du CA
        if kpis['evolution_ca'] > 15:
            alerts['opportunites'].append({
                'titre': ' Forte croissance détectée',
                'description': f"CA en hausse de {kpis['evolution_ca']:.1f}% : moment idéal pour accélérer (marketing, stock, équipe)"
            })
        
        return alerts
    
    def get_recommendations(self, kpis, alerts):
        """
        Génère des recommandations actionnables
        
        Args:
            kpis: Dictionnaire des KPIs
            alerts: Alertes détectées
            
        Returns:
            list: Liste des recommandations
        """
        recommendations = []
        
        # Recommandations basées sur la rétention
        if kpis['taux_retention'] < 30:
            recommendations.append({
                'priorite': 'haute',
                'action': 'Lancer une campagne de réactivation',
                'details': 'Identifier les clients qui n\'ont acheté qu\'une fois et leur proposer une offre ciblée (réduction, code promo)'
            })
        
        # Recommandations basées sur le panier moyen
        if kpis['evolution_panier'] < -5:
            recommendations.append({
                'priorite': 'moyenne',
                'action': 'Analyser la baisse du panier moyen',
                'details': 'Vérifier si c\'est lié à : plus de petits achats, moins de ventes premium, ou changement dans le mix produit'
            })
            
            recommendations.append({
                'priorite': 'moyenne',
                'action': 'Mettre en place des stratégies d\'upsell',
                'details': 'Suggestions de produits complémentaires, seuils de livraison gratuite, bundles'
            })
        
        # Recommandations basées sur la concentration
        if kpis['concentration_ca'] > 70:
            recommendations.append({
                'priorite': 'haute',
                'action': 'Diversifier votre base client',
                'details': 'Trop de dépendance envers quelques clients. Investir dans l\'acquisition pour réduire le risque'
            })
        
        # Recommandations générales
        if kpis['freq_achat_moyenne'] < 2:
            recommendations.append({
                'priorite': 'moyenne',
                'action': 'Augmenter la fréquence d\'achat',
                'details': 'Newsletter régulière, programme de fidélité, rappels par email'
            })
        
        # Si pas de problèmes majeurs
        if len(alerts['critiques']) == 0 and len(alerts['warnings']) <= 1:
            recommendations.append({
                'priorite': 'basse',
                'action': 'Continuer sur cette lancée',
                'details': 'Votre activité est saine. Focus sur l\'optimisation et la croissance progressive'
            })
        
        return recommendations
    
    def get_health_score(self, kpis):
        """
        Calcule un score de santé global (0-100)
        
        Args:
            kpis: Dictionnaire des KPIs
            
        Returns:
            tuple: (score, statut)
        """
        score = 100
        
        # Pénalités
        if kpis['evolution_ca'] < -10:
            score -= 20
        elif kpis['evolution_ca'] < 0:
            score -= 10
            
        if kpis['taux_retention'] < 30:
            score -= 15
        elif kpis['taux_retention'] < 50:
            score -= 5
            
        if kpis['evolution_panier'] < -5:
            score -= 10
            
        if kpis['concentration_ca'] > 70:
            score -= 10
        
        # Déterminer le statut
        if score >= 80:
            statut = "Excellente"
        elif score >= 60:
            statut = "Bonne"
        elif score >= 40:
            statut = "Moyenne"
        else:
            statut = "À surveiller"
        
        return score, statut