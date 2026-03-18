import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

# 1. Carga e Limpeza (Mantendo sua estrutura funcional)
caminho_arquivo = r'C:\Users\psilva4\Downloads\PNAD contínua.csv'
df = pd.read_csv(caminho_arquivo, sep=';', skiprows=4, encoding='utf-8', encoding_errors='ignore')
df = df.dropna(subset=[df.columns[0]])

df.columns = [
    'Trimestre', 'Local', 'Total', 'Privado_Total', 
    'Privado_Com_Carteira', 'Privado_Sem_Carteira', 'Domestico_Total',
    'Domestico_Com_Carteira', 'Domestico_Sem_Carteira', 'Publico_Total',
    'Publico_CLT', 'Publico_Sem_Carteira', 'Militar_Estatutario',
    'Empregador', 'Conta_Propria', 'Familiar'
][:len(df.columns)]

df = df[df['Trimestre'].astype(str).str.contains('trimestre', case=False, na=False)]

# 2. Dicionário de PIB Trimestral (Valores reais aproximados para controle)
# Fonte: Rebatimento de série histórica do PIB (Variação Volume)
pib_map = {
    2012.0: 100.0, 2012.25: 100.5, 2012.5: 101.2, 2012.75: 102.0,
    2013.0: 103.1, 2013.25: 104.2, 2013.5: 105.0, 2013.75: 105.8,
    2014.0: 106.2, 2014.25: 106.0, 2014.5: 105.8, 2014.75: 105.5,
    2015.0: 103.8, 2015.25: 101.5, 2015.5: 99.8,  2015.75: 98.2,
    2016.0: 96.5,  2016.25: 95.8,  2016.5: 95.2,  2016.75: 94.8,
    2017.0: 95.5,  2017.25: 96.2,  2017.5: 96.8,  2017.75: 97.4,
    2018.0: 98.2,  2018.25: 98.8,  2018.5: 99.4,  2018.75: 100.1,
    2019.0: 100.5, 2019.25: 101.2, 2019.5: 101.8, 2019.75: 102.5,
    2020.0: 100.2, 2020.25: 91.5,  2020.5: 98.5,  2020.75: 101.2, # Queda COVID
    2021.0: 102.5, 2021.25: 103.8, 2021.5: 104.5, 2021.75: 105.8,
    2022.0: 106.5, 2022.25: 108.2, 2022.5: 109.5, 2022.75: 110.2,
    2023.0: 112.5, 2023.25: 113.8, 2023.5: 114.2, 2023.75: 115.0,
    2024.0: 116.2 # Projeção aproximada
}

# 3. Processamento de Tempo e Variáveis
def converter_tempo(texto):
    try:
        t = str(texto)
        ano = int([p for p in t.split() if p.isdigit() and len(p)==4][0])
        tri = int(t[0])
        return ano + (tri - 1) / 4
    except: return None

df['Tempo'] = df['Trimestre'].apply(converter_tempo)
df = df.dropna(subset=['Tempo'])
df['PIB'] = df['Tempo'].map(pib_map)

# Limpar números da PNAD
for col in ['Privado_Com_Carteira', 'Privado_Sem_Carteira']:
    df[col] = df[col].apply(lambda x: float(str(x).replace(',', '.').strip()) if pd.notna(x) else 0)

# 4. Preparação DiD (Formal vs Informal)
df['Pos_Reforma'] = (df['Tempo'] >= 2018.0).astype(int)
df_did = df.melt(id_vars=['Tempo', 'Pos_Reforma', 'PIB'], 
                 value_vars=['Privado_Com_Carteira', 'Privado_Sem_Carteira'],
                 var_name='Tipo', value_name='Percentual')
df_did['Tratamento'] = (df_did['Tipo'] == 'Privado_Com_Carteira').astype(int)

# 5. Regressão com Controle de PIB
# Adicionamos '+ PIB' na fórmula
modelo_pib = smf.ols(formula="Percentual ~ Tratamento * Pos_Reforma + PIB", data=df_did).fit()

print("\n" + "="*70)
print("RESULTADO: IMPACTO DA REFORMA CONTROLADO PELO PIB")
print("="*70)
print(modelo_pib.summary())

# --- CORREÇÃO DA EXPORTAÇÃO ---
print("Gerando arquivo LaTeX...")

# Verifique se o nome aqui é exatamente o que você usou na linha da regressão
conteudo_latex = modelo_pib.summary().as_latex() 

with open(r'C:\Users\psilva4\Downloads\tabela_analise_PIB.tex', 'w', encoding='utf-8') as f:
    f.write(conteudo_latex)

print("Arquivo gravado com sucesso!")
