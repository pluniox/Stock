"""Méthode Counter du module typing, qui permet de compter dans une liste le
nombre d'éléments identiques."""
from typing import Counter


def verif_saisie_produit(saisie):
  """Vérifie la saisie d'un produit et retourne le produit s'il est valide, sinon une
  chaîne vide."""
  if saisie == "":
    print("Saisie vide")
    return ""
  if (65 <= ord(saisie[0]) <= 90) and (49 <= ord(saisie[1]) <= 57):
    return saisie
  else:
    print("Saisie invalide")
    return ""


def verif_saisie_paquet(saisie):
  """Vérifie la saisie d'un paquet de produits et retourne la liste si les produits
  sont valides, sinon une liste vide."""
  paquet = saisie.split(" ")
  produits_valide = []
  for curseur in range(len(paquet)):
    if len(paquet[curseur]) != 2:
      print("Saisie invalide")
      return []
    else:
      element = verif_saisie_produit(paquet[curseur])
      if element == "":
        print("Saisie invalide")
        return []
      else:
        produits_valide.append(element)
  return produits_valide


def sortie_de_produit(liste, paquet):
  """Compare deux listes (Dans ce context ici ce sera le stock de l'entrepôt et 
  un paquet de produits), enlève les premiers éléments correspondants et les renvoie."""
  curseur = 0
  sortie = []
  while curseur < len(liste) and len(paquet) > 0:
    if liste[curseur] in paquet:
      paquet.remove(liste[curseur])
      sortie.append(liste.pop(curseur))
    else:
      curseur += 1
  return sortie


def sortie_en_colis_paquet(stock, paquet):
  """Effectue la sortie d'un paquet de produits du stock (en utilisant
  sortie_de_produit), puis empile cette sortie dans un colis, du plus grand volume au 
  plus petit."""
  sortie = sortie_de_produit(stock, paquet)
  colis = []

  if sortie:
    while sortie:
      max_value = sortie[0]
      for produit in sortie:
        if produit[-1] > max_value[-1]:
          max_value = produit
      colis = [max_value] + colis
      sortie.remove(max_value)
  return colis


def afficher_sortie_produit(colis, produit_saisi):
  """Affiche le résultat de la sortie d'un produit."""
  if colis:
    print(f"Colis de sortie : {colis}")
  else:
    print(f'L\'élement {produit_saisi} n\'est pas dans le stock')


def afficher_sortie_paquet(colis, paquet):
  """Affiche le résultat de la sortie d'un paquet de produits."""
  if colis:
    print("Colis de sortie : ")
    for produit in colis:
      print(f"[{produit}]")
    if paquet != []:
      print(f'Les produits {paquet} n\'étaient pas dans le stock')
  else:
    print(f'Aucun des produits {paquet} ne sont dans le stock')


class Entrepot:
    """
    Entrepot class represents an inventory storage.

    Attributes:
    - stock: List of products in the inventory.
    - alertes: Dictionary to track inventory alerts.

    Methods:
    - __init__: Initializes the Entrepot instance.
    - est_vide: Checks if the inventory is empty.
    - ajouter_produit_ou_paquet: Adds a product or a package of products to the inventory.
    - remplir_stock: Fills the products in stock until a specified threshold.
    - generer_alerte: Generates alerts for products below a specified threshold.
    - print_alertes: Prints the current alerts.
    - sortir_produit_ou_paquet: Performs the exit of a product or a package of products from the inventory.
    """

    def __init__(self):
      """Initialise l'entrepôt avec un stock de produits prédéfini au lancement et une
      dictionnaire vide pour les alertes."""
      self.stock = [
          "A1", "Z8", "Z8", "Z8", "T6", "A1", "T6", "T6", "A1", "T6", "T3", "T3",
          "T3", "T3", "O3", "O3", "A1", "O3", "A1", "O3", "S3", "S3", "S3", "S3"
      ]
  
      self.alertes = {}

    def __repr__(self):
      """Représentation de la classe sous forme de chaîne de caractères, lorsqu'on
      appelle la méthode print() sur une instance de la classe. Ici, on représente l'
      entrepôt sous forme d'une file."""
      if self.est_vide():
        return ""
      else:
        string = "<- "
        for indice in range(len(self.stock)):
          string += f"{self.stock[indice]} "
        string += "<-"
        return string
  
    def est_vide(self):
      """Vérifie si l'entrepôt est vide."""
      return len(self.stock) == 0
  
    def ajouter_produit_ou_paquet(self):
      """Ajoute un produit ou un paquet de produits à l'entrepôt en fonction de la saisie
      de l'utilisateur."""
      saisie = input().upper()
      if saisie is not None and saisie != "":
        if len(saisie) <= 2:
          produit = verif_saisie_produit(saisie)
          if produit != "":
            self.stock.append(produit)
        else:
          paquet = verif_saisie_paquet(saisie)
          if paquet != []:
            self.stock = self.stock + paquet
  
    def remplir_stock(self, seuil):
      """Remplit les produits en rupture de stock jusqu'à atteindre le seuil spécifié."""
      for alerte in self.alertes:
        while self.alertes[alerte] < seuil + 1:
          self.stock.append(alerte)
          self.alertes[alerte] += 1
      self.alertes = {}
  
    def generer_alerte(self):
      """Génère des alertes si la quantité d'un produit est en dessous du seuil spécifié.
      Le dictionnaire des alertes est statique et limitée à 3 éléments. Si on essaye d'en
      ajouter un quatrième, on traite d'abord les trois premiers avec remplir_stock"""
      #Enlève les alertes de produits qui ne sont plus dans le stock
      alertes_aux = {}
      for produit in self.alertes:
        if produit in self.stock:
          alertes_aux[produit] = self.alertes[produit]
      self.alertes = alertes_aux
  
      #Définition du seuil et comptage du nombre de chaque produits dans le stock dans un
      #dictionnaire en utilisant la méthode Counter() de la libraire typing.
      seuil = 4
      quantite = Counter(self.stock)
  
      #Parcours du dictionnaire et traitement des alertes
      for produit, nombre in quantite.items():
  
        if nombre >= seuil and produit in self.alertes:
          self.alertes.pop(produit)
  
        elif nombre < seuil and produit in self.alertes:
          self.alertes[produit] = nombre
  
        elif nombre < seuil and produit not in self.alertes:
          if len(self.alertes) >= 3:
            self.remplir_stock(seuil)
          self.alertes[produit] = nombre
  
    def print_alertes(self):
      """Affiche les alertes actuelles."""
      if not self.alertes:
        print("Aucune alerte")
      else:
        for alerte in self.alertes:
          print(
              f"Alerte: {alerte} en rupture de stock. ({self.alertes[alerte]} restant)"
          )
  
    def sortir_produit_ou_paquet(self):
      """Effectue la sortie de l'entrepôt d'un produit ou d'un paquet de produits en
      fonction de la saisie de l'utilisateur."""
      saisie = input().upper()
      if saisie is not None and saisie != "":
        if len(saisie) <= 2:
          produit = verif_saisie_produit(saisie)
          if produit != "":
            colis = sortie_de_produit(self.stock, [produit])
            afficher_sortie_produit(colis, produit)
        else:
          paquet = verif_saisie_paquet(saisie)
          if paquet != []:
            colis = sortie_en_colis_paquet(self.stock, paquet)
            afficher_sortie_paquet(colis, paquet)


def afficher_menu():
  """Affiche le menu principal de sélection en mode console."""
  print("\nMenu:")
  print("1. Ajouter un/des produit(s)")
  print("2. Sortir un/des produit(s)")
  print("3. Afficher les alertes")
  print("4. Afficher les produits")
  print("5. Quitter")


def selection_choix():
  """Demande à l'utilisateur de choisir une option du menu principal."""
  choix = input("Choisissez une option (1-5): ")
  if choix == "1":
    print(
        """Entrez le produit à ajouter (Si vous en ajoutez par paquet, séparez les produits par des espaces): """
    )
    entrepot.ajouter_produit_ou_paquet()
    entrepot.generer_alerte()
    return 0
  elif choix == "2":
    print(
        """Entrez le produit à sortir (Si vous en sortez par paquet, séparez les
    produits par des espaces): """)
    entrepot.sortir_produit_ou_paquet()
    entrepot.generer_alerte()
    return 0
  elif choix == "3":
    entrepot.print_alertes()
    return 0
  elif choix == "4":
    print(entrepot)
    return 0
  elif choix == "5":
    print("Programme terminé.")
    return 1
  else:
    print("Option invalide. Veuillez choisir une option valide.")
    return 0


#Instanciation d'un objet Entrepot
entrepot = Entrepot()
#Génération d'alertes avec le stock en dur
entrepot.generer_alerte()

while True:
  #Affichage du menu puis séléction du choix
  afficher_menu()
  exit_code = selection_choix()
  if exit_code == 1:
    break
