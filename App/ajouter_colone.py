# -*- coding: utf-8 -*-
import arcpy
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkMessageBox

def ajouter_colonne(tables, nom_colonne, type_colonne):
    for table in tables:
        try:
            arcpy.AddField_management(table, nom_colonne, type_colonne)
            tkMessageBox.showinfo("Succès", "La colonne '{}' a été ajoutée à '{}' avec succès.".format(nom_colonne, table))
        except arcpy.ExecuteError:
            tkMessageBox.showerror("Erreur", arcpy.GetMessages(2))

def ajouter_colonne_ui(chemin_geodatabase):
    def ajouter():
        tables_selectionnees = [listbox_tables.get(i) for i in listbox_tables.curselection()]
        nom_colonne = nom_colonne_var.get()
        type_colonne = type_colonne_var.get()

        if tables_selectionnees and nom_colonne and type_colonne:
            tables_list = "\n".join(tables_selectionnees)
            confirmation_message = (
                "Voulez-vous vraiment ajouter la colonne '{}' de type '{}' "
                "aux tables sélectionnées suivantes ?\n\n{}".format(nom_colonne, type_colonne, tables_list)
            )
            confirmation = tkMessageBox.askyesno("Confirmation", confirmation_message)
            if confirmation:
                ajouter_colonne(tables_selectionnees, nom_colonne, type_colonne)
                fenetre.destroy()  # Fermer la fenêtre après l'ajout

    # Lister les tables dans la géodatabase
    arcpy.env.workspace = chemin_geodatabase
    tables = arcpy.ListTables()

    if tables:
        fenetre = tk.Tk()
        fenetre.title("Ajouter une colonne à plusieurs tables")

        label_tables = tk.Label(fenetre, text="Sélectionnez les tables:")
        label_tables.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        listbox_tables = tk.Listbox(fenetre, selectmode=tk.MULTIPLE, height=10)
        for table in tables:
            listbox_tables.insert(tk.END, table)
        listbox_tables.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        label_nom_colonne = tk.Label(fenetre, text="Nom de la colonne:")
        label_nom_colonne.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        nom_colonne_var = tk.StringVar()
        nom_colonne_entry = tk.Entry(fenetre, textvariable=nom_colonne_var)
        nom_colonne_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        label_type_colonne = tk.Label(fenetre, text="Type de la colonne:")
        label_type_colonne.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        types_colonne = ["TEXT", "FLOAT", "DOUBLE", "SHORT", "LONG", "DATE", "BLOB", "RASTER", "GUID"]
        type_colonne_var = tk.StringVar()
        type_colonne_combobox = ttk.Combobox(fenetre, textvariable=type_colonne_var, values=types_colonne)
        type_colonne_combobox.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        bouton_ajouter = tk.Button(fenetre, text="Ajouter", command=ajouter)
        bouton_ajouter.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        fenetre.mainloop()
    else:
        tkMessageBox.showwarning("Aucune table", "Aucune table n'est disponible dans la géodatabase.")

# Exemple d'appel de la fonction UI
chemin_geodatabase = r'C:\Users\aya\Documents\ArcGIS\BDSAS2024.gdb\couche'
ajouter_colonne_ui(chemin_geodatabase)
