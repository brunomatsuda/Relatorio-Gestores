import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

agora_brasil = datetime.now(ZoneInfo("America/Sao_Paulo"))

def processar_dados(hu, folha):
    folha["Providência"] = folha["Providência"].str.replace("Recomendação implementada ", "Recomendação implementada")
    folha["Providência"] = folha["Providência"].str.replace("Recomendação implementadaparcialmente", "Recomendação implementada parcialmente")

    folha["Data de Fim"] = pd.to_datetime(folha["Data de Fim"], errors="coerce", dayfirst=True)

    all_units = hu
    filtered_folha = folha[folha["Unidade Auditada"].isin(all_units)].copy()
    filtered_folha["Unidade Simples"] = filtered_folha["Unidade Auditada"].str.split("/").str[0]

    atendidas_2025 = folha[
        (folha["Unidade Auditada"].isin(all_units)) &
        (folha["Providência"] == "Recomendação implementada") &
        (folha["Data de Fim"].dt.year == 2025)
    ].copy()
    atendidas_2025["Unidade Simples"] = atendidas_2025["Unidade Auditada"].str.split("/").str[0]

    return {
        "filtered": filtered_folha,
        "atendidas_2025": atendidas_2025,
        "hu_nome": hu[0].split("/")[1],
        "agora": agora_brasil
    }
