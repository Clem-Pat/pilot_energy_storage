import csv
import os
import pandas as pd
import xlsxwriter

path = os.path.dirname(os.path.abspath(__file__))

def convert_txt_to_csv(file_name):
    """file_name whithout the .txt"""

    file = open(f'{path}\\{file_name}.txt', "r")
    lines = list(file)
    n = len(lines)
    lines_done = [[] for i in range(n)]
    for i in range(n):
        if i%10 == 0: print(f'translating {i+1} out of {n}')
        words = lines[i].split(';')
        for j in range(len(words)):
            lines_done[i].append(words[j].replace('\n', ''))

    workbook = xlsxwriter.Workbook(f'{path}\\{file_name}_excel.xlsx')
    worksheet = workbook.add_worksheet()
    r = 0
    c = 0
    for row in lines_done:
        for item in row:
            if (r+c)%10 == 0 : print(f'writing {r+c+1} out of {n}')
            worksheet.write(r, c, float(item))
            c += 1
        c = 0
        r += 1
    workbook.close()
    file.close()
    print('done')

convert_txt_to_csv('sim')
