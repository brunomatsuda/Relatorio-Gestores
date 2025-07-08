import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from relatorio import filtro


folha = pd.read_excel(r"Caminho da pasta")
agora_brasil = datetime.now(ZoneInfo("America/Sao_Paulo"))

#Passando os filtros de consulta de cada HU
chc_ufpr = ["XXXXX/YYYYY/ZZZZ", "XXXXX/YYYYY/ZZZZ", "XXXXX/YYYYY/ZZZZ", "XXXXX/YYYYY/ZZZZ"]
ch_ufc = ["XXXXX/YYYYY/ZZZZ", "XXXXX/YYYYY/ZZZZ", "XXXXX/YYYYY/ZZZZ", "XXXXX/YYYYY/ZZZZ"]
chu_ufpa = ["XXXXX/YYYYY/ZZZZ", "XXXXX/YYYYY/ZZZZ", "XXXXX/YYYYY/ZZZZ", "XXXXX/YYYYY/ZZZZ"]
hc_ufg = ["XXXXX/YYYYY/ZZZZ", "XXXXX/YYYYY/ZZZZ", "XXXXX/YYYYY/ZZZZ", "XXXXX/YYYYY/ZZZZ"]
hc_ufmg = ["XXXXX/YYYYY/ZZZZ", "XXXXX/YYYYY/ZZZZ", "XXXXX/YYYYY/ZZZZ", "XXXXX/YYYYY/ZZZZ"]

hu_lists_to_process = [
    chc_ufpr, ch_ufc, chu_ufpa, hc_ufg, hc_ufmg
]

# Chamando o arquivo que gera o pdf
for h_list in hu_lists_to_process:
  df = filtro(h_list)