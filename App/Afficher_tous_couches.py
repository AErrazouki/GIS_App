# -*- coding: utf-8 -*-

import arcpy
import tkinter as tk
from tkinter import messagebox


def afficher_couches(path):
    try:
        # Définir l'environnement de géodatabase
        arcpy.env.workspace = path

        # Récupérer la liste des couches
        liste_couches = arcpy.ListFeatureClasses() + arcpy.ListTables()

        # Créer une fenêtre pour afficher la liste des couches
        fenetre_couches = tk.Tk()
        fenetre_couches.title("Liste des couches")

        # Créer une zone de texte pour afficher les couches
        texte_couches = tk.Text(fenetre_couches, wrap="word", height=10, width=50)
        texte_couches.pack()

        # Ajouter chaque couche à la zone de texte
        for couche in liste_couches:
            texte_couches.insert(tk.END, couche + "\n")

        # Désactiver l'édition du texte
        texte_couches.configure(state=tk.DISABLED)

        # Fonction pour fermer la fenêtre lorsqu'on clique sur le bouton "Fermer"
        def fermer_fenetre():
            fenetre_couches.destroy()

        # Créer un bouton pour fermer la fenêtre
        bouton_fermer = tk.Button(fenetre_couches, text="Fermer", command=fermer_fenetre)
        bouton_fermer.pack()

        # Afficher la fenêtre
        #fenetre_couches.mainloop()

    except Exception as e:
        messagebox.showerror("Erreur", "Erreur lors de la récupération des couches : {}".format(e))

# Fonction de rappel pour le bouton "Afficher les couches"

# Afficher la fenêtre principale
#fenetre_principale.mainloop()
