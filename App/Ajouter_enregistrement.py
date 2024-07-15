# -*- coding: utf-8 -*-
import arcpy
import tkinter as tk
from tkinter import ttk, messagebox

def ajouter_enregistrement(table_name, values):
    try:
        # Ouvrir une connexion à la table en mode édition
        with arcpy.da.InsertCursor(table_name, list(values.keys())) as cursor:
            # Insérer l'enregistrement avec les valeurs fournies
            cursor.insertRow(list(values.values()))
        return True
    except Exception as e:
        print("Erreur lors de l'ajout de l'enregistrement:", e)
        return False

def ajouter_enregistrement_couche_arcgis(couche):
    # Créer une fenêtre Tkinter
    fenetre = tk.Toplevel()
    fenetre.title("Ajouter un nouvel enregistrement")

    # Récupérer les informations de la couche ArcGIS
    description = arcpy.Describe(couche)
    champs = description.fields

    # Créer les champs de saisie pour chaque champ de la couche
    entrees = []
    for champ in champs:
        if not champ.required:
            tk.Label(fenetre, text=champ.name).pack()
            entree = tk.Entry(fenetre)
            entree.pack()
            entrees.append(entree)

    # Fonction pour ajouter l'enregistrement à la couche
    def ajouter():
        valeurs = [entree.get() for entree in entrees]
        # with arcpy.da.InsertCursor(couche, [champ.name for champ in champs if not champ.required]) as curseur:
        #     curseur.insertRow(valeurs)
        ajouter_enregistrement(couche, valeurs)
        fenetre.destroy()

    # Ajouter un bouton pour ajouter l'enregistrement
    bouton = tk.Button(fenetre, text="Ajouter", command=ajouter)
    bouton.pack()

