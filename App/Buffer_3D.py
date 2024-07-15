# -*- coding: utf-8 -*-
import arcpy
import tkinter as tk
from tkinter import filedialog

import arcpy
import tkinter as tk
from tkinter import filedialog, messagebox


def select_input_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("Shapefiles", "*.shp")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


def select_centroid_file(entry):
    file_path = filedialog.askopenfilename(filetypes=[("Shapefiles", "*.shp")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)


def run_arcpy_script(input_entry, centroid_entry, output_entry, distance_entry):
    try:
        input_polygons = input_entry.get()
        centroid_points = centroid_entry.get()
        distance = distance_entry.get()

        # Chemin de sortie avec nom de fichier personnalisé
        output_features = r'C:\Users\aya\Documents\ArcGIS\\' + output_entry.get() + '.shp'

        # Créer les points centroids à partir des polygones
        arcpy.FeatureToPoint_management(input_polygons, centroid_points, "CENTROID")
        print("Points centroids créés avec succès")

        # Créer la zone tampon 3D pour les points centroids
        arcpy.Buffer3D_3d(centroid_points, output_features, distance)
        print("Zone tampon 3D créée avec succès pour les points centroids")

    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur s'est produite : ",e)
