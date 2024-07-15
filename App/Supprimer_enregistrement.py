# -*- coding: utf-8 -*-
import arcpy
import os

def supprimer_enregistrement(dossier_geodatabase, table_name, objectid):
    """
    Supprime un enregistrement d'une table dans une géodatabase basée sur l'OBJECTID.

    :param dossier_geodatabase: Chemin du dossier de la géodatabase.
    :param table_name: Nom de la table contenant l'enregistrement à supprimer.
    :param objectid: OBJECTID de l'enregistrement à supprimer.
    """
    try:
        # Construire le chemin complet de la table
        table_path = os.path.join(dossier_geodatabase, table_name)

        # Construire la clause where pour l'OBJECTID
        where_clause = "OBJECTID = " , objectid

        # Utiliser un curseur pour supprimer l'enregistrement
        with arcpy.da.UpdateCursor(table_path, ["OBJECTID"], where_clause) as cursor:
            for row in cursor:
                cursor.deleteRow()
        print("Enregistrement avec OBJECTID = ", objectid , " supprimé avec succès de la table ", table_name)
    except arcpy.ExecuteError:
        print(arcpy.GetMessages(2))
    except Exception as e:
        print("Une erreur est survenue:", str(e))
