from req import hu_lists_to_process, folha
import pandas as pd


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
                    if len(linha) > 1:
                        linha[i % (len(linha) - 1)] += ' '
                    else:
                         linha[0] += ' '
                linhas.append(''.join(linha))
            linha = []
            comprimento_linha = 0

        linha.append(palavra)
        comprimento_linha += len(palavra)

    linhas.append(' '.join(linha).ljust(largura))
    return '\n'.join(linhas)


def filtro(hu):
    all_units = hu

    #Tratamento da Providências Para todos os HU's
    folha["Providência"] = folha["Providência"].str.replace("Recomendação implementada ", "Recomendação implementada")
    folha["Providência"] = folha["Providência"].str.replace("Recomendação implementadaparcialmente", "Recomendação implementada parcialmente")

    #Tratamento UFPI (Caso Isolado*)
      ##GAD
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("XX/YY/ZZ/HH/JJ/HU/TTT", "XX/YY/ZZ/HH/JJ/HU/TTT")
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("XX/YY/ZZ/HH/JJ/HU/TTT", "XX/YY/ZZ/HH/JJ/HU/TTT")
      ##GAS
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("XX/YY/ZZ/HH/JJ/HU/TTT", "XX/YY/ZZ/HH/JJ/HU/TTT")
      ##GEP
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("XX/YY/ZZ/HH/JJ/HU/TTT", "XX/YY/ZZ/HH/JJ/HU/TTT")
      ##SUPRIN
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("XX/YY/ZZ/HH/JJ/HU/TTT", "XX/YY/ZZ/HH/JJ/HU/TTT")
    folha["Unidade Auditada"] = folha["Unidade Auditada"].str.replace("XX/YY/ZZ/HH/JJ/HU/TTT", "XX/YY/ZZ/HH/JJ/HU/TTT")

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

