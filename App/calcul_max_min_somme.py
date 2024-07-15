# -*- coding: utf-8 -*-
import arcpy
import Tkinter as tk
import ttk
import tkMessageBox

def est_numerique(field):
    return field.type in ['Double', 'Integer', 'Single', 'SmallInteger']


def calculer_statistiques(champ, geodabase):
    try:
        valeurs = []
        with arcpy.da.SearchCursor(geodabase, [champ]) as cursor:
            for row in cursor:
                valeurs.append(row[0])

        max_valeur = max(valeurs)
        min_valeur = min(valeurs)
        somme_valeur = sum(valeurs)
        moyenne_valeur = somme_valeur / len(valeurs)

        tkMessageBox.showinfo("Statistiques",
                              "Nombre d'enregistrements : {}\nMax: {}\nMin: {}\nSomme: {}\nMoyenne: {:.2f}".format(
                                  len(valeurs), max_valeur, min_valeur, somme_valeur, moyenne_valeur))
    except arcpy.ExecuteError:
        tkMessageBox.showerror("Erreur", arcpy.GetMessages(2))
    except Exception as e:
        tkMessageBox.showerror("Erreur", str(e))


def ouvrir_fenetre_statistiques(geodabase):
    def calculer(champ_combobox, couche_combobox):  # Passer champ_combobox et couche_combobox en arguments
        champ = champ_combobox.get()
        couche = couche_combobox.get()
        if champ and couche:
            calculer_statistiques(champ, couche)
        else:
            tkMessageBox.showwarning("Avertissement",
                                     "Veuillez sélectionner une couche et un champ pour calculer les statistiques.")

    fenetre = tk.Tk()
    fenetre.title("Calculer les statistiques d'un champ")
    fenetre.configure(bg="light blue")

    # Titre
    titre = tk.Label(fenetre, text="Calculer les statistiques d'un champ", font=("Bodoni MT", 18), bg="light blue")
    titre.pack(pady=10)

    # Sélection de la couche
    tk.Label(fenetre, text="Sélectionnez la couche:", bg="light blue").pack(pady=5)
    couche_var = tk.StringVar()
    couche_combobox = ttk.Combobox(fenetre, textvariable=couche_var)
    couche_combobox.pack(pady=5)

    # Sélection du champ
    tk.Label(fenetre, text="Sélectionnez le champ:", bg="light blue").pack(pady=5)
    champ_var = tk.StringVar()
    champ_combobox = ttk.Combobox(fenetre, textvariable=champ_var)
    champ_combobox.pack(pady=5)

    # Bouton pour calculer les statistiques
    bouton_calculer = tk.Button(fenetre, text="Calculer les statistiques", command=lambda: calculer(champ_combobox, couche_combobox))
    bouton_calculer.pack(pady=10)

    # Bouton pour fermer la fenêtre
    bouton_fermer = tk.Button(fenetre, text="Fermer", command=fenetre.destroy)
    bouton_fermer.pack(pady=10)

    # Remplir les options des combobox avec les couches et champs disponibles
    try:
        couches = arcpy.ListFeatureClasses()  # Liste des couches disponibles dans la géodatabase
        couche_combobox['values'] = couches

        # Fonction pour mettre à jour les champs en fonction de la couche sélectionnée
        def update_champs(event):
            selected_couche = couche_combobox.get()
            if selected_couche:
                fields = arcpy.ListFields(selected_couche)
                champs_couche = [field.name for field in fields if est_numerique(field)]
                champ_combobox['values'] = champs_couche

        # Associer la fonction update_champs à l'événement de sélection de la combobox de la couche
        couche_combobox.bind("<<ComboboxSelected>>", update_champs)

    except arcpy.ExecuteError:
        tkMessageBox.showerror("Erreur", arcpy.GetMessages(2))
    except Exception as e:
        tkMessageBox.showerror("Erreur", str(e))

    fenetre.mainloop()