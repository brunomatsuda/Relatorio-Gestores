from modules.load_data import get_folha
from modules.preprocess import processar_dados
from modules.report_generator import gerar_relatorio

from req import hu_lists_to_process

def main():
    folha = get_folha()
    for hu in hu_lists_to_process:
        df_resultado = processar_dados(hu, folha)
        gerar_relatorio(hu, df_resultado)

if __name__ == "__main__":
    main()
