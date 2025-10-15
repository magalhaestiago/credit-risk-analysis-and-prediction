# Credit Risk Analysis and Prediction

### Parte A - Carregando e entendendo os dados

[X] - 1. Carregue os dados usando pandas.read_csv().

[X] - 2. Quantas entradas (linhas) e variáveis (colunas) o dataset possui?

<p><b>Resposta:</b> 150000 entradas e 12 variáveis.</p>

[X] - 3. Verifique os tipos de dados de cada coluna. Há colunas que precisam ser
transformadas?
<p><b>Resposta:</b> Aparentemente não há colunas que precisam ser transformadas. Os valores estão em inteiros e floats.</p>

[X] - 4. Existem valores ausentes? Como tratá-los?
<p><b>Resposta:</b> Sim, nas colunas MonthlyIncome (29731) e NumberOfDependents (3924). No caso de MonthlyIncome, uma possível abordagem seria substituir os valores ausentes pela mediana dos valores existentes. Para NumberOfDependents, a melhor abordagem seria substituir os valores pela moda, que é melhor para variaveis discretas.</p>

[X] - 5. Há colunas que parecem irrelevantes ou redundantes?
<p><b>Resposta:</b> Inicialmente achei que a coluna "age" poderia ser irrelevante, porém ao plotar um gráfico com as variaveis de idade e inadimplência, percebe-se que há uma tendência de diminuição da inadimplência conforme a idade aumenta. Porém, essa relação pode está sendo enviesada pela quantidade de dados que foram registrados, tendo em vista que a menor quantidade de registros é entre 20 e 29 anos e corresponde a maior taxa de inadimplência. De qualquer forma, a coluna "age" pode ser considerada relevante para a análise. Além da variável NumberOfDependents que também parece não ter uma relação tão forte com a inadimplência, além de contêr bastante dados faltantes, porém ao plotar o gráfico, conseguimos visualizar melhor essa relação, e o gráfico traduz que conforme o número de dependentes aumenta, a taxa de inadimplência também tende a aumentar.</p>
<p> Em relação a redundância, essas 3 colunas aparentam ser redundantes: NumberOfTime30-59DaysPastDueNotWorse, NumberOfTime60-89DaysPastDueNotWorse, NumberOfTimes90DaysLate</p>


### Parte B - Carregando e entendendo os dados

#### B.1. Há correlação entre as variáveis?

[ ] - 1. Calcule e visualize a matriz de correlação entre as variáveis numéricas.  
[ ] - 2. Interprete os principais pares com correlação alta (positiva ou negativa).  
[ ] - 3. Use também uma matriz de dispersão (pairplot) para observar relações visuais
entre as variáveis mais importantes.

B.2 Delinquência e variáveis relacionadas
1. Qual a proporção de indivíduos com SeriousDlqin2yrs = 1?
2. Existe relação entre idade e inadimplência?
3. Existe relação entre número de linhas de crédito abertas ou atrasos e
inadimplência?
B.3 Criação de variáveis derivadas
1. IncomePerDependent = MonthlyIncome / (NumberOfDependents + 1)
2. DebtPerLoan = DebtRatio / (NumberOfOpenCreditLinesAndLoans + 1)
3. Crie outras variáveis que você considerar úteis para os modelos.