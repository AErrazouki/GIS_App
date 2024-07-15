# -*- coding: utf-8 -*-
import arcpy
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkMessageBox


def afficher_enregistrements(table):
    try:
        fenetre = tk.Toplevel()
        fenetre.title("Enregistrements de {}".format(table))

        # Création du Treeview
        tree = ttk.Treeview(fenetre)
        tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Définir les colonnes
        field_names = [f.name for f in arcpy.ListFields(table)]
        cursor = arcpy.da.SearchCursor(table, field_names)
        tree["columns"] = field_names

        # Configuration des colonnes
        for field in field_names:
            tree.column(field, anchor=tk.W)
            tree.heading(field, text=field)

        # Insertion des données
        for row in cursor:
            tree.insert("", tk.END, values=row)

        cursor.reset()
        cursor.close()

    except arcpy.ExecuteError:
        tkMessageBox.showerror("Erreur", arcpy.GetMessages(2))


def afficher_enregistrements_ui(chemin_geodatabase):
    def afficher():
        table_selectionnee = listbox_tables.get(tk.ACTIVE)
        if table_selectionnee:
            afficher_enregistrements(table_selectionnee)

    # Lister les tables dans la géodatabase
    arcpy.env.workspace = chemin_geodatabase
    tables = arcpy.ListTables() + arcpy.ListFeatureClasses()  # Inclure les classes d'entités

    if tables:
        fenetre = tk.Tk()
        fenetre.title("Afficher les enregistrements")

        label_tables = tk.Label(fenetre, text="Sélectionnez une table:")
        label_tables.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        listbox_tables = tk.Listbox(fenetre, height=10)
        for table in tables:
            listbox_tables.insert(tk.END, table)
        listbox_tables.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        bouton_afficher = tk.Button(fenetre, text="Afficher", command=afficher)
        bouton_afficher.grid(row=2, column=0, padx=5, pady=5)

        fenetre.mainloop()
    else:
        tkMessageBox.showwarning("Aucune table", "Aucune table n'est disponible dans la géodatabase.")


# Exemple d'appel de la fonction UI
chemin_geodatabase = r'C:\Users\aya\Documents\ArcGIS\BDSAS2024.gdb\couche'
afficher_enregistrements_ui(chemin_geodatabase)
