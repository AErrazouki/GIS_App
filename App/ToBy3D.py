# -*- coding: utf-8 -*-
import arcpy
import tkinter as tk
from tkinter import filedialog, messagebox

def select_input_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("Shapefiles", "*.shp")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def run_arcpy_script(input_entry, output_entry, height_field_var):
    try:
        input_features = input_entry.get()  # Récupérer le chemin des entités en entrée
        height_field = height_field_var.get()  # Récupérer le champ de hauteur sélectionné
        output_features = output_entry.get()  # Récupérer le chemin des entités en sortie

        # Créer des entités 3D à partir des attributs
        arcpy.FeatureTo3DByAttribute_3d(input_features, output_features, height_field)
        print("Entités 3D créées à partir des attributs avec succès")
        messagebox.showinfo("Succès", "Entités 3D créées à partir des attributs avec succès")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur s'est produite : " + str(e))
