import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import numpy as np
from modules.text_utils import justificar_texto

def gerar_relatorio(hu, dados):
    folha = dados["filtered"]
    atendidas_2025 = dados["atendidas_2025"]
    hu_nome = dados["hu_nome"]
    agora_brasil = dados["agora"]

    logo = mpimg.imread(r"assets/logo.png")

    tabela_apontamento = []
    for unidade in folha["Unidade Simples"].unique():
        atendidas = len(atendidas_2025[atendidas_2025["Unidade Simples"] == unidade])
        parcialmente = len(folha[(folha["Unidade Simples"] == unidade) & (folha["Providência"] == "Recomendação implementada parcialmente")])
        nao_atendidas = len(folha[(folha["Unidade Simples"] == unidade) & (folha["Providência"] == "Não houve providência")])
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

    with PdfPages(f"{hu_nome}.pdf") as pdf:
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')
        fig.figimage(logo, xo=295, yo=900, alpha=1, zorder=1)

        t_intro = justificar_texto(
            f"Trata-se de avaliação do Plano de Providências Permanente PPP do {hu_nome}, conforme previsto no Plano Anual de Auditoria Interna (PAINT/2025)...",
            largura=78
        )

        ax.text(0.5, 0.97, f"Relatório de Monitoramento\nPPP – {hu_nome}\n", ha='center', va='top', fontsize=14, fontweight='bold')
        ax.text(0.5, 0.915, f"Relatório gerado em: {agora_brasil.strftime('%d/%m/%Y %H:%M')}", ha='center', va='top', fontsize=8, fontweight='bold')
        ax.text(0.02, 0.86, "I - INTRODUÇÃO:", ha='left', va='top', wrap=True, fontsize=12, fontweight='bold')
        fig.text(0.1, 0.73, t_intro, fontsize=10, va='top', ha='left', family='monospace')

        ax.text(0.02, 0.54, "II - APONTAMENTOS MONITORADOS NO PERÍODO:", ha='left', va='top', fontsize=12, fontweight='bold')
        table = ax.table(
            cellText=df.values,
            colLabels=df.columns,
            colLoc='center',
            loc='center',
            bbox=[0.02, 0.13, 0.99, 0.36]
        )
        table.auto_set_font_size(False)
        table.set_fontsize(7.5)

        for (row, col), cell in table.get_celld().items():
            cell.get_text().set_ha('center')
            cell.get_text().set_va('center')
            if row == 0 or row == len(df):
                cell.set_text_props(weight='bold')
                cell.set_facecolor('#f0f0f0' if row == 0 else '#e0e0e0')

        ax.text(0.02, 0.10,
                "*Foram consideradas como Tarefas Atendidas aquelas realizadas a partir de 01/01/2025...",
                ha='left', va='top', wrap=True, fontsize=9, style='italic')

        pdf.savefig(fig)
        plt.close()

        # Gráfico
        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')
        fig.text(0.1, 0.95, "III - REPRESENTAÇÃO GRÁFICA DOS APONTAMENTOS:", ha='left', va='top', fontsize=12, fontweight='bold')

        x = np.arange(len(df['Unidades']))
        graf_ax = fig.add_axes([0.1, 0.45, 0.8, 0.45])
        graf_ax.bar(x - 0.22, df['*Atendidas'], width=0.2, label='*Atendidas', color='green')
        graf_ax.bar(x, df['Parc. Atend.'], width=0.2, label='Parcialmente Atendidas', color='orange')
        graf_ax.bar(x + 0.22, df['Não Atend.'], width=0.2, label='Não Atendidas', color='red')

        graf_ax.set_ylabel('Quantidade')
        graf_ax.set_xticks(x)
        graf_ax.set_xticklabels(df['Unidades'], rotation=45, ha='right')
        graf_ax.legend()

        for container in graf_ax.containers:
            graf_ax.bar_label(container, fmt="%.0f", size=10, label_type="edge", padding=7)

        texto_final = justificar_texto(
            "Informamos que todos os apontamentos podem ser consultados no Sistema do e-CGU. Além disso...",
            largura=78
        )
        fig.text(0.1, 0.33, texto_final, fontsize=10, va='top', ha='left', family='monospace')

        pdf.savefig(fig)
        plt.close()
