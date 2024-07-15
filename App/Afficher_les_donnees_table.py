# -*- coding: utf-8 -*-
import arcpy
import tkinter as tk
from tkinter import ttk, messagebox

def afficher_donnees_couche():
    try:
        # Récupérer le nom de la couche sélectionnée dans la liste déroulante
        nom_couche = liste_couche.get()

        # Récupérer les données de la couche sélectionnée
        donnees_couche = []
        with arcpy.da.SearchCursor(nom_couche, '*') as cursor:
            for row in cursor:
                donnees_couche.append(row)

        # Récupérer les noms des champs de la couche
        champs_couche = [field.name for field in arcpy.ListFields(nom_couche)]

        # Créer une nouvelle fenêtre pour afficher les données
        fenetre_donnees = tk.Tk()
        fenetre_donnees.title("Données de la couche : {}".format(nom_couche))

        # Créer un Treeview pour afficher les données
        tree = ttk.Treeview(fenetre_donnees)
        tree['columns'] = tuple(champs_couche)

        # Ajouter des colonnes à Treeview avec les noms de champs
        for champ in champs_couche:
            tree.column(champ, anchor=tk.CENTER, stretch=True)
            tree.heading(champ, text=champ, anchor=tk.CENTER)

        # Ajouter les données à Treeview
        for row in donnees_couche:
            tree.insert('', tk.END, values=row)

        # Pack le Treeview
        tree.pack(fill='both', expand=True)

        # Afficher la fenêtre
        fenetre_donnees.mainloop()

    except Exception as e:
        messagebox.showerror("Erreur", "Erreur lors de l'affichage des données de la couche : {}".format(e))

# Créer une fenêtre principale
fenetre_principale = tk.Tk()
fenetre_principale.title("Afficher les données par couche")

def charger_couches(path):
    try:
        # Définir l'environnement de géodatabase
        arcpy.env.workspace = path

        # Récupérer la liste des couches disponibles
        couches_disponibles = arcpy.ListFeatureClasses() + arcpy.ListTables()

        return couches_disponibles

    except Exception as e:
        messagebox.showerror("Erreur", "Erreur lors du chargement des couches : {}".format(e))
        return []

# Obtenir le chemin de la géodatabase
path_geodatabase = r'C:\Users\aya\Documents\ArcGIS\BDSAS2024.gdb\couche'

# Charger les couches disponibles
couches_disponibles = charger_couches(path_geodatabase)

if couches_disponibles:
    # Créer une liste déroulante pour sélectionner la couche
    label_couche = tk.Label(fenetre_principale, text="Sélectionnez une couche :")
    label_couche.pack()

    liste_couche = ttk.Combobox(fenetre_principale, values=couches_disponibles, state="readonly")
    liste_couche.pack()

    # Créer un bouton pour afficher les données de la couche sélectionnée
    bouton_afficher_donnees = tk.Button(fenetre_principale, text="Afficher les données de la couche", command=afficher_donnees_couche)
    bouton_afficher_donnees.pack()
else:
    messagebox.showerror("Erreur", "Aucune couche trouvée dans la géodatabase.")

fenetre_principale.mainloop()
