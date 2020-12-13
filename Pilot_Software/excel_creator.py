import os
import pandas as pd
import openpyxl


class Excel_manager():
    def __init__(self, app):
        self.app = app
        self.excel_names_already_used = []

        if path == None: self.path = self.find_file_path()
        else: self.path = path

        if name == None: self.name = self.find_file_name()
        else: self.name = name

        self.L_data = L_data
        self.data_dic = {"temps": L_data[0], "distance mesurée": L_data[1], "vitesse rotation": L_data[2], "bits envoyés": L_data[3], "motor_is_on" : L_data[4]}


    def find_file_name(self):
        title = "Expérience_"
        date = datetime.date.today().strftime("%d/%m/%Y").split("/")
        today = str(date[0] + "-" + date[1])
        comment = ""
        if self.app != None:
            if self.app.entrys[1]["fg"] == "green":
                comment = "_" + str(self.app.entrys[1].get())
        name = str(title + today + comment)
        i = 1
        if self.board.arduinoboard == None:
            while str(name + "_TEST" + "(" + str(i) + ")") in self.excel_names_already_used: i += 1
            name = str(name + "_TEST" + "(" + str(i) + ")")
        else:
            while str(name + "(" + str(i) + ")") in self.excel_names_already_used: i += 1
            name = str(name + "(" + str(i) + ")")
        self.excel_names_already_used.append(name)
        print("will create", name, f"{len(self.time_list)} values")
        return name

    def find_file_path(self):
        date = datetime.date.today().strftime("%d/%m/%Y").split("/")
        today = str(date[0] + "-" + date[1])
        folder_path = self.path + "/" + today
        try: os.mkdir(folder_path) #si le dossier n"existe pas on le crée
        except FileExistsError: pass #si le dossier existe déjà on ne fait rien
        return folder_path

    def create_excel(self):
        """crée le fichier excel de l"expérience"""
        if len(self.L_data[0]) == len(self.L_data[1]):
            df = pd.DataFrame(self.data_dic)

            writer = pd.ExcelWriter(self.path+"/"+self.name+".xlsx")
            df.to_excel(writer, sheet_name="Valeurs", index=False)

            writer.save()

            read_file = pd.read_excel (self.path+"/"+self.name+".xlsx")
            read_file.to_csv (self.path+"/"+self.name+".csv", index=False, header=True)

            print("CSV and Excel file created \n")
            return True

        else:
            print("les listes doivent être de la même longueur")
            return False
