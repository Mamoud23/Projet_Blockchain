"""
run_simulation.py
Lance la simulation complète de l'attaque par éclipse
"""

from src.simulator import Simulator

print("="*60)
print("🔄 SIMULATION D'ATTAQUE PAR ÉCLIPSE")
print("="*60)

# Configuration de la simulation
config = {
    'max_connexions': 8,      # Nombre max de connexions du wallet
    'duree': 300,              # Durée en secondes (5 minutes)
    'vitesse': 4.0,            # Vitesse en km/h (piéton)
    'intensite_attaque': 0.20  # 20% de chances d'attaque par seconde
}

print("\n📋 CONFIGURATION")
print(f"   Connexions max: {config['max_connexions']}")
print(f"   Durée: {config['duree']}s")
print(f"   Vitesse: {config['vitesse']} km/h")
print(f"   Intensité: {config['intensite_attaque']*100}%")

# Créer et lancer le simulateur
sim = Simulator(config)
resultat = sim.simuler()

print("\n" + "="*60)
print("✅ SIMULATION TERMINÉE")
print("="*60)

if resultat:
    print("🎉 L'attaque par éclipse a RÉUSSI !")
else:
    print("❌ L'attaque par éclipse a ÉCHOUÉ.")
