-- Consulta 2: Perfil de Renda e Idade por Tipo de Contrato (2024)
-- Objetivo: Medir a disparidade salarial e o perfil etário entre o emprego tradicional e os flexíveis.
-- Fonte: Base dos Dados (br_me_rais.microdados_vinculos) no Google BigQuery

SELECT 
  CASE 
    WHEN CAST(indicador_trabalho_intermitente AS STRING) = '1' THEN '1. Intermitente'
    WHEN CAST(indicador_trabalho_parcial AS STRING) = '1' THEN '2. Parcial'
    ELSE '3. Tradicional'
  END AS Tipo_Contrato,
  COUNT(*) AS Total_Vinculos,
  ROUND(AVG(CAST(valor_remuneracao_media AS FLOAT64)), 2) AS Renda_Media_Mensal,
  ROUND(AVG(CAST(idade AS INT64)), 1) AS Idade_Media
FROM 
  `basedosdados.br_me_rais.microdados_vinculos`
WHERE 
  ano = 2024 
GROUP BY 
  Tipo_Contrato
ORDER BY 
  Tipo_Contrato;