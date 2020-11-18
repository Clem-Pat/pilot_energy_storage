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

        read_file = pd.read_excel (path+'/Valeurs_capteur.xlsx')
        read_file.to_csv (path+'/Valeurs_capteur.csv', index=False, header=True)
        print('CSV file created')
        
    else:
        print('les listes doivent être de la même longueur')
