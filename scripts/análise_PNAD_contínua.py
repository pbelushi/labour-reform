import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

# 1. Carga dos Dados
caminho_arquivo = r'C:\Users\psilva4\Downloads\PNAD contínua.csv'

# Lendo o CSV ignorando as primeiras linhas de metadados
df = pd.read_csv(caminho_arquivo, sep=';', skiprows=4, encoding='utf-8', encoding_errors='ignore')

# 2. Limpeza de Rodapé e Colunas
# Removemos linhas totalmente vazias ou que não são de dados
df = df.dropna(subset=[df.columns[0]])

# Renomeação por POSIÇÃO para evitar erros de nomes de colunas
df.columns = [
    'Trimestre', 'Local', 'Total', 'Privado_Total', 
    'Privado_Com_Carteira', 'Privado_Sem_Carteira', 'Domestico_Total',
    'Domestico_Com_Carteira', 'Domestico_Sem_Carteira', 'Publico_Total',
    'Publico_CLT', 'Publico_Sem_Carteira', 'Militar_Estatutario',
    'Empregador', 'Conta_Propria', 'Familiar'
][:len(df.columns)]

# 3. Função de Tempo Robusta (Corrige o erro 'do')
def converter_tempo_seguro(texto):
    try:
        texto_str = str(texto)
        partes = texto_str.split()
        
        # Procura por um número de 4 dígitos na string (o ano)
        ano = None
        for p in partes:
            if p.isdigit() and len(p) == 4:
                ano = int(p)
                break
        
        # O trimestre é sempre o 1º caractere (ex: '1º')
        tri = int(texto_str[0])
        
        if ano and tri:
            return ano + (tri - 1) / 4
    except:
        return None

# Aplicar a conversão e filtrar apenas linhas válidas
df['Tempo'] = df['Trimestre'].apply(converter_tempo_seguro)
df = df.dropna(subset=['Tempo'])

# 4. Tratamento dos Números (Vírgula para Ponto)
def limpar_numero(valor):
    try:
        return float(str(valor).replace(',', '.').strip())
    except:
        return 0.0

for col in ['Privado_Com_Carteira', 'Privado_Sem_Carteira']:
    df[col] = df[col].apply(limpar_numero)

# 5. Configuração do Modelo DiD (Formal vs Informal)
df['Pos_Reforma'] = (df['Tempo'] >= 2018.0).astype(int)

df_did = df.melt(id_vars=['Tempo', 'Pos_Reforma'], 
                 value_vars=['Privado_Com_Carteira', 'Privado_Sem_Carteira'],
                 var_name='Tipo_Emprego', value_name='Percentual')

df_did['Tratamento'] = (df_did['Tipo_Emprego'] == 'Privado_Com_Carteira').astype(int)

# --- EXECUÇÃO DA REGRESSÃO ---
modelo = smf.ols(formula="Percentual ~ Tratamento * Pos_Reforma", data=df_did).fit()

print("\n" + "="*60)
print("ANÁLISE: FORMALIZAÇÃO VS INFORMALIDADE (SETOR PRIVADO)")
print("="*60)
print(modelo.summary())

# --- EXPORTAÇÃO PARA LATEX ---
print("\nA gerar arquivo LaTeX...")

# Aqui o nome deve ser 'modelo', conforme definido acima
conteudo_latex = modelo.summary().as_latex()

with open(r'C:\Users\psilva4\Downloads\tabela_formal_informal.tex', 'w', encoding='utf-8') as f:
    f.write(conteudo_latex)

print("Arquivo 'tabela_formal_informal.tex' gravado com sucesso em Downloads!")

# --- GRÁFICO ---
# (O gráfico deve vir por último para não travar a gravação do arquivo)
plt.figure(figsize=(12, 6))
for nome, dados in df_did.groupby('Tipo_Emprego'):
    cor = 'blue' if 'Com' in nome else 'orange'
    plt.plot(dados['Tempo'], dados['Percentual'], label=nome, marker='o', color=cor)

plt.axvline(x=2017.85, color='red', linestyle='--', label='Reforma (Nov/17)')
plt.title('Dinâmica do Mercado Privado: Com Carteira vs Sem Carteira')
plt.ylabel('% do Total de Ocupados')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
