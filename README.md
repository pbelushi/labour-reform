# labour-reform
Data about behavior of jobs market in Brazil after and before 2017's labour reform (work in progress)

Project Title: The Impact of Labor Reform on Formal Employment and New Contract Models: An Analysis Using PNAD Contínua and RAIS Data

Objective: This project aims to measure the impact of Brazil’s 2017 labor reform on job creation, independent of cyclical economic effects, and to evaluate the adoption rate of new contract models (Intermittent Work and Telework) introduced by the legislation.

### How to reproduce the data:
1. Go to [Google Cloud Console > BigQuery](https://console.cloud.google.com/bigquery).
2. Run the queries from the `sql/` folder in the environment.
3. Export the results in CSV format and save them in the `data/` directory of this project.
4. Run the Python scripts (in the `scripts/` folder) to generate the statistical visualizations.

# Methodology
The project is divided into two main analytical fronts, utilizing different methodologies and national databases:

1. The Differences-in-Differences (DiD) Model (PNAD Contínua)
The objective of the DiD model is to identify the variation in the treatment group (Employees with a Formal Contract) that occurs after the event of interest (Labor Reform), subtracting the variation observed in the control group (Employees without a Formal Contract) during the same period.

This technique allows us to control for common time trends and focus on the specific “shock” that occurred in the treated group.

Econometric Specification:The estimation is performed using Ordinary Least Squares (OLS), following the fundamental equation:

$$Y_{it} = \beta_0 + \beta_1 \cdot \text{Treatment}_i + \beta_2 \cdot \text{Post\_Reform}_t + \beta_3 \cdot (\text{Treatment}_i \times \text{Post\_Reform}_t) + \gamma \cdot \text{Controls}_{it} + \epsilon_{it}$$

Where:
$Y_{it}$: Percentage of the employed population in category $i$ at time $t$.
$\text{Treatment}_i$: Dummy variable that takes the value 1 for the group of interest (Formal) and 0 for the control group (Informal).
$\text{Post\_Reform}_t$: Temporal dummy variable (0 for periods before 2018, 1 for periods after).
$\beta_3$ (Interaction Coefficient): This is the DiD estimator. It indicates the actual effect of the legal change on formalization, isolating other macroeconomic factors.
$\text{Controls}$ (GDP): In one of the models, we included quarterly GDP as a control variable to ensure that the observed variations are not merely a reflection of the economic cycle (growth or recession).

2. Descriptive Analysis of New Contract Models (RAIS)
To enable historical analysis of the RAIS (Annual Social Information Report) without the need to process tens of gigabytes of raw microdata on local or virtual servers, this project adopted cloud-based extraction via **Google BigQuery**, using the architecture of the [Database](https://basedosdados.org/).

The SQL queries used to generate the datasets (CSVs) for this study are documented in the `sql/` folder:

* **`01_evolucao_vinculos_rais.sql`**: Generates the historical series (2016–2024) to compare the adoption rate of intermittent and part-time contracts relative to traditional employment.
* **`02_perfil_demografico_renda.sql`**: Provides a cross-sectional snapshot of the year 2024 to calculate wage disparities and the average age of workers under each contract type.

# How to Run:
Install dependencies: pip install -r requirements.txt (Ensure py7zr is added to your requirements).

Run the scripts in the /scripts folder.

## Citation
If you use this codebase or the processed data in your research, please cite it as:
Silva, P. (2026). Labour Reform Impact Analysis: A DiD Approach using PNAD Contínua and RAIS Data. GitHub repository: https://github.com/pbelushi/labour-reform

BibTex:
@software{Silva_Labour_Reform_2026,
  author = {Silva, P.},
  title = {{Labour Reform Impact Analysis: A DiD Approach using PNAD Contínua and RAIS Data}},
  url = {https://github.com/pbelushi/labour-reform},
  version = {1.1.0},
  year = {2026}
}
