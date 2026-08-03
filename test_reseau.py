"""
test_reseau.py
Teste le réseau mobile 3G/4G
"""

import random
from src.mobile_network import MobileNetwork

print("="*60)
print("📶 TEST DU RÉSEAU MOBILE")
print("="*60)

# 1. Créer un réseau
print("\n1️ Création du réseau")
reseau = MobileNetwork(vitesse_kmh=4.0)  # Piéton

# 2. Simuler 50 secondes de mouvement
print("\n2️ Simulation de 50 secondes de mouvement")
print("-"*40)

for seconde in range(50):
    # Bouger
    reseau.bouger(duree=1.0)
    
    # Vérifier si handover
    if random.random() < reseau.probabilite_handover():
        reseau.nb_handovers += 1
        print(f"  🔄 Handover à t={seconde}s")
    
    # Vérifier perte de connexion
    if reseau.perdre_connexion():
        print(f"  ❌ Perte de connexion à t={seconde}s")
    
    # Afficher toutes les 10 secondes
    if seconde % 10 == 0:
        print(f"  t={seconde}s: signal={reseau.signal*100:.0f}%, position=({reseau.position_x:.0f},{reseau.position_y:.0f})")

# 3. Résumé (en dehors de la boucle)
print("\n3️ RÉSUMÉ")
print("-"*40)
reseau.afficher()
