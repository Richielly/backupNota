import csv

def file_csv(nome, dados):
  arq = open(nome+'.csv', 'w', newline='', encoding='utf-8')
  rel = csv.writer(arq, delimiter=';')
  for i in dados:
    rel.writerow(i)
