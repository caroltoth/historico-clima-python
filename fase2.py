import csv
import matplotlib.pyplot as plt
import calendar

def carregar_dados(nome_arquivo):

#função para carregar os dados do arquivo CSV
    
    dados = []
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo, delimiter=',')
            
            for linha in leitor:
                try:
                    linha['precip'] = float(linha['precip'])
                    linha['maxima'] = float(linha['maxima'])
                    linha['minima'] = float(linha['minima'])
                    linha['um_relativa'] = float(linha['um_relativa'])
                    linha['vel_vento'] = float(linha['vel_vento'])
                    dados.append(linha)
                except (ValueError, TypeError):
                    continue
                    
        print(f"Sucesso: {len(dados)} registros foram carregados.")
        return dados
        
    except FileNotFoundError:
        print(f"ERRO CRÍTICO: O arquivo '{nome_arquivo}' não foi encontrado.")
        print("Por favor, certifique-se de que o programa e o arquivo CSV estão na mesma pasta.")
        return None

def visualizar_intervalo_dados(dados):
    
    #permite ao usuário visualizar dados de um período específico

    print("\n--- [a] Visualização de Dados por Período ---")
    
    while True:
        try:
            ano_inicio = int(input("Digite o ano inicial (1961-2016): "))
            if 1961 <= ano_inicio <= 2016:
                break
            else:
                print("--> Erro: Ano inválido. Por favor, insira um ano entre 1961 e 2016.")
        except ValueError:
            print("--> Erro: Entrada inválida. Por favor, digite um número.")

    while True:
        try:
            mes_inicio = int(input("Digite o mês inicial (1-12): "))
            if 1 <= mes_inicio <= 12:
                break
            else:
                print("--> Erro: Mês inválido. Por favor, insira um mês entre 1 e 12.")
        except ValueError:
            print("--> Erro: Entrada inválida. Por favor, digite um número.")

    while True:
        try:
            ano_fim = int(input("Digite o ano final (1961-2016): "))
            if 1961 <= ano_fim <= 2016:
                break
            else:
                print("--> Erro: Ano inválido. Por favor, insira um ano entre 1961 e 2016.")
        except ValueError:
            print("--> Erro: Entrada inválida. Por favor, digite um número.")

    while True:
        try:
            mes_fim = int(input("Digite o mês final (1-12): "))
            if 1 <= mes_fim <= 12:
                break
            else:
                print("--> Erro: Mês inválido. Por favor, insira um mês entre 1 e 12.")
        except ValueError:
            print("--> Erro: Entrada inválida. Por favor, digite um número.")

    if ano_inicio > ano_fim or (ano_inicio == ano_fim and mes_inicio > mes_fim):
        print("\n--> Erro de Período: A data de início não pode ser posterior à data de fim. Tente novamente.")
        return

    print("\nQual conjunto de dados você quer ver?")
    print("  1) Todos os dados")
    print("  2) Apenas Precipitação")
    print("  3) Apenas Temperaturas")
    print("  4) Apenas Umidade e Vento")
    escolha = input("Digite sua opção (1-4): ")

    print("\n--- DADOS PARA O PERÍODO SELECIONADO ---")
    if escolha == '1':
        print(f"{'Data':<12} | {'Precip (mm)':<12} | {'Temp Max (°C)':<14} | {'Temp Min (°C)':<14}")
    elif escolha == '2':
        print(f"{'Data':<12} | {'Precip (mm)':<12}")
    elif escolha == '3':
        print(f"{'Data':<12} | {'Temp Max (°C)':<14} | {'Temp Min (°C)':<14}")
    elif escolha == '4':
        print(f"{'Data':<12} | {'Umidade (%)':<12} | {'Vento (m/s)':<12}")
    else:
        print("Opção de visualização inválida.")
        return

    registros_encontrados = 0
    for registro in dados:
        _, mes_reg_str, ano_reg_str = registro['data'].split('/')
        ano_reg = int(ano_reg_str)
        mes_reg = int(mes_reg_str)

        if (ano_reg > ano_inicio or (ano_reg == ano_inicio and mes_reg >= mes_inicio)) and \
           (ano_reg < ano_fim or (ano_reg == ano_fim and mes_reg <= mes_fim)):
            
            registros_encontrados += 1
            if escolha == '1':
                print(f"{registro['data']:<12} | {registro['precip']:<12.1f} | {registro['maxima']:<14.1f} | {registro['minima']:<14.1f}")
            elif escolha == '2':
                print(f"{registro['data']:<12} | {registro['precip']:<12.1f}")
            elif escolha == '3':
                print(f"{registro['data']:<12} | {registro['maxima']:<14.1f} | {registro['minima']:<14.1f}")
            elif escolha == '4':
                 print(f"{registro['data']:<12} | {registro['um_relativa']:<12.1f} | {registro['vel_vento']:<12.1f}")
    
    if registros_encontrados == 0:
        print("\nNenhum registro encontrado para o período informado.")


def mes_mais_chuvoso(dados):
    
    #Encontra o mês/ano com a maior precipitação acumulada
   
    print("\n--- [b] Calculando Mês Mais Chuvoso ---")
    precipitacao_por_mes = {} 
    
    for registro in dados:
        _, mes, ano = registro['data'].split('/')
        chave_mes_ano = f"{ano}-{mes.zfill(2)}"
        
        if chave_mes_ano in precipitacao_por_mes:
            precipitacao_por_mes[chave_mes_ano] += registro['precip']
        else:
            precipitacao_por_mes[chave_mes_ano] = registro['precip']

    if not precipitacao_por_mes:
        print("Não foi possível calcular, sem dados de precipitação.")
        return

    mes_campeao = max(precipitacao_por_mes, key=precipitacao_por_mes.get)
    volume_maximo = precipitacao_por_mes[mes_campeao]
            
    print(f"Resultado: O mês/ano com maior volume de chuva foi {mes_campeao}.")
    print(f"Volume total: {volume_maximo:.2f} mm.")

def analisar_temperatura_minima(dados):
    
    #Calcula as médias de temperatura mínima, exibe os dados e o gráfico

    try:
        print("\n--- [c, d, e] Análise da Temperatura Mínima (2006-2016) ---")
        mes_desejado = int(input("Digite o mês para análise (1-12): "))
        if not (1 <= mes_desejado <= 12):
            print("Erro: Mês inválido.")
            return
            
        nome_mes = calendar.month_name[mes_desejado]
        
        medias_por_ano = {}
        for ano_analise in range(2006, 2017):
            temperaturas_do_mes = []
            for registro in dados:
                _, mes_reg_str, ano_reg_str = registro['data'].split('/')
                ano_reg = int(ano_reg_str)
                mes_reg = int(mes_reg_str)

                if ano_reg == ano_analise and mes_reg == mes_desejado:
                    temperaturas_do_mes.append(registro['minima'])
            
            if temperaturas_do_mes:
                media = sum(temperaturas_do_mes) / len(temperaturas_do_mes)
                chave = f"{nome_mes}{ano_analise}"
                medias_por_ano[chave] = media

        print(f"\n--- (c) Média da Temperatura Mínima para {nome_mes} (2006-2016) ---")
        if not medias_por_ano:
            print("Não há dados de temperatura mínima para este mês no período de 2006-2016.")
            return

        for chave, media in medias_por_ano.items():
            print(f"  {chave}: {media:.2f}°C")

        media_geral = sum(medias_por_ano.values()) / len(medias_por_ano)
        print(f"\n--- (e) Média Geral do Período ---")
        print(f"  A média geral para {nome_mes} foi de: {media_geral:.2f}°C")

        print("\n--- (d) Gerando Gráfico de Barras ---")
        gerar_grafico(medias_por_ano, nome_mes)

    except ValueError:
        print("Erro: Entrada inválida.")

def gerar_grafico(medias, nome_mes):
    
    #auxiliar para criar e exibir o gráfico de barras

    chaves = list(medias.keys())
    valores = list(medias.values())
    
    plt.figure(figsize=(12, 6))
    plt.bar(chaves, valores, color='royalblue')
    
    plt.title(f'Temperatura Mínima Média em {nome_mes} (2006-2016)')
    plt.ylabel('Temperatura Média (°C)')
    plt.xlabel('Mês/Ano')
    plt.xticks(rotation=45, ha="right") 
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def main():

    #função principal que controla a execução do programa e o menu
   
    nome_arquivo_csv = 'Anexo_Arquivo_Dados_Projeto_Logica_e_programacao_de_computadores.csv'
    
    dados_climaticos = carregar_dados(nome_arquivo_csv)
    
    if dados_climaticos is None:
        return

    while True:
        print("\n" + "="*20 + " MENU PRINCIPAL " + "="*20)
        print("Análise de Dados Climáticos de Porto Alegre (1961-2016)")
        print("  a) Visualizar dados por período")
        print("  b) Encontrar o mês mais chuvoso")
        print("  c) Analisar temperaturas mínimas (2006-2016)")
        print("  s) Sair do programa")
        print("="*56)
        
        opcao = input("Escolha uma opção: ").lower()

        if opcao == 'a':
            visualizar_intervalo_dados(dados_climaticos)
        elif opcao == 'b':
            mes_mais_chuvoso(dados_climaticos)
        elif opcao == 'c':
            analisar_temperatura_minima(dados_climaticos)
        elif opcao == 's':
            print("Programa encerrado.")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == "__main__":
    main()