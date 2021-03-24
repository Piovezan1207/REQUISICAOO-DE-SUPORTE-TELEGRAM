#pip install gspread oauth2client
#https://console.developers.google.com/project 

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('google_credentials/credentials.json', scope)

gc = gspread.authorize(credentials)

wks = gc.open_by_key('<KEY>')

worksheet = wks.get_worksheet(0)

def ler(tipo):
    if tipo == "salas":
        return worksheet.col_values(1)
    elif tipo == "id":
        return worksheet.col_values(2)
    elif tipo == "link":
        return worksheet.col_values(3)

def adicionar(tipo, dado):
    if tipo == "salas":
        tamanho = len(ler(tipo))
        worksheet.update_cell(tamanho+1 ,1, dado)

    elif tipo == "idA":
        worksheet.update_cell(1 ,2, '-'+dado)
    elif tipo == "idB":
        worksheet.update_cell(2 ,2, '-'+dado)

    elif tipo == "link":
        worksheet.update_cell(1 ,3,  str(dado))

def remover(dado):
    val = ler("salas")
    dado = dado.rstrip()

    if dado in val:
        local = val.index(dado)
        local = local+1
        worksheet.delete_rows(local)





