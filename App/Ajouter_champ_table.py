# -*- coding: utf-8 -*-
import arcpy
import tkinter as tk
from tkinter import messagebox

def ajouter_champ(table, nom_champ, type_champ):
    try:
        arcpy.AddField_management(table, nom_champ, type_champ)
        messagebox.showinfo("Succès", "Champ ajouté avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", "Erreur lors de l'ajout du champ : {}".format(e))

class AjouterChampApp(tk.Toplevel):
    def __init__(self, parent, couches):
        tk.Toplevel.__init__(self, parent)
        self.title("Ajouter un champ")
        self.configure(bg="light blue")

        self.couches = couches

        # Label et liste déroulante pour sélectionner la couche
        self.label_couche = tk.Label(self, text="Sélectionnez une couche :", bg="light blue")
        self.label_couche.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.liste_couche = tk.StringVar()
        self.liste_deroulante_couche = tk.OptionMenu(self, self.liste_couche, *self.couches)
        self.liste_deroulante_couche.grid(row=0, column=1, padx=10, pady=5)

        # Label et liste déroulante pour sélectionner le type de champ
        self.label_type_champ = tk.Label(self, text="Sélectionnez le type de champ :", bg="light blue")
        self.label_type_champ.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.liste_type_champ = tk.StringVar()
        self.liste_deroulante_type_champ = tk.OptionMenu(self, self.liste_type_champ, *["Text", "Integer", "Double", "Date", "Blob"])
        self.liste_deroulante_type_champ.grid(row=1, column=1, padx=10, pady=5)

        # Entrée pour le nom du champ
        self.label_nom_champ = tk.Label(self, text="Nom du champ :", bg="light blue")
        self.label_nom_champ.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_nom_champ = tk.Entry(self)
        self.entry_nom_champ.grid(row=2, column=1, padx=10, pady=5)

        # Boutons de validation et d'annulation
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider_champ)
        self.bouton_valider.grid(row=3, column=0, padx=10, pady=5)
        self.bouton_annuler = tk.Button(self, text="Annuler", command=self.destroy)
        self.bouton_annuler.grid(row=3, column=1, padx=10, pady=5)

    def valider_champ(self):
        couche_selectionnee = self.liste_couche.get()
        nom_champ = self.entry_nom_champ.get()
        type_champ = self.liste_type_champ.get()
        if couche_selectionnee and nom_champ and type_champ:
            ajouter_champ(couche_selectionnee, nom_champ, type_champ)
            self.destroy()
        else:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")

# Fonction pour récupérer la liste des couches dans la géodatabase
def obtenir_couches():
    path = r'C:\Users\aya\Documents\ArcGIS\BDSAS2024.gdb\couche'
    arcpy.env.workspace = path
    couches = arcpy.ListFeatureClasses() + arcpy.ListTables()
    return couches
