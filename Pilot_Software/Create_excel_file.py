import os
import pandas as pd
import openpyxl


def create_excel(L0, L1, L2, L3, L4, path, name):
    """crée le fichier excel de l'expérience"""
    if len(L0) == len(L1):
        df = pd.DataFrame({ 'temps':L0,
                            'distance mesurée': L1,
                            'vitesse rotation': L2,
                            'bits envoyés': L3, 
                            'motor_is_on' : L4})

        writer = pd.ExcelWriter(path+'/'+name+'.xlsx')
        df.to_excel(writer, sheet_name='Valeurs', index=False)

        writer.save()

        read_file = pd.read_excel (path+'/'+name+'.xlsx')
        read_file.to_csv (path+'/'+name+'.csv', index=False, header=True)

        print('CSV and Excel file created \n')
        return True

    else:
        print('les listes doivent être de la même longueur')
        return False
