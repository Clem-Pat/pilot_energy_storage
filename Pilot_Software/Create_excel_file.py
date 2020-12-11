import os
import pandas as pd
import openpyxl


def create_excel(L0, L1, L2, L3, L4, L5, path, name):
    """crée le fichier excel de l'expérience"""
    if len(L0) == len(L1) and len(L0) == len(L2) and len(L0) == len(L3) and len(L0) == len(L4) and len(L0) == len(L5):
        df = pd.DataFrame({ 'temps':L0,
                            'tension aux bornes du moteur': L1,
                            'distance mesurée': L2,
                            'vitesse de rotation mesurée': L3,
                            'bits envoyés': L4,
                            'motor_is_on' : L5})

        writer = pd.ExcelWriter(path+'/'+name+'.xlsx')
        df.to_excel(writer, sheet_name='Valeurs', index=False)

        writer.save()

        read_file = pd.read_excel (path+'/'+name+'.xlsx')
        read_file.to_csv (path+'/'+name+'.csv', index=False, header=True)

        print('CSV and Excel file created \n')
        return True

    else:
        print('les listes doivent être de la même longueur (',len(L0),len(L1), len(L2), len(L3), len(L4), len(L5),')')
        return False
