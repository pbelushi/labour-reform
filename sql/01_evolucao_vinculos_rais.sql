-- Consulta 1: Evolução Histórica dos Vínculos (2016 a 2024)
-- Objetivo: Rastrear o crescimento absoluto dos novos modelos de contrato após a Reforma Trabalhista.
-- Fonte: Base dos Dados (br_me_rais.microdados_vinculos) no Google BigQuery

SELECT 
  ano,
  COUNT(*) AS Total_Vinculos,
  SUM(CAST(indicador_trabalho_intermitente AS INT64)) AS Intermitente,
  SUM(CAST(indicador_trabalho_parcial AS INT64)) AS Parcial
FROM 
  `basedosdados.br_me_rais.microdados_vinculos`
WHERE 
  ano BETWEEN 2016 AND 2024
GROUP BY 
  ano
ORDER BY 
  ano;