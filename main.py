import time
import cx_Oracle
import script as script
import arquivo as doc
from datetime import date
import configparser
import PySimpleGUI as sg

cfg = configparser.ConfigParser()
cfg.read('cfg.ini')

data = date.today()

conexao = (cfg['DEFAULT']['DataBase'] + '/' + cfg['DEFAULT']['Password'] + '@' + cfg['DEFAULT']['Server'])

if data.year == 2022:
    con = cx_Oracle.connect(str(conexao))
    cur = con.cursor()

    arquivos = script.scripts.keys()

def start():
    tamanho = 0
    event, values = window.read()
    print('Conectado no banco de dados: ' + conexao)
    while True:
        if event == 'Iniciar':
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                break
            for export in arquivos:
                tamanho += 1
                window['status'].update('Arquivo ' + str(tamanho) + '/' + str(len(arquivos)))
                print('Arquivo: ' + export + ' iniciado em ' + time.strftime("%d/%m/%y %H:%M:%S"))
                cur.execute(script.scripts[export])
                doc.file_csv(export+'_' + cfg['DEFAULT']['codEntidade'] + '_' + str(data), list(cur))
                print('Arquivo: ' + export + ' finalizado em ' + time.strftime("%d/%m/%y %H:%M:%S") + '\n')

                progress_bar.UpdateBar(tamanho)
                time.sleep(1)

            time.sleep(2)
            sg.SystemTray.notify('Arquivos gerados com sucesso.', cfg['DEFAULT']['NomeEntidade'].replace("'", ''))
        cur.close()
        con.close()
        break

layout = [[sg.Text('Gerando Arquivos')],
          [sg.Text('0/'+str(len(arquivos)), key='status')],
          [sg.Output(size=(80,20))],
          [sg.ProgressBar(len(arquivos), orientation='h', size=(53, 20), key='progressbar')],
          [sg.OK('Iniciar'), sg.Cancel()]]
        # create the window`
window = sg.Window('Backup ESNFS entidade - ' + cfg['DEFAULT']['CodEntidade'] + ' - ' + cfg['DEFAULT']['NomeEntidade'].replace("'",''), layout, icon='equiplano.ico')
progress_bar = window['progressbar']

start()

# pyinstaller --name backup_nota --onefile --noconsole main.py