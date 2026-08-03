"""
spv_wallet.py
Ce fichier simule un portefeuille Bitcoin SPV sur un téléphone mobile.
Un portefeuille SPV (Simple Payment Verification) est un portefeuille léger.
"""

class Pair:
    """
    Un Pair = un ordinateur connecté au portefeuille
    """
    def __init__(self, id, est_malveillant=False):
        self.id = id                    # L'identifiant du pair
        self.est_malveillant = est_malveillant  # True si contrôlé par l'attaquant
    
    def __str__(self):
        statut = "🔴 malveillant" if self.est_malveillant else " 🟢 honnête"
        return f"Pair {self.id} ({statut})"


class SPVWallet:
    """
    Le portefeuille SPV sur le téléphone.
    Il se connecte à des pairs pour vérifier les transactions.
    """
    
    def __init__(self, nom_utilisateur="victime"):
        self.nom = nom_utilisateur
        self.pairs = []                    # Liste des pairs connectés
        self.max_pairs = 8                 # Le téléphone peut avoir 8 connexions max
        self.etat = "CONNECTÉ"             # CONNECTÉ, RECONNEXION, ÉCLIPSÉ
        print(f"  Portefeuille {self.nom} créé")
    
    def ajouter_pair(self, pair):
        """
        Ajoute un pair au portefeuille s'il y a de la place.
        """
        if len(self.pairs) >= self.max_pairs:
            print(f"  Impossible d'ajouter {pair.id} : plus de place")
            return False
        
        # Vérifier que le pair n'est pas déjà connecté
        for p in self.pairs:
            if p.id == pair.id:
                print(f"⚠️ {pair.id} est déjà connecté")
                return False
        
        self.pairs.append(pair)
        print(f"  {pair.id} connecté à {self.nom}")
        return True
    
    def supprimer_pair(self, pair_id):
        """
        Supprime un pair du portefeuille.
        """
        for i, p in enumerate(self.pairs):
            if p.id == pair_id:
                del self.pairs[i]
                print(f"🗑️ {pair_id} déconnecté")
                return True
        print(f"⚠️{pair_id} n'est pas connecté")
        return False
    
    def compter_malveillants(self):
        """
        Compte combien de pairs sont malveillants.
        """
        compte = 0
        for p in self.pairs:
            if p.est_malveillant:
                compte += 1
        return compte
    
    def taux_attaque(self):
        """
        Calcule le pourcentage de pairs malveillants (0% à 100%).
        """
        if len(self.pairs) == 0:
            return 0.0
        return (self.compter_malveillants() / len(self.pairs)) * 100
    
    def est_clipse(self):
        """
        Vérifie si le portefeuille est complètement éclipsé.
        Une éclipse = TOUTES les connexions sont malveillantes.
        """
        if len(self.pairs) == self.max_pairs:
            if self.compter_malveillants() == self.max_pairs:
                self.etat = "ÉCLIPSÉ"
                return True
        return False
    
    def afficher_etat(self):
        """
        Affiche l'état actuel du portefeuille.
        """
        print("\n" + "="*50)
        print(f"   PORTEFEUILLE: {self.nom}")
        print(f"   État: {self.etat}")
        print(f"   Connexions: {len(self.pairs)}/{self.max_pairs}")
        print(f"   Pairs malveillants: {self.compter_malveillants()}")
        print(f"   Taux d'attaque: {self.taux_attaque():.1f}%")
        print("="*50)
        
        # Afficher la liste des pairs
        for p in self.pairs:
            print(f"   → {p}")
