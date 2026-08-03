"""
mobile_network.py
Ce fichier simule un réseau mobile 3G/4G avec :
- Qualité du signal
- Mobilité du téléphone
- Pertes de connexion
"""

import random
import math

class MobileNetwork:
    """
    Simule un réseau mobile 3G/4G
    """
    
    def __init__(self, vitesse_kmh=4.0):
        """
        Initialise le réseau mobile.
        vitesse_kmh : vitesse de déplacement du téléphone (km/h)
        4 km/h = vitesse d'un piéton
        """
        self.vitesse = vitesse_kmh
        
        # Position du téléphone (x, y) en mètres
        self.position_x = random.uniform(-500, 500)
        self.position_y = random.uniform(-500, 500)
        
        # Direction du mouvement (en radians)
        self.direction = random.uniform(0, 2 * math.pi)
        
        # Qualité du signal (0 = pas de signal, 1 = signal parfait)
        self.signal = 1.0
        
        # État de la connexion
        self.connecte = True
        
        # Compteurs
        self.nb_handovers = 0
        self.nb_deconnexions = 0
        
        # Position de l'antenne relais (centre de la zone)
        self.antenne_x = 0
        self.antenne_y = 0
        self.rayon_zone = 500  # En mètres
        
        print(f"📶 Réseau mobile créé (vitesse: {vitesse_kmh} km/h)")
    
    def bouger(self, duree=1.0):
        """
        Déplace le téléphone pendant 'duree' secondes.
        """
        # Convertir km/h en m/s
        vitesse_ms = self.vitesse / 3.6
        
        # Calculer la distance parcourue
        distance = vitesse_ms * duree
        
        # Nouvelle position
        self.position_x += distance * math.cos(self.direction)
        self.position_y += distance * math.sin(self.direction)
        
        # Si on sort de la zone, on rebondit
        if abs(self.position_x) > self.rayon_zone:
            self.position_x = self.position_x * -0.9
            self.direction = math.pi - self.direction
        
        if abs(self.position_y) > self.rayon_zone:
            self.position_y = self.position_y * -0.9
            self.direction = -self.direction
        
        # Changer un peu la direction (mouvement aléatoire)
        self.direction += random.uniform(-0.2, 0.2)
        self.direction = self.direction % (2 * math.pi)
        
        # Mettre à jour la qualité du signal
        self._mettre_a_jour_signal()
    
    def _mettre_a_jour_signal(self):
        """
        Calcule la qualité du signal en fonction de la distance à l'antenne.
        Plus on est loin, plus le signal est faible.
        """
        # Distance à l'antenne
        distance = math.sqrt(
            (self.position_x - self.antenne_x)**2 + 
            (self.position_y - self.antenne_y)**2
        )
        
        # Calcul du signal (plus on est loin, plus il baisse)
        if distance == 0:
            signal = 1.0
        else:
            # Le signal diminue avec la distance
            signal = 1.0 / (1 + (distance / self.rayon_zone) * 2)
        
        # Ajouter un peu de bruit (fading)
        bruit = random.uniform(-0.1, 0.1)
        self.signal = max(0, min(1, signal + bruit))
    
    def probabilite_handover(self):
        """
        Probabilité qu'un handover (changement d'antenne) se produise.
        Plus le signal est faible, plus la probabilité est élevée.
        """
        if self.signal < 0.2:
            return 0.8
        elif self.signal < 0.4:
            return 0.4
        elif self.signal < 0.6:
            return 0.1
        else:
            return 0.02
    
    def perdre_connexion(self):
        """
        Simule une perte de connexion.
        Retourne True si la connexion est perdue.
        """
        # Probabilité de perte de connexion
        # Plus le signal est faible, plus la probabilité est élevée
        proba = max(0, (1 - self.signal) * 0.6)
        
        if random.random() < proba:
            self.connecte = False
            self.nb_deconnexions += 1
            return True
        
        self.connecte = True
        return False
    
    def afficher(self):
        """
        Affiche l'état du réseau.
        """
        print("\n📶 ÉTAT DU RÉSEAU MOBILE")
        print(f"   Position: ({self.position_x:.0f}, {self.position_y:.0f}) m")
        print(f"   Signal: {self.signal*100:.0f}%")
        print(f"   Connecté: {'✅ Oui' if self.connecte else '❌ Non'}")
        print(f"   Handovers: {self.nb_handovers}")
        print(f"   Déconnexions: {self.nb_deconnexions}")
