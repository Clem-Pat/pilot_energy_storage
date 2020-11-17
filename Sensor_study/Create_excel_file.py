import os
import pandas as pd
import openpyxl


def create_excel(L0,L1,path):
    """crée le fichier excel de l'expérience"""
    if len(L0) == len(L1):
        df = pd.DataFrame({ 'reel':L0,
                            'capteur': L1})

        writer = pd.ExcelWriter(path+'/Valeurs_capteur.xlsx')
        df.to_excel(writer, sheet_name='Valeurs', index=False)
        
        writer.save()
        print('Excel file created')
    else:
        print('les listes doivent être de la même longueur')
