# -*- coding: utf-8 -*-
import arcpy
import tkinter as tk
from tkinter import ttk
import tkMessageBox
import tkinter.filedialog as tkFileDialog

def ajouter_couche(chemin_geodatabase):
    def valider():
        nom_couche = champ_saisie.get()
        type_couche = liste_types.get()

        if nom_couche and type_couche and chemin_geodatabase:
            # Créer le chemin complet de la nouvelle couche
            chemin_couche = arcpy.CreateFeatureclass_management(chemin_geodatabase, nom_couche, type_couche)

            tkMessageBox.showinfo("Information",
                                "La couche {} a été ajoutée avec succès dans la géodatabase {}.".format(nom_couche, chemin_geodatabase))
        else:
            tkMessageBox.showerror("Erreur", "Veuillez remplir tous les champs.")

    # Créer la fenêtre de saisie
    fenetre_saisie = tk.Tk()
    fenetre_saisie.geometry("400x200")
    fenetre_saisie.title("Ajouter une couche")

    # Zone de saisie pour le nom de la couche
    label_nom = tk.Label(fenetre_saisie, text="Nom de la couche:")
    label_nom.pack()

    champ_saisie = tk.Entry(fenetre_saisie)
    champ_saisie.pack()

    # Liste déroulante pour le type de la couche
    label_type = tk.Label(fenetre_saisie, text="Type de la couche:")
    label_type.pack()

    types_couche = ["POINT", "POLYLINE", "POLYGON"]  # Types de couche supportés par ArcGIS

    liste_types = ttk.Combobox(fenetre_saisie, values=types_couche, state="readonly")
    liste_types.pack()

    # Affichage du chemin de la géodatabase
    label_geodatabase = tk.Label(fenetre_saisie, text="Chemin de la géodatabase:")
    label_geodatabase.pack()

    champ_geodatabase = tk.Entry(fenetre_saisie)
    champ_geodatabase.pack()
    champ_geodatabase.insert(0, chemin_geodatabase)  # Afficher le chemin de la géodatabase

    # Bouton Valider
    bouton_valider = tk.Button(fenetre_saisie, text="Valider", command=valider)
    bouton_valider.pack()

    fenetre_saisie.mainloop()
