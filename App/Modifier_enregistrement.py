# -*- coding: utf-8 -*-
import arcpy
import tkinter as tk
from tkinter import ttk, messagebox

def modifier_enregistrement(table_path, object_id, nouvelles_valeurs):
    try:
        with arcpy.da.UpdateCursor(table_path, ["name", "X", "Y"], "OBJECTID = " , object_id) as cursor:
            for row in cursor:
                row[1] = nouvelles_valeurs["X"]
                row[2] = nouvelles_valeurs["Y"]
                cursor.updateRow(row)
        messagebox.showinfo("Succès", "Enregistrement modifié avec succès.")
    except Exception as e:
        messagebox.showerror("Erreur", "Une erreur est survenue : " , str(e))
