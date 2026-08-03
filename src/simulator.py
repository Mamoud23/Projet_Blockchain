"""
simulator.py
Simulateur complet de l'attaque par éclipse
Combine : portefeuille + réseau mobile + attaquant
"""

import random
from src.spv_wallet import SPVWallet, Pair
from src.mobile_network import MobileNetwork

class Simulator:
    """
    Simulateur de l'attaque par éclipse
    """
    
    def __init__(self, config):
        """
        Initialise le simulateur avec une configuration.
        config = {
            'max_connexions': 8,
            'duree': 300,  # en secondes
            'vitesse': 4.0,  # km/h
            'intensite_attaque': 0.15  # 15% de chances par seconde
        }
        """
        self.config = config
        
        # Créer le portefeuille
        self.wallet = SPVWallet("Téléphone_Victime")
        
        # Créer le réseau mobile
        self.reseau = MobileNetwork(vitesse_kmh=config.get('vitesse', 4.0))
        
        # Variables de suivi
        self.temps = 0
        self.eclipse_reussie = False
        
        # Créer des pairs honnêtes initiaux
        self._creer_pairs_initiaux()
        
        print("\n🚀 SIMULATEUR PRÊT")
        print(f"   Connexions max: {self.wallet.max_pairs}")
        print(f"   Durée: {config.get('duree', 300)}s")
        print(f"   Vitesse: {self.reseau.vitesse} km/h")
        print(f"   Intensité attaque: {config.get('intensite_attaque', 0.15)}")
    
    def _creer_pairs_initiaux(self):
        """
        Crée 4 pairs honnêtes pour le démarrage.
        """
        for i in range(4):
            pair = Pair(f"Ami_{i+1:03d}", est_malveillant=False)
            self.wallet.ajouter_pair(pair)
    
    def _creer_pair_malveillant(self):
        """
        Crée un pair contrôlé par l'attaquant.
        """
        return Pair(f"Hacker_{random.randint(0, 9999):04d}", est_malveillant=True)
    
    def _attaquer(self):
        """
        L'attaquant essaie de prendre le contrôle du portefeuille.
        """
        # Probabilité d'attaque
        if random.random() > self.config.get('intensite_attaque', 0.15):
            return
        
        # Créer un pair malveillant
        nouveau_hacker = self._creer_pair_malveillant()
        
        # Si le portefeuille est plein, remplacer un pair honnête
        if len(self.wallet.pairs) >= self.wallet.max_pairs:
            # Trouver un pair honnête à remplacer
            honnetes = [p for p in self.wallet.pairs if not p.est_malveillant]
            if honnetes:
                # Remplacer un pair honnête par un malveillant
                victime = random.choice(honnetes)
                self.wallet.supprimer_pair(victime.id)
                self.wallet.ajouter_pair(nouveau_hacker)
                print(f"🔴 {nouveau_hacker.id} a remplacé {victime.id}")
        else:
            # S'il reste de la place, ajouter directement
            self.wallet.ajouter_pair(nouveau_hacker)
    
    def simuler(self):
        """
        Lance la simulation.
        """
        duree = self.config.get('duree', 300)
        
        print("\n" + "="*60)
        print("🔄 DÉMARRAGE DE LA SIMULATION")
        print("="*60)
        
        self.wallet.afficher_etat()
        
        for t in range(duree):
            self.temps = t
            
            # 1. Le téléphone bouge
            self.reseau.bouger(duree=1.0)
            
            # 2. Gérer les handovers
            if random.random() < self.reseau.probabilite_handover():
                self.reseau.nb_handovers += 1
                print(f"🔄 Handover à t={t}s")
                # Pendant un handover, le téléphone est vulnérable
            
            # 3. Gérer les pertes de connexion
            if self.reseau.perdre_connexion():
                print(f"📴 Perte de connexion à t={t}s")
                # L'attaquant profite des pertes de connexion
                # Pour simuler cela, on augmente temporairement l'intensité
                intensite_sauvegardee = self.config['intensite_attaque']
                self.config['intensite_attaque'] = intensite_sauvegardee * 2
                self._attaquer()
                self.config['intensite_attaque'] = intensite_sauvegardee
            else:
                # Attaque normale
                self._attaquer()
            
            # 4. Vérifier si le portefeuille est éclipsé
            if self.wallet.est_clipse() and not self.eclipse_reussie:
                self.eclipse_reussie = True
                print("\n" + "🔥"*20)
                print("⚠️  ÉCLIPSE RÉUSSIE !")
                print(f"   Tous les pairs ({self.wallet.max_pairs}) sont malveillants !")
                print(f"   Temps: {t}s")
                print("🔥"*20 + "\n")
            
            # 5. Afficher l'état toutes les 30 secondes
            if t % 30 == 0 and t > 0:
                print(f"\n--- t={t}s ---")
                print(f"Signal: {self.reseau.signal*100:.0f}%")
                print(f"Pairs: {len(self.wallet.pairs)}/{self.wallet.max_pairs}")
                print(f"Malveillants: {self.wallet.compter_malveillants()}")
        
        # Fin de la simulation
        print("\n" + "="*60)
        print("📊 RÉSULTATS FINAUX")
        print("="*60)
        
        self.wallet.afficher_etat()
        
        print("\n📶 RÉSEAU MOBILE")
        print(f"   Handovers: {self.reseau.nb_handovers}")
        print(f"   Déconnexions: {self.reseau.nb_deconnexions}")
        
        if self.eclipse_reussie:
            print("\n✅ ÉCLIPSE RÉUSSIE !")
        else:
            print("\n❌ ÉCLIPSE ÉCHOUÉE")
            print(f"   Taux d'attaque final: {self.wallet.taux_attaque():.1f}%")
        
        return self.eclipse_reussie
