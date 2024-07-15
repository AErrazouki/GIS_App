# -*- coding: utf-8 -*-

import arcpy
import tkinter as tk
from tkinter import messagebox

def afficher_champs_couche(path):
    try:
        # Définir l'environnement de géodatabase
        arcpy.env.workspace = path

        # Récupérer la liste des couches
        liste_couches = arcpy.ListFeatureClasses() + arcpy.ListTables()

        # Créer une fenêtre pour afficher les champs pour chaque couche
        fenetre_champs = tk.Tk()
        fenetre_champs.title("Champs des couches")

        for couche in liste_couches:
            # Créer un label pour le nom de la couche
            label_couche = tk.Label(fenetre_champs, text="Couche: {}".format(couche))
            label_couche.pack()

            # Récupérer les noms des champs de la couche
            champs = [field.name for field in arcpy.ListFields(couche)]

            # Créer une zone de texte pour afficher les champs
            texte_champs = tk.Text(fenetre_champs, wrap="word", height=6, width=60)
            texte_champs.pack()

            # Ajouter chaque champ à la zone de texte
            for champ in champs:
                texte_champs.insert(tk.END, champ + "\n")

            # Désactiver l'édition du texte
            texte_champs.configure(state=tk.DISABLED)

            # Ajouter une séparation entre chaque couche
            tk.Label(fenetre_champs, text="").pack()

        # Fonction pour fermer la fenêtre lorsqu'on clique sur le bouton "Fermer"
        def fermer_fenetre():
            fenetre_champs.destroy()

        # Créer un bouton pour fermer la fenêtre
        bouton_fermer = tk.Button(fenetre_champs, text="Fermer", command=fermer_fenetre)
        bouton_fermer.pack()

        # Afficher la fenêtre
        fenetre_champs.mainloop()

    except Exception as e:
        messagebox.showerror("Erreur", "Erreur lors de la récupération des champs : {}".format(e))


