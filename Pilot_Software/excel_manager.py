import os
import pandas as pd
import openpyxl
import datetime


class Excel_manager():
    def __init__(self, app):
        self.app = app
        self.excel_names_already_used = []
        self.project_path = os.path.dirname(os.path.abspath(__file__))

    def find_file_name(self):
        date = datetime.date.today().strftime('%d/%m/%Y').split('/')
        today = f'{date[0]}-{date[1]}'
        if self.app.entrys[1]['fg'] == 'green': comment = f'_{str(self.app.entrys[1].get())}'
        else: comment = ''
        name = f'Expérience_{today}{comment}'
        i = 1
        if self.app.board.arduinoboard == None:
            while f'{name}_TEST({i})' in self.excel_names_already_used: i += 1
            name = f'{name}_TEST({i})'
        else:
            while f'{name}({i})' in self.excel_names_already_used: i += 1
            name = f'{name}({i})'
        self.excel_names_already_used.append(name)
        print(f'will create {name} ({len(self.data_dic["Temps (s)"])} values)')
        return name

    def find_file_path(self):
        date = datetime.date.today().strftime('%d/%m/%Y').split('/')
        today = f'{date[0]}-{date[1]}'
        folder_path = f'{self.project_path}/{today}'
        try: os.mkdir(folder_path) #si le dossier n'existe pas on le crée
        except FileExistsError: pass #si le dossier existe déjà on ne fait rien
        return folder_path

    def data_from_list_to_dict(self,L_data):
        return {"Temps (s)": L_data[0], "Tension mesurée (V)": L_data[1], "Position Angulaire (rad)": L_data[2], "Vitesse rotation (rad/s)": L_data[3],  "Distance mesurée (cm)": L_data[4], "Bits envoyés": L_data[5], "Moteur allumé" : L_data[6]}

    def print_in_console(self, successed, name):
        def console_text_back_to_normal():
            self.app.canvas[0].itemconfig(2, text=old_text, fill=old_color)

        if successed:
            print("CSV and Excel file created \n")
            old_text, old_color = self.app.canvas[0].itemcget(2, 'text'), self.app.canvas[0].itemcget(2, 'fill')
            self.app.canvas[0].itemconfig(2, text=f'Fichier {name} créé ({len(self.L_data[0])} valeurs)', fill='green')
            self.app.fen.after(3000, console_text_back_to_normal)
        else:
            lists_lengths = str(','.join([str(len(x)) for x in self.L_data]))
            print(f'Lists must have the same length ! ({lists_lengths}) \n')
            old_text, old_color = self.app.canvas[0].itemcget(2, 'text'), self.app.canvas[0].itemcget(2, 'fill')
            self.app.canvas[0].itemconfig(2, text=f'Les listes ne sont pas de la même taille !', fill='red')
            self.app.fen.after(3000, console_text_back_to_normal)

    def create_excel(self, L_data):
        """crée le fichier excel de l'expérience"""
        self.L_data = L_data
        self.data_dic = self.data_from_list_to_dict(self.L_data)
        path = self.find_file_path()
        name = self.find_file_name()
        if len(set(map(len, self.L_data))) in (0, 1): #Toutes les listes sont de même taille, on peut créer l'excel
            data_frame = pd.DataFrame(self.data_dic)
            writer = pd.ExcelWriter(f'{path}/{name}.xlsx')
            data_frame.to_excel(writer, index=False)
            writer.save()
            # print(f'{path}/{name}.xlsx')
            read_file = pd.read_excel(f'{path}/{name}.xlsx')
            read_file.to_csv(f'{path}/{name}.csv', index=False, header=True)

            self.print_in_console(True, name)
        else:
            self.print_in_console(False, None)
