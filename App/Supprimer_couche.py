# -*- coding: utf-8 -*-
import arcpy
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkMessageBox

def supprimer_couche(chemin_geodatabase, nom_couche):
    if arcpy.Exists(chemin_geodatabase):
        # Vérifier si la couche existe dans la géodatabase
        if arcpy.Exists(chemin_geodatabase + "\\" + nom_couche):
            # Supprimer la couche
            arcpy.Delete_management(chemin_geodatabase + "\\" + nom_couche)
            tkMessageBox.showinfo("Information", "La couche {} a été supprimée avec succès.".format(nom_couche))
        else:
            tkMessageBox.showerror("Erreur", "La couche {} n'existe pas dans la géodatabase.".format(nom_couche))
    else:
        tkMessageBox.showerror("Erreur", "La géodatabase spécifiée n'existe pas.")

def supprimer_couche_ui(chemin_geodatabase):
    # Fonction appelée lorsque l'utilisateur clique sur le bouton "Supprimer"
    def supprimer():
        # Récupérer le nom de la couche sélectionnée dans la liste déroulante
        nom_couche_selectionnee = liste_couches.get()
        if nom_couche_selectionnee:
            # Demander une confirmation à l'utilisateur avant de supprimer la couche
            confirmation = tkMessageBox.askyesno("Confirmation", "Voulez-vous vraiment supprimer la couche {} ?".format(nom_couche_selectionnee))
            if confirmation:
                # Appeler la fonction pour supprimer la couche
                supprimer_couche(chemin_geodatabase, nom_couche_selectionnee)
                # Fermer la fenêtre après la suppression
                fenetre.destroy()

    # Obtenir la liste des couches dans la géodatabase spécifiée
    couches = arcpy.ListFeatureClasses()

    if couches:
        # Créer une fenêtre tkinter pour l'interface utilisateur
        fenetre = tk.Tk()
        fenetre.title("Supprimer une couche")
        fenetre.configure(bg="light blue")

        # Ajouter une étiquette pour indiquer à l'utilisateur de sélectionner une couche
        label = tk.Label(fenetre, text="Sélectionnez la couche à supprimer:" ,
                         font=("Bodoni MT", 18),
                         bg="light blue")
        label.pack()

        # Créer une liste déroulante pour afficher les couches disponibles
        liste_couches = ttk.Combobox(fenetre, values=couches)
        liste_couches.pack()

        # Ajouter un bouton pour permettre à l'utilisateur de supprimer la couche sélectionnée
        bouton_supprimer = tk.Button(fenetre, text="Supprimer", command=supprimer)
        bouton_supprimer.pack()

        # Lancer la boucle principale de l'interface utilisateur tkinter
        fenetre.mainloop()
    else:
        tkMessageBox.showwarning("Aucune couche", "Aucune couche n'est disponible dans la géodatabase.")
