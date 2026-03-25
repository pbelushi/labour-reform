import os
import pandas as pd
import matplotlib.pyplot as plt

# 1. Configuração de Diretórios (Automático)
# Descobre a pasta raiz do projeto (labour-reform)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_FIGURES = os.path.join(BASE_DIR, 'output', 'figures')

os.makedirs(OUTPUT_FIGURES, exist_ok=True)

# Caminho exato do seu CSV (Ajuste o nome do arquivo se você tiver renomeado!)
caminho_csv = os.path.join(DATA_DIR, 'RAIS_vinculos_2016_2024.csv')

print(f"Lendo dados de: {caminho_csv}")

try:
    # 2. Carregar os dados
    df = pd.read_csv(caminho_csv)
    
    # Preencher NaN com 0 para o ano de 2016 (antes da reforma)
    df.fillna(0, inplace=True)

    # 3. Criar as métricas proporcionais
    df['Perc_Intermitente'] = (df['Intermitente'] / df['Total_Vinculos']) * 100
    df['Perc_Parcial'] = (df['Parcial'] / df['Total_Vinculos']) * 100

    # 4. Calcular a Taxa de Crescimento Anual (CAGR) de 2018 a 2024
    vinculos_2018 = df.loc[df['ano'] == 2018, 'Total_Vinculos'].values[0]
    vinculos_2024 = df.loc[df['ano'] == 2024, 'Total_Vinculos'].values[0]
    cagr_total = ((vinculos_2024 / vinculos_2018) ** (1/6) - 1) * 100

    inter_2018 = df.loc[df['ano'] == 2018, 'Intermitente'].values[0]
    inter_2024 = df.loc[df['ano'] == 2024, 'Intermitente'].values[0]
    cagr_inter = ((inter_2024 / inter_2018) ** (1/6) - 1) * 100

    print("\n" + "="*50)
    print("ANÁLISE DE CRESCIMENTO (2018 - 2024)")
    print("="*50)
    print(f"Taxa de crescimento anual do Mercado Total: {cagr_total:.1f}%")
    print(f"Taxa de crescimento anual do Intermitente:  {cagr_inter:.1f}%")
    print("="*50 + "\n")

    # 5. Gerar Gráficos
    plt.style.use('ggplot')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Gráfico 1: Crescimento Absoluto
    ax1.plot(df['ano'], df['Intermitente'], marker='o', label='Intermitente', color='purple', linewidth=2)
    ax1.plot(df['ano'], df['Parcial'], marker='s', label='Parcial', color='green', linewidth=2)
    ax1.axvline(x=2017.8, color='red', linestyle='--', label='Reforma (Nov/17)')
    ax1.set_title('Evolução dos Novos Contratos (Absoluto)')
    ax1.set_ylabel('Quantidade de Vínculos')
    ax1.legend()

    # Gráfico 2: Crescimento Proporcional (Porcentagem)
    ax2.plot(df['ano'], df['Perc_Intermitente'], marker='o', color='purple', linewidth=2, label='% Intermitente')
    ax2.plot(df['ano'], df['Perc_Parcial'], marker='s', color='green', linewidth=2, label='% Parcial')
    ax2.axvline(x=2017.8, color='red', linestyle='--', label='Reforma')
    ax2.set_title('Participação no Mercado de Trabalho (%)')
    ax2.set_ylabel('% do Total de Vínculos')
    ax2.legend()

    plt.tight_layout()
    
    # Salvar na pasta output/figures
    caminho_grafico = os.path.join(OUTPUT_FIGURES, 'graficos_reforma_tendencia.png')
    plt.savefig(caminho_grafico)
    print(f"Gráfico salvo com sucesso em: {caminho_grafico}")
    
    # Opcional: mostrar o gráfico na tela (funciona no VS Code ou Colab)
    plt.show()

except FileNotFoundError:
    print(f"\n[!] ERRO: O arquivo CSV não foi encontrado no caminho:\n{caminho_csv}")
    print("Verifique se o nome do arquivo está correto e se ele está dentro da pasta 'data/'.")