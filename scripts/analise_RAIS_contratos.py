import os
import sys
import pandas as pd
import py7zr
from ftplib import FTP
import matplotlib.pyplot as plt

# --- CONFIGURAÇÕES DE DIRETÓRIOS INTELIGENTES ---
# Descobre automaticamente se estamos no Google Colab ou no VS Code local
if 'google.colab' in sys.modules:
    print("🌍 Rodando no Google Colab! Usando caminhos da nuvem...")
    BASE_DIR = '/content'
else:
    print("💻 Rodando localmente! Usando caminhos do repositório...")
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DATA_DIR = os.path.join(BASE_DIR, 'data', 'RAIS')
OUTPUT_TABLES = os.path.join(BASE_DIR, 'output', 'tables')
OUTPUT_FIGURES = os.path.join(BASE_DIR, 'output', 'figures')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_TABLES, exist_ok=True)
os.makedirs(OUTPUT_FIGURES, exist_ok=True)

ANOS = ['2016', '2017', '2018', '2019', '2020', '2021']
UFS = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

# Apaga o .7z logo após extrair para proteger seu Disco Rígido
APAGAR_ZIP_APOS_PROCESSAR = True 

def processar_arquivo_txt(caminho_txt):
    """Lê o ficheiro txt aos pedaços (chunks) e soma os contratos da Reforma Trabalhista."""
    print(f"     -> Lendo e contabilizando dados de {os.path.basename(caminho_txt)}...")
    res_parciais = {'Total_Vinculos': 0, 'Intermitente': 0, 'Teletrabalho': 0, 'Parcial': 0}
    chunksize = 10**6 # 1 milhão de linhas por vez
    
    try:
        for chunk in pd.read_csv(caminho_txt, sep=';', encoding='latin1', chunksize=chunksize, on_bad_lines='skip', low_memory=False):
            res_parciais['Total_Vinculos'] += len(chunk)
            
            if 'Ind Trab Intermitente' in chunk.columns:
                res_parciais['Intermitente'] += pd.to_numeric(chunk['Ind Trab Intermitente'], errors='coerce').fillna(0).sum()
            if 'Ind Teletrabalho' in chunk.columns:
                res_parciais['Teletrabalho'] += pd.to_numeric(chunk['Ind Teletrabalho'], errors='coerce').fillna(0).sum()
            if 'Ind Trab Parcial' in chunk.columns:
                res_parciais['Parcial'] += pd.to_numeric(chunk['Ind Trab Parcial'], errors='coerce').fillna(0).sum()
    except Exception as e:
        print(f"     [!] Erro ao ler ficheiro {caminho_txt}: {e}")
        
    return res_parciais

# --- EXECUÇÃO PRINCIPAL ---
dados_finais = []

for ano in ANOS:
    print(f"\n{'='*60}\nA PROCESSAR O ANO {ano} (BRASIL INTEIRO)\n{'='*60}")
    resultados_ano = {'Ano': ano, 'Total_Vinculos': 0, 'Intermitente': 0, 'Teletrabalho': 0, 'Parcial': 0}
    
    try:
        # 1. PEGAR A LISTA DE ARQUIVOS (Liga e desliga rápido)
        ftp = FTP('ftp.mtps.gov.br', timeout=120)
        ftp.login() 
        ftp.cwd(f'pdet/microdados/RAIS/{ano}/')
        arquivos_ftp = ftp.nlst()
        ftp.quit()
        
        # Filtra apenas arquivos de vínculos
        alvos = []
        for arq in arquivos_ftp:
            arq_upper = arq.upper()
            if not (arq_upper.endswith('.7Z') or arq_upper.endswith('.ZIP')): continue
            if 'ESTAB' in arq_upper: continue
            
            if int(ano) >= 2018:
                if 'VINC_PUB' in arq_upper: alvos.append(arq)
            else:
                for uf in UFS:
                    if arq_upper.startswith(uf) or f'_{uf}' in arq_upper:
                        alvos.append(arq)
                        break
                        
        print(f" -> Encontrados {len(alvos)} ficheiros para descarregar neste ano.")
        
        # 2. LOOP DE ARQUIVOS (Processa 1 a 1, ligando e desligando o FTP)
        for nome_arq in alvos:
            caminho_7z = os.path.join(DATA_DIR, f"{ano}_{nome_arq}")
            precisa_baixar = True
            
            # Liga FTP para checar tamanho e baixar
            ftp = FTP('ftp.mtps.gov.br', timeout=120)
            ftp.login()
            ftp.cwd(f'pdet/microdados/RAIS/{ano}/')
            tamanho_ftp = ftp.size(nome_arq)

            if os.path.exists(caminho_7z):
                tamanho_local = os.path.getsize(caminho_7z)
                if tamanho_local == tamanho_ftp:
                    print(f"\n  -> [Pular Download] O ficheiro {nome_arq} já existe e está completo.")
                    precisa_baixar = False
                else:
                    print(f"\n  -> [Atenção] Ficheiro {nome_arq} incompleto. Apagando para tentar de novo...")
                    os.remove(caminho_7z)
            
            if precisa_baixar:
                print(f"\n  -> A descarregar {nome_arq}...")
                baixados = 0
                
                def mostrar_progresso(bloco):
                    global baixados
                    baixados += len(bloco)
                    if baixados % (1024 * 1024 * 10) < 8192: 
                        print(f"     Descarregado: {baixados / (1024*1024):.1f} MB de {tamanho_ftp / (1024*1024):.1f} MB", end='\r')
                        
                with open(caminho_7z, 'wb') as f:
                    ftp.retrbinary(f'RETR {nome_arq}', lambda b: (f.write(b), mostrar_progresso(b)))
                
                # Checagem de segurança
                if os.path.getsize(caminho_7z) != tamanho_ftp:
                    ftp.quit()
                    raise ValueError(f"A conexão caiu! Download incompleto do ficheiro {nome_arq}.")
                print(f"\n     Download concluído.")

            ftp.quit() # Fechamos a conexão aqui para o servidor não nos derrubar por inatividade

            # 3. EXTRAIR E CONTABILIZAR
            print(f"  -> A extrair {nome_arq}...")
            with py7zr.SevenZipFile(caminho_7z, mode='r') as z:
                z.extractall(path=DATA_DIR)
                nomes_extraidos = z.getnames()
            
            for nome_txt in nomes_extraidos:
                if nome_txt.upper().endswith('.TXT') or nome_txt.upper().endswith('.CSV'):
                    caminho_txt = os.path.join(DATA_DIR, nome_txt)
                    res_parciais = processar_arquivo_txt(caminho_txt)
                    
                    # Acumula resultados no total do ano
                    resultados_ano['Total_Vinculos'] += res_parciais['Total_Vinculos']
                    resultados_ano['Intermitente'] += res_parciais['Intermitente']
                    resultados_ano['Teletrabalho'] += res_parciais['Teletrabalho']
                    resultados_ano['Parcial'] += res_parciais['Parcial']
                    
                    os.remove(caminho_txt) # Apaga o .txt gigante
            
            if APAGAR_ZIP_APOS_PROCESSAR:
                if os.path.exists(caminho_7z):
                    os.remove(caminho_7z)
                print(f"  -> Ficheiro compactado {nome_arq} apagado para libertar espaço.")

    except Exception as e:
        print(f"Erro ao processar o ano {ano}: {e}")
        
    dados_finais.append(resultados_ano)

# --- CONSOLIDAÇÃO FINAL ---
df_resultados = pd.DataFrame(dados_finais)

df_resultados['Perc_Intermitente'] = (df_resultados['Intermitente'] / df_resultados['Total_Vinculos']) * 100
df_resultados['Perc_Teletrabalho'] = (df_resultados['Teletrabalho'] / df_resultados['Total_Vinculos']) * 100

print("\n" + "="*60)
print("RESUMO NACIONAL: NOVOS CONTRATOS (REFORMA TRABALHISTA)")
print("="*60)
print(df_resultados)

caminho_csv = os.path.join(OUTPUT_TABLES, 'tabela_rais_novos_contratos_BRASIL.csv')
df_resultados.to_csv(caminho_csv, index=False, sep=';')
print(f"\nTabela exportada para: {caminho_csv}")

# --- GRÁFICOS ---
plt.figure(figsize=(10, 6))
plt.plot(df_resultados['Ano'], df_resultados['Intermitente'], marker='o', label='Trabalho Intermitente', color='purple')
plt.plot(df_resultados['Ano'], df_resultados['Teletrabalho'], marker='s', label='Teletrabalho', color='green')

plt.axvline(x=1.85, color='red', linestyle='--', label='Reforma (Nov/17)')
plt.title('Evolução dos Novos Modelos de Contrato (RAIS - Brasil Inteiro)')
plt.ylabel('Quantidade Total de Vínculos')
plt.xlabel('Ano')
plt.legend()
plt.grid(True, alpha=0.3)

caminho_grafico = os.path.join(OUTPUT_FIGURES, 'evolucao_novos_contratos_rais_brasil.png')
plt.savefig(caminho_grafico)
print(f"Gráfico guardado em: {caminho_grafico}")