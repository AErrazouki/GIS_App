# creer_buffer.py
# -*- coding: utf-8 -*-
# creer_buffer.py
import arcpy
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox, OptionMenu

class BufferTool:
    def __init__(self, root):
        self.root = root
        self.selected_feature_class = tk.StringVar(root)
        self.selected_polygon_class = tk.StringVar(root)

    def get_feature_classes(self):
        return arcpy.ListFeatureClasses()

    def creer_buffer(self):
        layer_name = self.selected_feature_class.get()
        buffer_window = tk.Toplevel(self.root)
        buffer_window.title("Distance du buffer")

        label = Label(buffer_window, text="Entrez la distance du buffer en unités de la carte:")
        label.pack(pady=10)

        distance_entry = Entry(buffer_window)
        distance_entry.pack(pady=5)

        def create_buffer():
            distance_str = distance_entry.get()
            if distance_str.strip() == "":
                messagebox.showerror("Erreur", "Veuillez saisir une distance valide.")
                return
            try:
                distance = float(distance_str)
                buffer_name = "Buffer_" + layer_name
                arcpy.Buffer_analysis(layer_name, buffer_name, "{} Meters".format(distance))
                messagebox.showinfo("Succès", "Le buffer autour de la couche {} a été créé avec succès.".format(layer_name))
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez saisir une distance valide (nombre).")
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
            buffer_window.destroy()

        create_button = Button(buffer_window, text="Créer le buffer", command=create_buffer, bg="light blue", fg="white", font=("Arial", 12, "bold"))
        create_button.pack(pady=5)

    def creer_intersection_buffers(self):
        buffer_layers = [layer for layer in self.get_feature_classes() if layer.startswith("Buffer_")]

        if len(buffer_layers) < 2:
            messagebox.showerror("Erreur", "Il doit y avoir au moins deux couches de buffer pour créer une intersection.")
            return

        intersect_window = tk.Toplevel(self.root)
        intersect_window.title("Sélectionner les buffers à intersecter")

        selected_buffer1 = tk.StringVar(intersect_window)
        selected_buffer1.set(buffer_layers[0])
        buffer1_dropdown = OptionMenu(intersect_window, selected_buffer1, *buffer_layers)
        buffer1_dropdown.pack(pady=10)

        selected_buffer2 = tk.StringVar(intersect_window)
        selected_buffer2.set(buffer_layers[1])
        buffer2_dropdown = OptionMenu(intersect_window, selected_buffer2, *buffer_layers)
        buffer2_dropdown.pack(pady=10)

        def create_intersection():
            buffer1 = selected_buffer1.get()
            buffer2 = selected_buffer2.get()
            if buffer1 == buffer2:
                messagebox.showerror("Erreur", "Veuillez sélectionner deux buffers différents.")
                return
            intersection_output = "Intersection_{}_{}".format(buffer1, buffer2)
            try:
                arcpy.Intersect_analysis([buffer1, buffer2], intersection_output)
                messagebox.showinfo("Succès", "L'intersection des buffers {} et {} a été créée avec succès.".format(buffer1, buffer2))
            except Exception as e:
                messagebox.showerror("Erreur", str(e))
            intersect_window.destroy()

        intersect_button = Button(intersect_window, text="Créer l'intersection", command=create_intersection, bg="light blue", fg="white", font=("Arial", 12, "bold"))
        intersect_button.pack(pady=10)

    def convertir_polygone_en_lignes(self):
        polygon_layer_name = self.selected_polygon_class.get()
        line_layer_name = "Lines_" + polygon_layer_name
        try:
            arcpy.FeatureToLine_management(polygon_layer_name, line_layer_name)
            messagebox.showinfo("Succès", "La couche de polygones {} a été convertie en lignes avec succès.".format(polygon_layer_name))
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
