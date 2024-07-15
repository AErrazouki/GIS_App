# -*- coding: utf-8 -*-
import arcpy
from tkinter import messagebox
import tkinter as tk
def creer_geodatabase(chemin, nom_geodatabase):
    try:
        # Chemin complet de la nouvelle géodatabase
        gdb_path = "{}\\{}.gdb".format(chemin, nom_geodatabase)

        # Créer une nouvelle géodatabase de type File Geodatabase
        arcpy.CreateFileGDB_management(chemin, nom_geodatabase)

        messagebox.showinfo("Succès", "Nouvelle géodatabase créée avec succès à l'emplacement :\n{}".format(gdb_path))
        return gdb_path
    except Exception as e:
        messagebox.showerror("Erreur", "Erreur lors de la création de la géodatabase : {}".format(e))
