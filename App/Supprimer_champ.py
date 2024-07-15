# -*- coding: utf-8 -*-
import arcpy
import tkinter as tk
from tkinter import messagebox
import time

def supprimer_champ(table, nom_champ):
    try:
        # Vérifiez et supprimez les verrous
        if arcpy.Exists(table):
            arcpy.management.ClearWorkspaceCache()

        # Ajouter un délai pour permettre la libération des verrous
        time.sleep(2)

        # Supprimer le champ
        arcpy.management.DeleteField(table, nom_champ)
        messagebox.showinfo("Succès", "Champ supprimé avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", "Erreur lors de la suppression du champ : {}".format(e))

class SupprimerChampApp(tk.Toplevel):
    def __init__(self, parent, couches):
        tk.Toplevel.__init__(self, parent)
        self.title("Supprimer un champ")
        self.configure(bg="light blue")

        self.couches = couches

        # Liste des champs obligatoires
        self.required_fields = ["OBJECTID", "Shape", "Shape_Length", "Shape_Area"]

        # Label et liste déroulante pour sélectionner la couche
        self.label_couche = tk.Label(self, text="Sélectionnez une couche :", bg="light blue")
        self.label_couche.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.liste_couche = tk.StringVar()
        self.liste_deroulante_couche = tk.OptionMenu(self, self.liste_couche, *self.couches, command=self.update_champs)
        self.liste_deroulante_couche.grid(row=0, column=1, padx=10, pady=5)

        # Label et liste déroulante pour sélectionner le champ
        self.label_champ = tk.Label(self, text="Sélectionnez un champ à supprimer :", bg="light blue")
        self.label_champ.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.liste_champ = tk.StringVar()
        self.liste_deroulante_champ = tk.OptionMenu(self, self.liste_champ, "")
        self.liste_deroulante_champ.grid(row=1, column=1, padx=10, pady=5)

        # Boutons de validation et d'annulation
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider_champ)
        self.bouton_valider.grid(row=2, column=0, padx=10, pady=5)
        self.bouton_annuler = tk.Button(self, text="Annuler", command=self.destroy)
        self.bouton_annuler.grid(row=2, column=1, padx=10, pady=5)

    def update_champs(self, selected_couche):
        champs = [f.name for f in arcpy.ListFields(selected_couche) if f.name not in self.required_fields]
        self.liste_champ.set("")  # Clear previous selection
        menu = self.liste_deroulante_champ["menu"]
        menu.delete(0, "end")
        for champ in champs:
            menu.add_command(label=champ, command=lambda value=champ: self.liste_champ.set(value))

    def valider_champ(self):
        couche_selectionnee = self.liste_couche.get()
        nom_champ = self.liste_champ.get()
        if couche_selectionnee and nom_champ:
            supprimer_champ(couche_selectionnee, nom_champ)
            self.destroy()
        else:
            messagebox.showwarning("Attention", "Veuillez sélectionner une couche et un champ.")

# Fonction pour récupérer la liste des couches dans la géodatabase
def obtenir_couches():
    path = r'C:\Users\aya\Documents\ArcGIS\BDSAS2024.gdb\couche'
    arcpy.env.workspace = path
    couches = arcpy.ListFeatureClasses() + arcpy.ListTables()
    return couches