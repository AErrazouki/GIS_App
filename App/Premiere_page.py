# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.messagebox as tkMessageBox
import arcpy
import tkinter as tk
import tkinter.messagebox as tkMessageBox
import tkinter.filedialog as tkFileDialog
import tkinter.simpledialog as tkSimpleDialog  # Ajoutez cet import pour utiliser askstring
import arcpy
import os
import tkSimpleDialog
from Afficher_tous_couches import afficher_couches
from Ajouter_champ_table import *
from Supprimer_champ import *
from Creer_data_gbd import *
from Ajouter_couche import *
from Supprimer_couche import *
from Remplir_colonne import *
from calcul_max_min_somme import *
from Afficher_champ_table import *
from creer_buffer import *
from tkinter import filedialog, messagebox, simpledialog
from Ajouter_enregistrement import ajouter_enregistrement_couche_arcgis
from Modifier_enregistrement import *
from Supprimer_enregistrement import *
from tkinter import messagebox, Label, Entry, Button, OptionMenu
from Buffer_3D import select_input_file, select_centroid_file, run_arcpy_script
from ToBy3D import select_input_file,run_arcpy_script

class ArcgisApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Application ArcGIS")
        self.configure(bg="light blue")
        self.dossier_geodatabase = None  # Variable pour stocker le dossier de géodatabase sélectionné

        self.label_bienvenue = tk.Label(self, text="Bienvenue sur l'application ArcGIS", font=("Bodoni MT", 18),
                                        bg="light blue")
        self.label_bienvenue.pack(pady=30)

        self.frame_boutons = tk.Frame(self, bg="light blue")
        self.frame_boutons.pack()

        self.bouton_geodatabase = tk.Button(self.frame_boutons, text="Choisir une géodatabase",
                                            command=self.choisir_geodatabase, width=20, height=2)
        self.bouton_geodatabase.pack(side=tk.LEFT, padx=10, pady=10)

        self.bouton_traitement = tk.Button(self.frame_boutons, text="Choisir un traitement",
                                           command=self.choisir_traitement, width=20, height=2)
        self.bouton_traitement.pack(side=tk.LEFT, padx=10, pady=10)

        # Bouton pour ouvrir la fenêtre pour le nom de la couche
        self.bouton_nom_couche = tk.Button(self.frame_boutons, text="Couche",
                                           command=self.ouvrir_nom_couche_window, width=20, height=2)
        self.bouton_nom_couche.pack(side=tk.LEFT, padx=10, pady=10)

        # Bouton pour créer un buffer
        self.bouton_buffer = tk.Button(self.frame_boutons, text="Buffer",
                                       command=self.open_buffer_tool, width=20, height=2)
        self.bouton_buffer.pack(side=tk.LEFT, padx=10, pady=10)

        # Bouton pour créer des entités 3D
        self.bouton_3d = tk.Button(self.frame_boutons, text="Créer Entités 3D",
                                   command=self.open_buffer_3d_tool, width=20, height=2)
        self.bouton_3d.pack(side=tk.LEFT, padx=10, pady=10)

        self.bouton_to_3d = tk.Button(self.frame_boutons, text="Créer Entités 3D par l'hauter", command=self.open_create_to3D_tool,
                                   width=20, height=2)
        self.bouton_to_3d.pack(side=tk.LEFT, padx=10, pady=10)

        self.bouton_fermer = tk.Button(self, text="Fermer", command=self.fermer_application, width=20, height=2)
        self.bouton_fermer.pack(pady=10)

        self.buffer_tool = BufferTool(self)

    def open_buffer_3d_tool(self):
        try:
            self.buffer_3d_window = tk.Toplevel(self)
            self.buffer_3d_window.title("ArcPy Buffer 3D")

            tk.Label(self.buffer_3d_window, text="Sélectionnez le fichier de polygones :").grid(row=0, column=0,
                                                                                                padx=10, pady=5)
            self.input_entry = tk.Entry(self.buffer_3d_window, width=50)
            self.input_entry.grid(row=0, column=1, padx=10, pady=5)
            tk.Button(self.buffer_3d_window, text="Parcourir",
                      command=lambda: select_input_file(self.input_entry)).grid(row=0, column=2, padx=10, pady=5)

            tk.Label(self.buffer_3d_window, text="Sélectionnez le fichier des points centroids :").grid(row=1, column=0,
                                                                                                        padx=10, pady=5)
            self.centroid_entry = tk.Entry(self.buffer_3d_window, width=50)
            self.centroid_entry.grid(row=1, column=1, padx=10, pady=5)
            tk.Button(self.buffer_3d_window, text="Parcourir",
                      command=lambda: select_centroid_file(self.centroid_entry)).grid(row=1, column=2, padx=10, pady=5)

            tk.Label(self.buffer_3d_window, text="Nom du fichier de sortie (sans extension) :").grid(row=2, column=0,
                                                                                                     padx=10, pady=5)
            self.output_entry = tk.Entry(self.buffer_3d_window, width=50)
            self.output_entry.grid(row=2, column=1, padx=10, pady=5)

            tk.Label(self.buffer_3d_window, text="Distance du tampon (e.g., '100 Meters') :").grid(row=3, column=0,
                                                                                                   padx=10, pady=5)
            self.distance_entry = tk.Entry(self.buffer_3d_window, width=50)
            self.distance_entry.grid(row=3, column=1, padx=10, pady=5)

            tk.Button(self.buffer_3d_window, text="Exécuter le script",
                      command=lambda: run_arcpy_script(self.input_entry, self.centroid_entry, self.output_entry,
                                                       self.distance_entry)).grid(row=4, column=0, columnspan=3,
                                                                                  pady=20)

        except Exception as e:
            messagebox.showerror("Erreur", "Une erreur s'est produite lors de l'ouverture de l'outil Buffer 3D : ",e)

    def open_create_to3D_tool(self):
        try:
            self.create_3d_window = tk.Toplevel(self)
            self.create_3d_window.title("ArcPy Create 3D Features")

            tk.Label(self.create_3d_window, text="Sélectionnez le fichier de polygones :").grid(row=0, column=0,
                                                                                                padx=10, pady=5)
            self.input_entry = tk.Entry(self.create_3d_window, width=50)
            self.input_entry.grid(row=0, column=1, padx=10, pady=5)
            tk.Button(self.create_3d_window, text="Parcourir",
                      command=lambda: select_input_file(self.input_entry, self.populate_height_fields,
                                                        self.height_field_menu["menu"], self.height_field)).grid(row=0,
                                                                                                                 column=2,
                                                                                                                 padx=10,
                                                                                                                 pady=5)

            tk.Label(self.create_3d_window, text="Nom du fichier de sortie (sans extension) :").grid(row=1, column=0,
                                                                                                     padx=10, pady=5)
            self.output_entry = tk.Entry(self.create_3d_window, width=50)
            self.output_entry.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(self.create_3d_window, text="Champ de hauteur :").grid(row=2, column=0, padx=10, pady=5)
            self.height_field = tk.Entry(self.create_3d_window, width=50)
            self.height_field.grid(row=2, column=1, padx=10, pady=5)

            tk.Button(self.create_3d_window, text="Exécuter le script",
                      command=lambda: run_arcpy_script(self.input_entry, self.output_entry,
                                                          self.height_field.get())).grid(
                row=3, column=0, columnspan=3, pady=20)

        except Exception as e:
            messagebox.showerror("Erreur",
                                 "Une erreur s'est produite lors de l'ouverture de l'outil Create 3D Features : ", e)

    def open_buffer_tool(self):
        if self.dossier_geodatabase:
            self.buffer_tool.creer_buffer()
        else:
            tkMessageBox.showwarning("Attention", "Veuillez d'abord sélectionner une géodatabase.")

    def setup_ui(self):
        for widget in self.winfo_children():
            if isinstance(widget, OptionMenu) or isinstance(widget, Button):
                widget.destroy()

        feature_classes = self.buffer_tool.get_feature_classes()

        if not feature_classes:
            messagebox.showerror("Erreur", "Aucune couche trouvée dans l'espace de travail.")
        else:
            self.buffer_tool.selected_feature_class.set(feature_classes[0])

            # Dropdown for feature classes
            dropdown = OptionMenu(self, self.buffer_tool.selected_feature_class, *feature_classes)
            dropdown.pack(pady=10)

            # Button to create buffer
            bouton_creer_buffer = Button(self, text="Créer un buffer", command=self.buffer_tool.creer_buffer)
            bouton_creer_buffer.pack(pady=10)

            # Button to create intersection
            bouton_creer_intersection = Button(self, text="Créer une intersection", command=self.buffer_tool.creer_intersection_buffers)
            bouton_creer_intersection.pack(pady=10)

            # Filter and dropdown for polygon feature classes
            polygon_classes = [fc for fc in feature_classes if arcpy.Describe(fc).shapeType == "Polygon"]
            if polygon_classes:
                self.buffer_tool.selected_polygon_class.set(polygon_classes[0])

                polygon_dropdown = OptionMenu(self, self.buffer_tool.selected_polygon_class, *polygon_classes)
                polygon_dropdown.pack(pady=10)

                # Button to convert polygons to lines
                bouton_convertir_poly_en_lignes = Button(self, text="Convertir polygones en lignes", command=self.buffer_tool.convertir_polygone_en_lignes)
                bouton_convertir_poly_en_lignes.pack(pady=10)
            else:
                messagebox.showerror("Erreur", "Aucune couche de polygones trouvée dans l'espace de travail.")

            # Filter and dropdown for line feature classes
            line_classes = [fc for fc in feature_classes if arcpy.Describe(fc).shapeType == "Polyline"]
            if line_classes:
                selected_line_class = tk.StringVar(self)
                selected_line_class.set(line_classes[0])

                line_dropdown = OptionMenu(self, selected_line_class, *line_classes)
                line_dropdown.pack(pady=10)

    def choisir_geodatabase(self):
        # Créer une fenêtre parente pour la boîte de dialogue
        parent_window = self.winfo_toplevel()

        # Créer une fenêtre pour la saisie du chemin de la géodatabase
        fenetre_saisie = tk.Toplevel(parent_window)
        fenetre_saisie.title("Saisir le chemin de la géodatabase")
        fenetre_saisie.configure(bg="light blue")

        # Étiquette pour demander à l'utilisateur de saisir le chemin
        etiquette = tk.Label(fenetre_saisie, text="Veuillez saisir le chemin de la géodatabase:", bg="light blue")
        etiquette.pack(pady=10)

        # Champ de saisie pour le chemin de la géodatabase
        champ_saisie = tk.Entry(fenetre_saisie, width=50)
        champ_saisie.pack(pady=5)

        # Bouton pour valider la saisie
        bouton_valider = tk.Button(fenetre_saisie, text="Valider",
                                   command=lambda: self.valider_chemin_geodatabase(champ_saisie.get(), fenetre_saisie),
                                   width=20, height=2)
        bouton_valider.pack(pady=10)

    def valider_chemin_geodatabase(self, chemin, fenetre_saisie):
        if chemin:
            arcpy.env.workspace = chemin
            success_message = "Dossier de géodatabase {} importé avec succès".format(chemin)
            print(success_message)
            self.dossier_geodatabase = chemin
            fenetre_saisie.destroy()
            self.setup_ui()
        else:
            tkMessageBox.showwarning("Attention", "Veuillez saisir un chemin de géodatabase.")

    def choisir_traitement(self):
        if self.dossier_geodatabase:  # Vérifier si un dossier de géodatabase est sélectionné
            fenetre_traitement = tk.Toplevel(self)
            fenetre_traitement.title("Traitements sur les couches et Champs")
            fenetre_traitement.configure(bg="light blue")
            fenetre_traitement.geometry("600x150")  # Taille de la fenêtre (largeur x hauteur)

            # Titre
            titre = tk.Label(fenetre_traitement, text="Choisir une option de traitement", font=("Bodoni MT", 18),
                             bg="light blue")
            titre.pack()

            bouton_afficher_couches = tk.Button(fenetre_traitement, text="Afficher tous les couches", width=20,
                                                height=2,
                                                command=self.afficher_toutes_les_couches)
            bouton_afficher_couches.pack(side=tk.LEFT, padx=5, pady=5)

            bouton_traitement_champs = tk.Button(fenetre_traitement, text="Traitement sur champs", width=20, height=2,
                                                 command=self.traitement_champs)
            bouton_traitement_champs.pack(side=tk.LEFT, padx=5,
                                          pady=5)

            bouton_traitement_enregistrement = tk.Button(fenetre_traitement, text="Traitement d'enregistrement", width=20, height=2,
                                                         command=self.ouvrir_fenetre_traitement_enregistrement)
            bouton_traitement_enregistrement.pack(side=tk.LEFT, padx=5, pady=5)

            # Bouton de fermeture
            bouton_fermer = tk.Button(fenetre_traitement, text="Fermer", command=fenetre_traitement.destroy, width=20,
                                      height=2)
            bouton_fermer.pack(side=tk.LEFT, padx=5, pady=5)
        else:
            tkMessageBox.showwarning("Attention", "Veuillez d'abord sélectionner une géodatabase.")

    def ouvrir_fenetre_selection_table(self):
        couches = arcpy.ListFeatureClasses() + arcpy.ListTables()  # Obtenez une liste des couches disponibles
        if couches:
            fenetre_selection_table = tk.Toplevel(self)
            fenetre_selection_table.title("Sélectionner une table")
            fenetre_selection_table.configure(bg="light blue")

            titre = tk.Label(fenetre_selection_table, text="Sélectionner une table", font=("Bodoni MT", 18),
                             bg="light blue")
            titre.pack(pady=10)

            # Créez une liste déroulante pour sélectionner une table parmi les couches disponibles
            table_select = ttk.Combobox(fenetre_selection_table, values=couches)
            table_select.pack(pady=10)

            # Bouton pour valider la sélection de la table
            bouton_valider = tk.Button(fenetre_selection_table, text="Valider",
                                       command=lambda: self.valider_selection_table(table_select.get(),
                                                                                    fenetre_selection_table), width=20,
                                       height=2)
            bouton_valider.pack(pady=10)
        else:
            tkMessageBox.showwarning("Attention", "Aucune table disponible dans la géodatabase.")
    def selectionner_couche(self):
        if self.dossier_geodatabase:
            couches = arcpy.ListFeatureClasses() + arcpy.ListTables()
            if couches:
                fenetre_selection_couche = tk.Toplevel(self)
                fenetre_selection_couche.title("Sélectionner une couche")
                fenetre_selection_couche.configure(bg="light blue")

                titre = tk.Label(fenetre_selection_couche, text="Sélectionner une couche", font=("Bodoni MT", 18),
                                 bg="light blue")
                titre.pack(pady=10)

                couche_select = ttk.Combobox(fenetre_selection_couche, values=couches)
                couche_select.pack(pady=10)

                bouton_valider = tk.Button(fenetre_selection_couche, text="Valider",
                                           command=lambda: self.valider_selection_couche(couche_select.get(),
                                                                                         fenetre_selection_couche),
                                           width=20, height=2)
                bouton_valider.pack(pady=10)
            else:
                tkMessageBox.showwarning("Attention", "Aucune couche disponible dans la géodatabase.")
        else:
            tkMessageBox.showwarning("Attention", "Veuillez d'abord sélectionner une géodatabase.")
    def get_couches(self):
        """Retourne une liste de toutes les couches dans la géodatabase."""
        if self.dossier_geodatabase:
            arcpy.env.workspace = self.dossier_geodatabase
            return arcpy.ListFeatureClasses()
        else:
            tkMessageBox.showwarning("Attention", "Veuillez d'abord sélectionner une géodatabase.")
            return []

    def ouvrir_nom_couche_window(self):
        self.nom_couche_window = tk.Toplevel(self)
        self.nom_couche_window.title("Nom de la couche")
        self.nom_couche_window.configure(bg="light blue")
        self.nom_couche_window.geometry("300x200")

        self.label_nom_couche = tk.Label(self.nom_couche_window, text="Nom de la couche", font=("Bodoni MT", 14),
                                         bg="light blue")
        self.label_nom_couche.pack(pady=10)

        self.nom_couche_entry = tk.Entry(self.nom_couche_window, font=("Bodoni MT", 12))
        self.nom_couche_entry.pack(pady=10)

        self.bouton_valider_nom_couche = tk.Button(self.nom_couche_window, text="Valider",
                                                   command=self.valider_nom_couche, width=20, height=2)
        self.bouton_valider_nom_couche.pack(pady=10)

    def valider_nom_couche(self):
        self.nom_couche = self.nom_couche_entry.get()
        if self.nom_couche:
            tkMessageBox.showinfo("Nom de la couche", "Le nom de la couche est: ", self.nom_couche)
            self.nom_couche_window.destroy()
        else:
            tkMessageBox.showwarning("Attention", "Veuillez entrer un nom de couche.")
    def ouvrir_fenetre_statistiques(self):
        if self.dossier_geodatabase:
            ouvrir_fenetre_statistiques(self.dossier_geodatabase)
        else:
            tkMessageBox.showwarning("Attention", "Veuillez d'abord sélectionner une géodatabase.")

    def afficher_toutes_les_couches(self):
        if self.dossier_geodatabase:
            path = self.dossier_geodatabase  # Utiliser le dossier de géodatabase sélectionné
            afficher_couches(path)
        else:
            tkMessageBox.showwarning("Attention", "Veuillez d'abord sélectionner une géodatabase.")

    def traitement_champs(self):
        if self.dossier_geodatabase:
            fenetre_traitement = tk.Toplevel(self)
            fenetre_traitement.title("Traitements sur les champs")
            fenetre_traitement.configure(bg="light blue")
            fenetre_traitement.geometry("500x300")  # Taille de la fenêtre (largeur x hauteur)

            # Titre
            titre = tk.Label(fenetre_traitement, text="Choisir une option de traitement de champs",
                             font=("Bodoni MT", 18), bg="light blue")
            titre.grid(row=0, column=0, columnspan=2, pady=(10, 20),
                       sticky="n")  # Utilisation de sticky pour centrer le titre

            # Boutons Ajouter et Supprimer
            bouton_ajouter = tk.Button(fenetre_traitement, text="Ajouter un champ", width=20, height=2,
                                       command=self.ajouter_champs)
            bouton_ajouter.grid(row=1, column=0, padx=5, pady=5)

            bouton_supprimer = tk.Button(fenetre_traitement, text="Supprimer un champ", width=20, height=2,
                                         command=self.supprimer_champ)
            bouton_supprimer.grid(row=1, column=1, padx=5, pady=5)

            # Boutons Afficher et Remplir
            bouton_afficher = tk.Button(fenetre_traitement, text="Afficher les champs", width=20, height=2,
                                        command=self.afficher_champs)
            bouton_afficher.grid(row=2, column=0, padx=5, pady=10)

            bouton_remplir = tk.Button(fenetre_traitement, text="Remplir une colonne", width=20, height=2,
                                       command=self.remplir_colonne)
            bouton_remplir.grid(row=2, column=1, padx=5, pady=10)

            # Bouton pour ouvrir la fenêtre de statistiques
            self.bouton_statistiques = tk.Button(fenetre_traitement, text="Calculer Statistiques",
                                                 command=self.ouvrir_fenetre_statistiques, width=20, height=2)
            self.bouton_statistiques.grid(row=3, column=0, padx=10, pady=10)

            # Bouton de fermeture
            bouton_fermer = tk.Button(fenetre_traitement, text="Fermer", command=fenetre_traitement.destroy, width=20,
                                      height=2)
            bouton_fermer.grid(row=3, column=1, padx=10, pady=10)
        else:
            tkMessageBox.showwarning("Attention", "Veuillez d'abord sélectionner une géodatabase.")

    def ouvrir_nom_couche_window(self):
        if self.dossier_geodatabase:
            nom_couche_window = tk.Toplevel(self)
            nom_couche_window.title("Opérations sur la couche")
            nom_couche_window.configure(bg="light blue")

            # Titre
            titre = tk.Label(nom_couche_window, text="Choisir une option de traitement de couche",
                             font=("Bodoni MT", 18),
                             bg="light blue")
            titre.pack()

            bouton_ajouter = tk.Button(nom_couche_window, text="Ajouter", width=20, height=2,
                                       command=self.ajouter_couche)
            bouton_ajouter.pack(pady=10)

            bouton_supprimer = tk.Button(nom_couche_window, text="Supprimer", width=20, height=2,
                                         command=self.supprimer_couche)
            bouton_supprimer.pack(pady=10)

            bouton_fermer = tk.Button(nom_couche_window, text="Fermer", width=20, height=2,
                                      command=nom_couche_window.destroy)
            bouton_fermer.pack(pady=10)
        else:
            tkMessageBox.showwarning("Attention", "Veuillez d'abord sélectionner une géodatabase.")
    def ajouter_couche(self):
        if self.dossier_geodatabase:
            chemin_geodatabase = self.dossier_geodatabase  # Récupérer le chemin de la géodatabase
            ajouter_couche(chemin_geodatabase)  # Passer le chemin à la fonction ajouter_couche
        else:
            tkMessageBox.showwarning("Attention", "Veuillez d'abord sélectionner une géodatabase.")

    def supprimer_couche(self):
        if self.dossier_geodatabase:
            chemin_geodatabase = self.dossier_geodatabase  # Récupérer le chemin de la géodatabase
            supprimer_couche_ui(chemin_geodatabase)  # Passer le chemin à la fonction supprimer_couche
        else:
            tkMessageBox.showwarning("Attention", "Veuillez d'abord sélectionner une géodatabase.")

    def remplir_colonne(self):
        if self.dossier_geodatabase:
            chemin_geodatabase = self.dossier_geodatabase  # Récupérer le chemin de la géodatabase
            modifier_valeurs_ui(chemin_geodatabase)  # Passer le chemin à la fonction modifier_valeurs_ui
        else:
            tkMessageBox.showwarning("Attention", "Veuillez d'abord sélectionner une géodatabase.")

    def ajouter_champs(self):
        couches = obtenir_couches()
        if couches:
            app = AjouterChampApp(self, couches)
        else:
            tkMessageBox.showwarning("Attention", "Aucune couche disponible dans la géodatabase.")

    def supprimer_champ(self):
        couches = obtenir_couches()
        if couches:
            app = SupprimerChampApp(self, couches)
        else:
            tkMessageBox.showwarning("Attention", "Aucune couche disponible dans la géodatabase.")

    def ouvrir_fenetre_traitement_enregistrement(self):
        fenetre_enregistrement = tk.Toplevel(self)
        fenetre_enregistrement.title("Traitement d'enregistrement")
        fenetre_enregistrement.configure(bg="light blue")
        fenetre_enregistrement.geometry("600x150")  # Taille de la fenêtre (largeur x hauteur)

        titre = tk.Label(fenetre_enregistrement, text="Choisir une option de traitement", font=("Bodoni MT", 18),
                         bg="light blue")
        titre.pack()

        bouton_ajouter_enregistrement = tk.Button(fenetre_enregistrement, text="Ajouter enregistrement", width=20,
                                                  height=2,
                                                  command=self.ajouter_enregistrement)
        bouton_ajouter_enregistrement.pack(side=tk.LEFT, padx=5, pady=5)

        bouton_modifier_enregistrement = tk.Button(fenetre_enregistrement, text="Modifier enregistrement", width=20,
                                                   height=2,
                                                   command=self.valider_modification_enregistrement)
        bouton_modifier_enregistrement.pack(side=tk.LEFT, padx=5,
                                            pady=5)

        bouton_supprimer_enregistrement = tk.Button(fenetre_enregistrement, text="Supprimer enregistrement", width=20,
                                                    height=2,
                                                    command=self.ouvrir_fenetre_suppression_enregistrement)
        bouton_supprimer_enregistrement.pack(side=tk.LEFT, padx=5, pady=5)

        # Bouton de fermeture
        bouton_fermer = tk.Button(fenetre_enregistrement, text="Fermer", command=fenetre_enregistrement.destroy,
                                  width=20,
                                  height=2)
        bouton_fermer.pack(side=tk.LEFT, padx=5, pady=5)

    def ajouter_enregistrement(self):
        couches = obtenir_couches()
        if couches:
            self.ajouter_enregistrement_couche_arcgis(couches)
        else:
            messagebox.showwarning("Attention", "Aucune couche disponible dans la géodatabase.")

    def ouvrir_fenetre_suppression_enregistrement(self):
        couches = arcpy.ListFeatureClasses() + arcpy.ListTables()  # Obtenez une liste des couches disponibles
        if couches:
            fenetre_suppression = tk.Toplevel(self)
            fenetre_suppression.title("Supprimer un enregistrement")
            fenetre_suppression.configure(bg="light blue")

            titre = tk.Label(fenetre_suppression, text="Sélectionner une table et OBJECTID", font=("Bodoni MT", 18),
                             bg="light blue")
            titre.pack(pady=10)

            # Sélection de la table
            label_table = tk.Label(fenetre_suppression, text="Sélectionner une table:", bg="light blue")
            label_table.pack()
            table_select = ttk.Combobox(fenetre_suppression, values=couches)
            table_select.pack(pady=5)

            # Entrée pour l'OBJECTID
            label_objectid = tk.Label(fenetre_suppression, text="Entrer l'OBJECTID de l'enregistrement à supprimer:",
                                      bg="light blue")
            label_objectid.pack()
            entry_objectid = tk.Entry(fenetre_suppression)
            entry_objectid.pack(pady=5)

            bouton_valider = tk.Button(fenetre_suppression, text="Valider", width=20, height=2,
                                       command=lambda: self.valider_suppression_enregistrement(
                                           table_select.get(), entry_objectid.get(), fenetre_suppression))
            bouton_valider.pack(pady=10)
        else:
            messagebox.showinfo("Information", "Aucune couche ou table disponible.")

    def valider_suppression_enregistrement(self, table_name, objectid, fenetre_suppression):
        try:
            objectid = int(objectid)
            supprimer_enregistrement(self.dossier_geodatabase, table_name, objectid)
            tkMessageBox.showinfo("Succès", "Enregistrement supprimé avec succès.")
            fenetre_suppression.destroy()
        except ValueError:
            tkMessageBox.showerror("Erreur", "Veuillez entrer un OBJECTID valide.")
        except Exception as e:
            tkMessageBox.showerror("Erreur", "Une erreur est survenue: " , str(e))
    def afficher_champs(self):
        if self.dossier_geodatabase:
            afficher_champs_couche(self.dossier_geodatabase)
        else:
            tkMessageBox.showwarning("Attention", "Veuillez d'abord sélectionner une géodatabase.")



    def choisir_couche_et_modifier(self):
        fenetre = tk.Toplevel(self.root)
        fenetre.title("Choisir une couche et un enregistrement à modifier")

        if app.dossier_geodatabase:
            arcpy.env.workspace = app.dossier_geodatabase
            couches = self.get_couches()  # Obtenir la liste des couches

            if couches:
                couche_select = ttk.Combobox(fenetre, values=couches)
                couche_select.pack(pady=10)

                label_object_id = tk.Label(fenetre, text="Object ID :")
                label_object_id.pack()

                entry_object_id = tk.Entry(fenetre)
                entry_object_id.pack()

                label_nouvelles_valeurs = tk.Label(fenetre, text="Nouvelles valeurs :")
                label_nouvelles_valeurs.pack()

                entry_x = tk.Entry(fenetre)
                entry_x.pack()

                entry_y = tk.Entry(fenetre)
                entry_y.pack()

                bouton_valider = tk.Button(fenetre, text="Valider",
                                           command=lambda: self.valider_modification_enregistrement(couche_select.get(),
                                                                                                    entry_object_id.get(),
                                                                                                    {"X": entry_x.get(),
                                                                                                     "Y": entry_y.get()},
                                                                                                    fenetre),
                                           width=20, height=2)
                bouton_valider.pack(pady=10)
            else:
                messagebox.showwarning("Attention", "Aucune couche disponible dans la géodatabase.")
        else:
            messagebox.showwarning("Attention", "Veuillez d'abord sélectionner une géodatabase.")

    def valider_modification_enregistrement(self, couche, object_id, nouvelles_valeurs, fenetre):
        if couche and object_id and nouvelles_valeurs["X"] and nouvelles_valeurs["Y"]:
            table_path = os.path.join(app.dossier_geodatabase, couche)
            modifier_enregistrement(table_path, object_id, nouvelles_valeurs)
            fenetre.destroy()
        else:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")
    def fermer_application(self):
        self.destroy()
if __name__ == "__main__":
    app = ArcgisApp()
    app.mainloop()