import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from zoneinfo import ZoneInfo
from textwrap import wrap
from matplotlib.offsetbox import TextArea, AnchoredOffsetbox
from matplotlib.table import Table
import textwrap
import matplotlib.image as mpimg





folha = pd.read_excel(r"Caminho da pasta")
agora_brasil = datetime.now(ZoneInfo("America/Sao_Paulo")) # Horário BR


##JUSTIFY
def justificar_texto(texto, largura):
    palavras = texto.split()
    linhas = []
    linha = []

    comprimento_linha = 0

    for palavra in palavras:
        if comprimento_linha + len(palavra) + len(linha) > largura:
            espacos_para_adicionar = largura - comprimento_linha
            if len(linha) == 1:
                linhas.append(linha[0].ljust(largura))
            else:
                for i in range(espacos_para_adicionar):
                    # Ensure index is within bounds of line
                    if len(linha) > 1:
                        linha[i % (len(linha) - 1)] += ' '
                    else:
                         # Handle case where there's only one word left in the line to justify
                         linha[0] += ' '
                linhas.append(''.join(linha))
            linha = []
            comprimento_linha = 0

        linha.append(palavra)
        comprimento_linha += len(palavra)

    # Última linha à esquerda
    linhas.append(' '.join(linha).ljust(largura))

    return '\n'.join(linhas)


def filtro(hu):
    all_units = hu

    #Tratamento da Providências
    folha["Providência"] = folha["Providência"].str.replace("Recomendação implementada ", "Recomendação implementada")
    folha["Providência"] = folha["Providência"].str.replace("Recomendação implementadaparcialmente", "Recomendação implementada parcialmente")

    #Tratamento UFPI
      ##GAD
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("UPAT/SAD/DAF/GAD/SUPRIN/HU-UFPI/EBSERH", "GAD/SUPRIN/HU-UFPI/EBSERH")
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("USOST/DIVGP/GAD/SUPRIN/HU-UFPI/EBSERH", "GAD/SUPRIN/HU-UFPI/EBSERH")
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("SAFS/DLIH/GAD/SUPRIN/HU-UFPI/EBSERH", "GAD/SUPRIN/HU-UFPI/EBSERH")
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("DIVGP/GAD/SUPRIN/HU-UFPI/EBSERH", "GAD/SUPRIN/HU-UFPI/EBSERH")
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("DLIH/GAD/SUPRIN/HU-UFPI/EBSERH", "GAD/SUPRIN/HU-UFPI/EBSERH")
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("SAD/DAF/GAD/SUPRIN/HU-UFPI/EBSERH", "GAD/SUPRIN/HU-UFPI/EBSERH")
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("SAFS/DLIH/GAD/SUPRIN/HU-UFPI/EBSERH", "GAD/SUPRIN/HU-UFPI/EBSERH")
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("SCONT/DAF/GAD/SUPRIN/HU-UFPI/EBSERH", "GAD/SUPRIN/HU-UFPI/EBSERH")
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("SEC/DLIH/GAD/SUPRIN/HU-UFPI/EBSERH", "GAD/SUPRIN/HU-UFPI/EBSERH")
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("UACE/SAFS/DLIH/GAD/SUPRIN/HU-UFPI/EBSERH", "GAD/SUPRIN/HU-UFPI/EBSERH")
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("UAP/DIVGP/GAD/SUPRIN/HU-UFPI/EBSERH", "GAD/SUPRIN/HU-UFPI/EBSERH")
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("UDP/DIVGP/GAD/SUPRIN/HU-UFPI/EBSERH", "GAD/SUPRIN/HU-UFPI/EBSERH")
      ##GAS
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("UBCPME/SADT/DGCADT/GAS/SUPRIN/HU-UFPI/EBSERH", "GAS/SUPRIN/HU-UFPI/EBSERH")
      ##GEP
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("UGPG/SGE/GEP/SUPRIN/HU-UFPI/EBSERH", "GEP/SUPRIN/HU-UFPI/EBSERH")
      ##SUPRIN
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("SEGOV/SUPRIN/HU-UFPI/EBSERH", "SUPRIN/HU-UFPI/EBSERH")
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("STCOR/SUPRIN/HU-UFPI/EBSERH", "SUPRIN/HU-UFPI/EBSERH")

    # Filtragem base para todas as unidades
    filtered_folha = folha[folha["Unidade Auditada"].isin(all_units)]

    # Conversão da coluna de data
    folha["Data de Fim"] = pd.to_datetime(folha["Data de Fim"], errors="coerce", dayfirst=True)

    # Filtra somente para "Atendidas" com Data de Fim em 2025
    atendidas_2025 = folha[
        (folha["Unidade Auditada"].isin(all_units)) &
        (folha["Providência"] == "Recomendação implementada") &
        (folha["Data de Fim"].dt.year == 2025)
    ]

    # Simplificar nomes das unidades
    filtered_folha["Unidade Simples"] = filtered_folha["Unidade Auditada"].str.split("/").str[0]
    atendidas_2025["Unidade Simples"] = atendidas_2025["Unidade Auditada"].str.split("/").str[0]
    hu_nome = hu[0].split("/")[1]

    # LOGO
    logo_path = (r"C:\Users\bruno.matsuda\OneDrive - EBSERH\PPP\logo.png")
    logo = mpimg.imread(logo_path)

    #CHAMADA DO JUSTIFY
    texto_intro = (f"Trata-se de avaliação do Plano de Providências Permanente PPP do {hu_nome}, conforme previsto no Plano Anual de Auditoria Interna (PAINT/2025), fundamentado no art. 19 da Instrução Normativa-CGU nº 05/2021 e no Estatuto de Auditoria Interna da Ebserh, art. 25.\n\n  A Auditoria Interna monitora o PPP por meio do Sistema e-CGU, no qual foram cadastradas as recomendações expedidas pela própria Auditoria Interna, pelos órgãos de controle interno e externo, pelo Conselho Fiscal, pelo Conselho de Administração e de outros órgãos ou entidades de regulação e fiscalização. Faz o acompanhamento gerencial do PPP por meio do Painel PPP, em que são apresentadas as informações estratégicas sobre o monitoramento, tratadas de forma detalhada no presente trabalho")
    largura=78
    t = justificar_texto(texto_intro, largura)

    with PdfPages(f"{hu_nome}.pdf") as pdf:
        fig, ax = plt.subplots(figsize=(8.5, 11))  # A4 retrato
        ax.axis('off')

        fig.figimage(logo, xo=295, yo=900, alpha=1, zorder=1)

        # Introdução
        titulo = f"Relatório de Monitoramento do\nPlano de Providências Permanente – {hu_nome}\n\n"
        introducao = "I - INTRODUÇÃO:\n\n"
        texto_intro = (
            f"           Trata-se de avaliação do Plano de Providências Permanente – PPP do {hu_nome},\nconforme previsto "
            "no Plano Anual de Auditoria Interna (PAINT/2025), fundamentado\nno art. 19 da Instrução Normativa-CGU "
            "nº 05/2021 e no Estatuto de Auditoria Interna\nda Ebserh, art. 25.\n\n"
            "           A Auditoria Interna monitora o PPP por meio do Sistema e-CGU, no qual foram cadastradas as recomendações "
            "expedidas pela própria Auditoria Interna, pelos órgãos\nde controle interno e externo, pelo Conselho Fiscal, "
            "pelo Conselho de Administração e\nde outros órgãos ou entidades de regulação e fiscalização. Faz o acompanhamento "
            "ge-\nrencial do PPP por meio do Painel PPP, em que são apresentadas as informações estraté-\ngicas sobre o monitoramento, "
            "tratadas de forma detalhada no presente trabalho.\n\n"
        )

        ax.text(0.5, 0.97, titulo, ha='center', va='top', fontsize=14, fontweight='bold')
        ax.text(0.5, 0.915, f"Relatório gerado em: {agora_brasil.strftime('%d/%m/%Y %H:%M')}", ha='center', va='top', fontsize=8, fontweight='bold')
        ax.text(0.02, 0.86, introducao, ha='left', va='top', wrap=True, fontsize=12, fontweight='bold')
        fig.text(0.1, 0.73, t, fontsize=10, va='top', ha='left', family='monospace')
        #ax.text(0.02, 0.82, texto_intro, ha='left', va='top', wrap=True, fontsize=10)

        # Tabela
        ax.text(0.02, 0.54, "II - APONTAMENTOS MONITORADOS NO PERÍODO:", ha='left', va='top', fontsize=12, fontweight='bold')

        # Criação da tabela
        tabela_apontamento = []
        for unidade in filtered_folha["Unidade Simples"].unique():
            atendidas = len(atendidas_2025[atendidas_2025["Unidade Simples"] == unidade])
            parcialmente = len(filtered_folha[
                (filtered_folha["Unidade Simples"] == unidade) &
                (filtered_folha["Providência"] == "Recomendação implementada parcialmente")
            ])
            nao_atendidas = len(filtered_folha[
                (filtered_folha["Unidade Simples"] == unidade) &
                (filtered_folha["Providência"] == "Não houve providência")
            ])
            total = atendidas + parcialmente + nao_atendidas

            tabela_apontamento.append({
                'Unidades': unidade,
                'Tot. Tarefas': total,
                '*Atendidas': atendidas,
                '% Atend.': f"{(atendidas * 100 / total):.2f}%" if total > 0 else "0.00%",
                'Parc. Atend.': parcialmente,
                '% Parc.': f"{(parcialmente * 100 / total):.2f}%" if total > 0 else "0.00%",
                'Não Atend.': nao_atendidas,
                '% Não Atend.': f"{(nao_atendidas * 100 / total):.2f}%" if total > 0 else "0.00%",
            })

        df = pd.DataFrame(tabela_apontamento)
        totais = {
            'Unidades': 'TOTAL',
            'Tot. Tarefas': df['Tot. Tarefas'].sum(),
            '*Atendidas': df['*Atendidas'].sum(),
            '% Atend.': '-',
            'Parc. Atend.': df['Parc. Atend.'].sum(),
            '% Parc.': '-',
            'Não Atend.': df['Não Atend.'].sum(),
            '% Não Atend.': '-',
        }
        df = pd.concat([df, pd.DataFrame([totais])], ignore_index=True)

        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            colLoc='center',
            loc='center',
            bbox=[0.02, 0.13, 0.99, 0.36]  # [x, y, width, height] - ajustado para caber junto com texto
        )
        table.auto_set_font_size(False)
        #table.scale(1.05, 2.0)
        table.set_fontsize(7.5)

        for (row, col), cell in table.get_celld().items():
            cell.get_text().set_ha('center')
            cell.get_text().set_va('center')
            if row == 0:
                cell.set_text_props(weight='bold')
                cell.set_facecolor('#f0f0f0')
            elif row == len(df):  # TOTAL
                cell.set_text_props(weight='bold')
                cell.set_facecolor('#e0e0e0')

        ax.text(0.02, 0.10,
                "*Foram consideradas como Tarefas Atendidas aquelas realizadas a partir de 01/01/2025, enquanto as não atendidas e as parcialmente atendidas foram consideradas as que previamente integravam o estoque.",
                ha='left', va='top', wrap=True, fontsize=9, style='italic')

        pdf.savefig(fig)
        plt.close()


        # Gráfico
        categorias = df['Unidades']
        atendidas = df['*Atendidas']
        parcial = df['Parc. Atend.']
        nao_atendidas = df['Não Atend.']

        x = np.arange(len(categorias))
        largura = 0.2  # largura da barra
        espaco = 0.22  # Espaçamento entre as barras

        # Gráfico + Texto Final 
        fig, ax = plt.subplots(figsize=(8.5, 11))  # A4 retrato
        ax.axis('off')

        fig.text(0.1, 0.95, "III - REPRESENTAÇÃO GRÁFICA DOS APONTAMENTOS:", ha='left', va='top', fontsize=12, fontweight='bold')

        graf_ax = fig.add_axes([0.1, 0.45, 0.8, 0.45])  # [x, y, largura, altura]

        graf_ax.bar(x - espaco, atendidas, width=largura, label='*Atendidas', color='green')
        graf_ax.bar(x, parcial, width=largura, label='Parcialmente Atendidas', color='orange')
        graf_ax.bar(x + espaco, nao_atendidas, width=largura, label='Não Atendidas', color='red')

        #graf_ax.set_title(f"Painel Atualizado em: {agora_brasil.strftime('%d/%m/%Y %H:%M')}")
        graf_ax.set_ylabel('Quantidade')
        graf_ax.set_xticks(x)
        graf_ax.set_xticklabels(categorias, rotation=45, ha='right')
        graf_ax.legend()

        graf_ax.bar_label(container=graf_ax.containers[0], fmt="%.0f", size=10, label_type="edge", padding=7)
        graf_ax.bar_label(container=graf_ax.containers[1], fmt="%.0f", size=10, label_type="edge", padding=7)
        graf_ax.bar_label(container=graf_ax.containers[2], fmt="%.0f", size=10, label_type="edge", padding=7)

        texto_final = (
            "Informamos que todos os apontamentos podem ser consultados no Sistema do e-CGU. Além disso,"
            " a Auditoria disponibilizou o Painel do PPP, que pode ser acessado na Intranet\nda Ebserh."
            "Por oportuno, esta Auditoria Interna se coloca à disposição para quaisquer esclarecimentos "
            "que se fizerem necessários."
        )
        largura=78
        t_final = justificar_texto(texto_final, largura)

        #fig.text(0.1, 0.33, texto_final, ha='left', va='top', wrap=True, fontsize=10, family='monospace')
        fig.text(0.1, 0.33, t_final, fontsize=10, va='top', ha='left',  wrap=True, family='monospace')

        pdf.savefig(fig)
        plt.close()


    return df


################################# CHAMADA DA FUNÇÃO ####################################
chc_ufpr = ["SUPRIN/CHC-UFPR/EBSERH", "GAD/SUPRIN/CHC-UFPR/EBSERH", "GAS/SUPRIN/CHC-UFPR/EBSERH", "GEP/SUPRIN/CHC-UFPR/EBSERH"]
ch_ufc = ["SUPRIN/CH-UFC/EBSERH", "GAD/SUPRIN/CH-UFC/EBSERH", "GAS1/SUPRIN/CH-UFC/EBSERH", "GAS2/SUPRIN/CH-UFC/EBSERH", "GEP/SUPRIN/CH-UFC/EBSERH"]
chu_ufpa = ["SUPRIN/CHU-UFPA/EBSERH", "GAD/SUPRIN/CHU-UFPA/EBSERH", "GAS1/SUPRIN/CHU-UFPA/EBSERH", "GEP/SUPRIN/CHU-UFPA/EBSERH"]
hc_ufg = ["SUPRIN/HC-UFG/EBSERH", "GAD/SUPRIN/HC-UFG/EBSERH", "GAS/SUPRIN/HC-UFG/EBSERH", "GEP/SUPRIN/HC-UFG/EBSERH"]
hc_ufmg = ["SUPRIN/HC-UFMG/EBSERH", "GAD/SUPRIN/HC-UFMG/EBSERH", "GAS/SUPRIN/HC-UFMG/EBSERH", "GEP/SUPRIN/HC-UFMG/EBSERH"]

hc_ufpe = ["SUPRIN/HC-UFPE/EBSERH", "GAD/SUPRIN/HC-UFPE/EBSERH", "GAS/SUPRIN/HC-UFPE/EBSERH", "GEP/SUPRIN/HC-UFPE/EBSERH"]
hc_uftm = ["SUPRIN/HC-UFTM/EBSERH", "GAD/SUPRIN/HC-UFTM/EBSERH", "GAS/SUPRIN/HC-UFTM/EBSERH", "GEP/SUPRIN/HC-UFTM/EBSERH"]
hc_ufu = ["SUPRIN/HC-UFU/EBSERH", "GAD/SUPRIN/HC-UFU/EBSERH", "GAS/SUPRIN/HC-UFU/EBSERH", "GEP/SUPRIN/HC-UFU/EBSERH"]
hdt_uft = ["SUPRIN/HDT-UFT/EBSERH", "GAD/SUPRIN/HDT-UFT/EBSERH", "GAS/SUPRIN/HDT-UFT/EBSERH", "GEP/SUPRIN/HDT-UFT/EBSERH"]
he_ufpel = ["SUPRIN/HE-UFPEL/EBSERH", "GAD/SUPRIN/HE-UFPEL/EBSERH", "GAS/SUPRIN/HE-UFPEL/EBSERH", "GEP/SUPRIN/HE-UFPEL/EBSERH"]

huab_ufrn = ["SUPRIN/HUAB-UFRN/EBSERH", "GAD/SUPRIN/HUAB-UFRN/EBSERH", "GAS/SUPRIN/HUAB-UFRN/EBSERH", "GEP/SUPRIN/HUAB-UFRN/EBSERH"]
huac_ufcg = ["SUPRIN/HUAC-UFCG/EBSERH", "GAD/SUPRIN/HUAC-UFCG/EBSERH", "GAS/SUPRIN/HUAC-UFCG/EBSERH", "GEP/SUPRIN/HUAC-UFCG/EBSERH"]
huap_uff = ["SUPRIN/HUAP-UFF/EBSERH", "GAD/SUPRIN/HUAP-UFF/EBSERH", "GAS/SUPRIN/HUAP-UFF/EBSERH", "GEP/SUPRIN/HUAP-UFF/EBSERH"]
hub_unb = ["SUP/HUB-UnB/EBSERH", "GAD/SUP/HUB-UnB/EBSERH", "GAS/SUP/HUB-UnB/EBSERH", "GEP/SUP/HUB-UnB/EBSERH"]
hucam_ufes = ["SUPRIN/HUCAM-UFES/EBSERH", "GAD/SUPRIN/HUCAM-UFES/EBSERH", "GAS/SUPRIN/HUCAM-UFES/EBSERH", "GEP/SUPRIN/HUCAM-UFES/EBSERH"]

hu_furg = ["SUPRIN/HU-FURG/EBSERH", "GAD/SUPRIN/HU-FURG/EBSERH", "GAS/SUPRIN/HU-FURG/EBSERH", "GEP/SUPRIN/HU-FURG/EBSERH"]
hugg_unirio = ["SUPRIN/HUGG-UNIRIO/EBSERH", "GAD/SUPRIN/HUGG-UNIRIO/EBSERH", "GAS/SUPRIN/HUGG-UNIRIO/EBSERH", "GEP/SUPRIN/HUGG-UNIRIO/EBSERH"]
hugv_ufam = ["SUPRIN/HUGV-UFAM/EBSERH", "GAD/SUPRIN/HUGV-UFAM/EBSERH", "GAS/SUPRIN/HUGV-UFAM/EBSERH", "GEP/SUPRIN/HUGV-UFAM/EBSERH"]
hujb_ufcg = ["SUPRIN/HUJB-UFCG/EBSERH", "GAD/SUPRIN/HUJB-UFCG/EBSERH", "GAS/SUPRIN/HUJB-UFCG/EBSERH", "GEP/SUPRIN/HUJB-UFCG/EBSERH"]
hujm_ufmt = ["SUPRIN/HUJM-UFMT/EBSERH", "GAD/SUPRIN/HUJM-UFMT/EBSERH", "GAS/SUPRIN/HUJM-UFMT/EBSERH", "GEP/SUPRIN/HUJM-UFMT/EBSERH", "HUJM-UFMT/EBSERH"]

hul_ufs = ["SUPRIN/HUL-UFS/EBSERH", "GAD/SUPRIN/HUL-UFS/EBSERH", "GAS/SUPRIN/HUL-UFS/EBSERH", "GEP/SUPRIN/HUL-UFS/EBSERH"]
hulw_ufpb = ["SUPRIN/HULW-UFPB/EBSERH", "GAD/SUPRIN/HULW-UFPB/EBSERH", "GAS/SUPRIN/HULW-UFPB/EBSERH", "GEP/SUPRIN/HULW-UFPB/EBSERH"]
humap_ufms = ["SUPRIN/HUMAP-UFMS/EBSERH", "GAD/SUPRIN/HUMAP-UFMS/EBSERH", "GAS/SUPRIN/HUMAP-UFMS/EBSERH", "GEP/SUPRIN/HUMAP-UFMS/EBSERH"]
huol_ufrn = ["SUPRIN/HUOL-UFRN/EBSERH", "GAD/SUPRIN/HUOL-UFRN/EBSERH", "GAS/SUPRIN/HUOL-UFRN/EBSERH", "GEP/SUPRIN/HUOL-UFRN/EBSERH"]
hupaa_ufal = ["SUPRIN/HUPAA-UFAL/EBSERH", "GAD/SUPRIN/HUPAA-UFAL/EBSERH", "GAS/SUPRIN/HUPAA-UFAL/EBSERH", "GEP/SUPRIN/HUPAA-UFAL/EBSERH"]

hupes_ufba = ["SUPRIN/HUPES-UFBA/EBSERH", "GAD/SUPRIN/HUPES-UFBA/EBSERH", "GAS/SUPRIN/HUPES-UFBA/EBSERH", "GEP/SUPRIN/HUPES-UFBA/EBSERH"]
husm_ufsm = ["SUPRIN/HUSM-UFSM/EBSERH", "GAD/SUPRIN/HUSM-UFSM/EBSERH", "GAS/SUPRIN/HUSM-UFSM/EBSERH", "GEP/SUPRIN/HUSM-UFSM/EBSERH"]
hu_ufgd = ["SUPRIN/HU-UFGD/EBSERH", "GAD/SUPRIN/HU-UFGD/EBSERH", "GAS/SUPRIN/HU-UFGD/EBSERH", "GEP/SUPRIN/HU-UFGD/EBSERH"]
hu_ufjf = ["SUPRIN/HU-UFJF/EBSERH", "GAD/SUPRIN/HU-UFJF/EBSERH", "GAS/SUPRIN/HU-UFJF/EBSERH", "GEP/SUPRIN/HU-UFJF/EBSERH"]
hu_ufma = ["SUPRIN/HU-UFMA/EBSERH", "GAD/SUPRIN/HU-UFMA/EBSERH", "GAS/SUPRIN/HU-UFMA/EBSERH", "GEP/SUPRIN/HU-UFMA/EBSERH","HU-UFMA/EBSERH"]

hu_ufpi = ["SUPRIN/HU-UFPI/EBSERH","SEGOV/SUPRIN/HU-UFPI/EBSERH",
           "GAD/SUPRIN/HU-UFPI/EBSERH", "SAFS/DLIH/GAD/SUPRIN/HU-UFPI/EBSERH", "DIVGP/GAD/SUPRIN/HU-UFPI/EBSERH", "DLIH/GAD/SUPRIN/HU-UFPI/EBSERH", "SAD/DAF/GAD/SUPRIN/HU-UFPI/EBSERH", "SAFS/DLIH/GAD/SUPRIN/HU-UFPI/EBSERH", "SCONT/DAF/GAD/SUPRIN/HU-UFPI/EBSERH", "SEC/DLIH/GAD/SUPRIN/HU-UFPI/EBSERH", "UACE/SAFS/DLIH/GAD/SUPRIN/HU-UFPI/EBSERH", "UAP/DIVGP/GAD/SUPRIN/HU-UFPI/EBSERH", "UDP/DIVGP/GAD/SUPRIN/HU-UFPI/EBSERH", "UPAT/SAD/DAF/GAD/SUPRIN/HU-UFPI/EBSERH", "USOST/DIVGP/GAD/SUPRIN/HU-UFPI/EBSERH",
           "GAS/SUPRIN/HU-UFPI/EBSERH", "UBCPME/SADT/DGCADT/GAS/SUPRIN/HU-UFPI/EBSERH",
           "GEP/SUPRIN/HU-UFPI/EBSERH", "STCOR/SUPRIN/HU-UFPI/EBSERH", "UGPG/SGE/GEP/SUPRIN/HU-UFPI/EBSERH"]
hu_ufs = ["SUPRIN/HU-UFS/EBSERH", "GAD/SUPRIN/HU-UFS/EBSERH", "GAS/SUPRIN/HU-UFS/EBSERH", "GEP/SUPRIN/HU-UFS/EBSERH"]
hu_ufsc = ["SUPRIN/HU-UFSC/EBSERH", "GAD/SUPRIN/HU-UFSC/EBSERH", "GAS/SUPRIN/HU-UFSC/EBSERH", "GEP/SUPRIN/HU-UFSC/EBSERH", "HU-UFSC/EBSERH"]
hu_ufscar = ["SUPRIN/HU-UFSCAR/EBSERH", "GAD/SUPRIN/HU-UFSCAR/EBSERH", "GAS/SUPRIN/HU-UFSCAR/EBSERH", "GEP/SUPRIN/HU-UFSCAR/EBSERH"]
hu_unifap = ["SUP/HU-UNIFAP/EBSERH", "GAD/SUP/HU-UNIFAP/EBSERH", "GAS/SUP/HU-UNIFAP/EBSERH", "GEP/SUP/HU-UNIFAP/EBSERH"]

hu_univasf = ["SUPRIN/HU-UNIVASF/EBSERH", "GAD/SUPRIN/HU-UNIVASF/EBSERH", "GAS/SUPRIN/HU-UNIVASF/EBSERH", "GEP/SUPRIN/HU-UNIVASF/EBSERH"]
mco_ufba = ["SUPRIN/MCO-UFBA/EBSERH", "GAD/SUPRIN/MCO-UFBA/EBSERH", "GAS/SUPRIN/MCO-UFBA/EBSERH", "GEP/SUPRIN/MCO-UFBA/EBSERH", "MCO-UFBA/EBSERH"]
mejc_ufrn = ["SUPRIN/MEJC-UFRN/EBSERH", "GAD/SUPRIN/MEJC-UFRN/EBSERH", "GAS/SUPRIN/MEJC-UFRN/EBSERH", "GEP/SUPRIN/MEJC-UFRN/EBSERH"]
ch_ufrj = ["SUPAD/CH-UFRJ/EBSERH", "SETI/CH-UFRJ/EBSERH", "SEGOV/CH-UFRJ/EBSERH", "SUPEP/CH-UFRJ/EBSERH", "CH-UFRJ/EBSERH"]

hu_lists_to_process = [
    chc_ufpr, ch_ufc, chu_ufpa, hc_ufg, hc_ufmg, hc_ufpe, hc_uftm, hc_ufu, hdt_uft, he_ufpel,
    huab_ufrn, huac_ufcg, huap_uff, hub_unb, hucam_ufes, hu_furg, hugg_unirio, hugv_ufam, hujb_ufcg, hujm_ufmt,
    hul_ufs, hulw_ufpb, humap_ufms, huol_ufrn, hupaa_ufal, hupes_ufba, husm_ufsm, hu_ufgd, hu_ufjf, hu_ufma,
    hu_ufpi, hu_ufs, hu_ufsc, hu_ufscar, hu_unifap, hu_univasf, mco_ufba, mejc_ufrn, ch_ufrj
]
 # Add other lists here as needed

for h_list in hu_lists_to_process:
  df = filtro(h_list)

