# labour-reform
Data about behavior of jobs market in Brazil after and before 2017's labour reform 

Project Title: The Impact of Labor Reform on Formal Employment: A DiD Analysis Using Data from the Continuous National Household Sample Survey (PNAD Contínua)

Objective: This project aims to measure the impact of Brazil’s 2017 labor reform on job creation, independent of cyclical economic effects

# Methodology
The analysis uses the Differences-in-Differences (DiD) method to estimate the impact on formal employment levels in the Brazilian labor market, using data from the PNAD Contínua (IBGE).
1. The Differences-in-Differences (DiD) Model
The objective of the DiD model is to identify the variation in the treatment group (Employees with a Formal Contract) that occurs after the event of interest (Labor Reform), subtracting the variation observed in the control group (Employees without a Formal Contract) during the same period.
This technique allows us to control for common time trends and focus on the specific “shock” that occurred in the treated group.
2. Econometric Specification
The estimation is performed using Ordinary Least Squares (OLS), following the fundamental equation:
$$Y_{it} = \beta_0 + \beta_1 \cdot \text{Treatment}_i + \beta_2 \cdot \text{Post\_Reform}_t + \beta_3 \cdot (\text{Treatment}_i \times \text{Post\_Reform}_t) + \gamma \cdot \text{Controls}_{it} + \epsilon_{it}$$
Where:
$Y_{it}$: Percentage of the employed population in category $i$ at time $t$.
$\text{Treatment}_i$: Dummy variable that takes the value 1 for the group of interest (Formal) and 0 for the control group (Informal).
$\text{Post\_Reform}_t$: Temporal dummy variable (0 for periods before 2018, 1 for periods after).
$\beta_3$ (Interaction Coefficient): This is the DiD estimator. It indicates the actual effect of the legal change on formalization, isolating other macroeconomic factors.
$\text{Controls}$ (GDP): In one of the models, we included quarterly GDP as a control variable to ensure that the observed variations are not merely a reflection of the economic cycle (growth or recession).
3. Tools Used
Language: Python 3.x
Libraries:
pandasfor time series manipulation.
statsmodelsfor performing linear regressions and statistical tests.
matplotlibfor visualizing trends and visually validating the assumption of parallel trends.

# How to Run:
Install dependencies: pip install -r requirements.txt
Run the scripts in the /scriptsfolder.

## Citation
If you use this codebase or the processed data in your research, please cite it as:
Silva, P. (2026). Labour Reform Impact Analysis: A DiD Approach using PNAD Contínua Data. GitHub repository: https://github.com/pbelushi/labour-reform

BibTex:
@software{Silva_Labour_Reform_2026,
  author = {Silva, P.},
  title = {{Labour Reform Impact Analysis: A DiD Approach using PNAD Contínua Data}},
  url = {https://github.com/pbelushi/labour-reform},
  version = {1.0.0},
  year = {2026}
}
