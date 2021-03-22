import os
import pandas as pd
import openpyxl
import datetime


class Excel_manager():
    def __init__(self, app):
        self.app = app
        self.project_path = os.path.dirname(os.path.abspath(__file__))

    def find_file_name(self, path):
        """find a proper file name that doesn't exist already : enables the user to avoid crushing old data records"""
        date = datetime.date.today().strftime('%d/%m/%Y').split('/')
        today = f'{date[0]}-{date[1]}'
        if self.app.entrys[1]['fg'] == 'green': comment = f'_{str(self.app.entrys[1].get())}'
        else: comment = ''
        name = f'Expérience_{today}{comment}'
        i = 1
        if self.app.board.arduinoboard == None:
            while os.path.isfile(path+f'\\{name}_TEST({i}).csv'): i += 1
            name =  f'{name}_TEST({i})'
        else:
            while os.path.isfile(path+f'\\{name}({i}).csv'): i += 1
            name =  f'{name}({i})'
        print(f'will create {name} ({len(self.data_dic["Temps (s)"])} values) at :')
        print(path+'\\'+name+'.csv')
        return name

    def find_file_path(self):
        """find a proper file path : enables the user to have clear tree structure"""
        date = datetime.date.today().strftime('%d/%m/%Y').split('/')
        today = f'{date[0]}-{date[1]}'
        folder_path = f'{self.project_path}\\{today}'
        try: os.mkdir(folder_path) #si le dossier n'existe pas on le crée
        except FileExistsError: pass #si le dossier existe déjà on ne fait rien
        return folder_path

    def data_from_list_to_dict(self,L_data):
        """translates the list of data to dictionnary (useful for excel creation)"""
        return {"Temps (s)": L_data[0], "Tension mesurée (V)": L_data[1], "Tension mesurée 2 (V)": L_data[2], "Intensité mesurée (A)": L_data[3], "Position Angulaire (rad)": L_data[4], "Vitesse rotation (rad/s)": L_data[5],  "Distance mesurée (cm)": L_data[6], "Bits envoyés": L_data[7], "Moteur allumé" : L_data[8]}

    def print_in_console(self, successed, path, name):
        """send a message back to the user in the console of the application"""
        def console_text_back_to_normal():
            self.app.canvas[0].itemconfig(2, text=old_text, fill=old_color)

        if successed:
            print("CSV and Excel file created \n")
            old_text, old_color = self.app.canvas[0].itemcget(2, 'text'), self.app.canvas[0].itemcget(2, 'fill')
            self.app.canvas[0].itemconfig(2, text=f'Fichier {name} créé ({len(self.L_data[0])} valeurs)', fill='green')
            self.app.last_excel_created = f'{path}/{name}.xlsx'
            self.app.after(3000, console_text_back_to_normal)
        else:
            lists_lengths = str(','.join([str(len(x)) for x in self.L_data]))
            print(f'Lists must have the same length ! ({lists_lengths}) \n')
            old_text, old_color = self.app.canvas[0].itemcget(2, 'text'), self.app.canvas[0].itemcget(2, 'fill')
            self.app.canvas[0].itemconfig(2, text=f'Les listes ne sont pas de la même taille !', fill='red')
            self.app.after(3000, console_text_back_to_normal)

    def create_excel(self, L_data):
        """crée le fichier excel de l'expérience"""
        self.L_data = L_data
        self.data_dic = self.data_from_list_to_dict(self.L_data)
        path = self.find_file_path()
        name = self.find_file_name(path)
        if len(set(map(len, self.L_data))) in (0, 1): #Toutes les listes sont de même taille, on peut créer l'excel
            data_frame = pd.DataFrame(self.data_dic)
            writer = pd.ExcelWriter(f'{path}/{name}.xlsx')
            data_frame.to_excel(writer, index=False)
            writer.save()
            read_file = pd.read_excel(f'{path}/{name}.xlsx')
            read_file.to_csv(f'{path}/{name}.csv', index=False, header=True)

            self.print_in_console(True, path, name)
        else:
            self.print_in_console(False, None, None)
