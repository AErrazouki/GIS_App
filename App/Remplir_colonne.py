# -*- coding: utf-8 -*-
import arcpy
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkMessageBox

def modifier_valeurs(table, colonne_source, colonne_cible):
    try:
        with arcpy.da.UpdateCursor(table, [colonne_source, colonne_cible]) as cursor:
            for row in cursor:
                row[1] = row[0]  # Remplacer la valeur de colonne_cible par la valeur de colonne_source
                cursor.updateRow(row)
        tkMessageBox.showinfo("Succès", "Les valeurs de la colonne '{}' ont été mises à jour avec les valeurs de '{}'.".format(colonne_cible, colonne_source))
    except arcpy.ExecuteError:
        tkMessageBox.showerror("Erreur", arcpy.GetMessages(2))

def modifier_valeurs_ui(chemin_geodatabase):
    def modifier():
        table_selectionnee = listbox_tables.get(tk.ACTIVE)
        colonne_source = colonne_source_combobox.get()
        colonne_cible = colonne_cible_combobox.get()

        if table_selectionnee and colonne_source and colonne_cible:
            confirmation_message = (
                "Voulez-vous vraiment remplacer les valeurs de la colonne '{}' par les valeurs de la colonne '{}' "
                "dans la table sélectionnée '{}' ?".format(colonne_cible, colonne_source, table_selectionnee)
            )

            confirmation = tkMessageBox.askokcancel("Confirmation", confirmation_message)
            if confirmation:
                modifier_valeurs(table_selectionnee, colonne_source, colonne_cible)
                fenetre.destroy()  # Fermer la fenêtre après la mise à jour

    # Lister les tables dans la géodatabase
    arcpy.env.workspace = chemin_geodatabase
    tables = arcpy.ListTables() + arcpy.ListFeatureClasses()  # Inclure les classes d'entités

    if tables:
        fenetre = tk.Tk()
        fenetre.title("Modifier les valeurs d'une colonne")
        fenetre.configure(bg="light blue")

        # Titre
        titre = tk.Label(fenetre, text="Remplir une colonne pour les valeurs d'autre colonne",
                         font=("Bodoni MT", 18),
                         bg="light blue")
        titre.pack()

        listbox_tables = tk.Listbox(fenetre, height=10, width=10)
        for table in tables:
            listbox_tables.insert(tk.END, table)
        listbox_tables.pack(padx=10, pady=10)

        label_colonne_source = tk.Label(fenetre, text="Sélectionnez la colonne source:", bg="light blue")
        label_colonne_source.pack(pady=5)
        colonne_source_var = tk.StringVar()
        colonne_source_combobox = ttk.Combobox(fenetre, textvariable=colonne_source_var)
        colonne_source_combobox.pack(pady=5)

        label_colonne_cible = tk.Label(fenetre, text="Sélectionnez la colonne cible:", bg="light blue")
        label_colonne_cible.pack(pady=5)
        colonne_cible_var = tk.StringVar()
        colonne_cible_combobox = ttk.Combobox(fenetre, textvariable=colonne_cible_var)
        colonne_cible_combobox.pack(pady=5)

        def update_comboboxes(event):
            table_selectionnee = listbox_tables.get(tk.ACTIVE)
            if table_selectionnee:
                field_names = [f.name for f in arcpy.ListFields(table_selectionnee)]
                colonne_source_combobox['values'] = field_names
                colonne_cible_combobox['values'] = field_names

        listbox_tables.bind('<<ListboxSelect>>', update_comboboxes)

        bouton_modifier = tk.Button(fenetre, text="Modifier", command=modifier)
        bouton_modifier.pack(pady=5)

        # Bouton pour fermer la fenêtre
        bouton_fermer = tk.Button(fenetre, text="Fermer", command=fenetre.destroy)
        bouton_fermer.pack(pady=5)

        fenetre.mainloop()
    else:
        tkMessageBox.showwarning("Aucune table", "Aucune table n'est disponible dans la géodatabase.")
