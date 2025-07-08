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
                    linha[i % (len(linha) - 1)] += ' '
                linhas.append(''.join(linha))
            linha = []
            comprimento_linha = 0

        linha.append(palavra)
        comprimento_linha += len(palavra)

    linhas.append(' '.join(linha).ljust(largura))
    return '\n'.join(linhas)
