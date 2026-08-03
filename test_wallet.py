"""
test_wallet.py
Ce fichier teste notre portefeuille pour comprendre son fonctionnement.
"""

# Importer notre portefeuille
from src.spv_wallet import SPVWallet, Pair

print("="*60)
print(" TEST DU PORTEFEUILLE SPV")
print("="*60)

# 1. Créer un portefeuille
print("\n1️⃣ Création du portefeuille")
mon_wallet = SPVWallet("Mon_Téléphone")

# 2. Créer des pairs
print("\n2️⃣ Création des pairs")
pairs_honnettes = [
    Pair("Ami_001", est_malveillant=False),
    Pair("Ami_002", est_malveillant=False),
    Pair("Ami_003", est_malveillant=False),
    Pair("Ami_004", est_malveillant=False),
]

pairs_malveillants = [
    Pair("Hacker_001", est_malveillant=True),
    Pair("Hacker_002", est_malveillant=True),
    Pair("Hacker_003", est_malveillant=True),
    Pair("Hacker_004", est_malveillant=True),
]

# 3. Ajouter 4 pairs honnêtes
print("\n3️⃣ Ajout de pairs honnêtes")
for pair in pairs_honnettes:
    mon_wallet.ajouter_pair(pair)

mon_wallet.afficher_etat()

# 4. Ajouter 4 pairs malveillants (pour remplir le wallet)
print("\n4️⃣ Ajout de pairs malveillants")
for pair in pairs_malveillants:
    mon_wallet.ajouter_pair(pair)

mon_wallet.afficher_etat()

# 5. Vérifier si éclipsé
print("\n5️⃣ Vérification de l'éclipse")
if mon_wallet.est_clipse():
    print("⚠️  ATTENTION ! Le portefeuille est ÉCLIPSÉ !")
    print("   Toutes les connexions sont contrôlées par l'attaquant.")
else:
    print("✅ Le portefeuille est sécurisé.")
