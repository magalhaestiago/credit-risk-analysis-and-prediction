# Credit Risk Analysis and Prediction

### Parte A - Carregando e entendendo os dados

[X] - 1. Carregue os dados usando pandas.read_csv().

[X] - 2. Quantas entradas (linhas) e variáveis (colunas) o dataset possui?

<p><b>Resposta:</b> 150000 entradas e 12 variáveis (ou será que são 11??, uma coluna está aparentemente bugada e se refere apenas ao indice do dado).</p>

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

[X] - 1. Calcule e visualize a matriz de correlação entre as variáveis numéricas.  
[X] - 2. Interprete os principais pares com correlação alta (positiva ou negativa).  
Com certeza! Analisando a matriz de correlação que você gerou, podemos extrair insights muito importantes.

Esta é a interpretação dos principais pares com correlação alta:

Correlações Positivas Fortes (Cores Vermelhas)

Estas são as mais significativas e evidentes no seu gráfico:

1. O Trio de Inadimplência: NumberOfTime...DaysPastDue...

    NumberOfTime30-59DaysPastDueNotWorse e NumberOfTimes90DaysLate têm uma correlação de +0.98.

    NumberOfTime30-59DaysPastDueNotWorse e NumberOfTime60-89DaysPastDueNotWorse têm uma correlação de +0.99.

    NumberOfTimes90DaysLate e NumberOfTime60-89DaysPastDueNotWorse têm uma correlação de +0.99.

    Interpretação: Este é o achado mais importante. Uma correlação tão próxima de 1.00 significa que essas três variáveis são extremamente redundantes. Elas estão medindo essencialmente o mesmo fenômeno: a propensão de um cliente a atrasar pagamentos. Quando um cliente atrasa 90 dias, é quase certo que ele também já atrasou 30 e 60 dias.

    Ação: Isso confirma, de forma visual e numérica, que a nossa decisão anterior de manter apenas a variável mais severa (NumberOfTimes90DaysLate) e descartar as outras duas é uma excelente estratégia para simplificar o modelo e evitar multicolinearidade.

2. Linhas de Crédito e Empréstimos Imobiliários

    NumberOfOpenCreditLinesAndLoans e NumberRealEstateLoansOrLines têm uma correlação de +0.43.

    Interpretação: Há uma correlação positiva moderada. Isso faz todo o sentido, pois empréstimos imobiliários são um tipo de "linha de crédito aberta". Pessoas com mais empréstimos no geral tendem a ter também mais empréstimos imobiliários. Como a correlação não é altíssima (é < 0.7), não é tão problemático quanto o trio de inadimplência, e ambas as colunas podem ser mantidas, pois ainda carregam informações distintas.

3. Preditores de Risco de Crédito (SeriousDlqin2yrs)

    A variável alvo SeriousDlqin2yrs tem suas maiores correlações positivas com:

        NumberOfTime30-59DaysPastDueNotWorse (+0.13)

        NumberOfTimes90DaysLate (+0.12)

        RevolvingUtilizationOfUnsecuredLines (+0.12)

    Interpretação: Embora esses valores não sejam "altos" em termos absolutos, eles indicam que estas são as variáveis com a mais forte relação linear com a ocorrência de inadimplência grave. Um aumento em qualquer uma delas está associado a um aumento na probabilidade de default.

Correlações Negativas (Cores Azuis)

No seu gráfico, não há correlações negativas fortes. A mais notável, ainda que fraca, é:

1. Idade e Número de Dependentes

    age e NumberOfDependents têm uma correlação de -0.21.

    Interpretação: Esta é uma correlação negativa fraca. Ela sugere que, em geral, à medida que a idade (age) aumenta, o número de dependentes (NumberOfDependents) tende a diminuir. Isso é intuitivo, pois com o passar do tempo os filhos crescem e se tornam financeiramente independentes.

Resumo Final

O insight mais poderoso deste gráfico é a confirmação da redundância extrema entre as variáveis de atraso de pagamento, validando a decisão de simplificar o modelo. Adicionalmente, ele aponta para as variáveis de utilização de crédito e histórico de atrasos como os principais indicadores lineares do risco de crédito.  
[X] - 3. Use também uma matriz de dispersão (pairplot) para observar relações visuais
entre as variáveis mais importantes.

B.2 Delinquência e variáveis relacionadas


[X] - 1. Qual a proporção de indivíduos com SeriousDlqin2yrs = 1?
<p><b>Resposta:</b> A proporção de indivíduos com SeriousDlqin2yrs = 1 é de aproximadamente 6.68%, há um desbalanceamento significativo entre as classes, 10026 são inadimplentes e 139974 são não inadimplentes.</p>
[X] - 2. Existe relação entre idade e inadimplência?
<p><b>Resposta:</b> Pelos dados que temos, é difícil afirmar com certeza, porém ao observar o gráfico de histograma, podemos perceber que a taxa de inadimplência tende a diminuir conforme a idade aumenta, porém essa relação pode estar sendo enviesada pela quantidade de dados que foram registrados, tendo em vista que a menor quantidade de registros é entre 20 e 29 anos e corresponde a maior taxa de inadimplência.</p>

[X] - 3. Existe relação entre número de linhas de crédito abertas ou atrasos e
inadimplência?
<p><b>Resposta:</b> Mais uma vez é dificil afirmar com certeza devido ao equilibrio ruim entre os dados.</p>

B.3 Criação de variáveis derivadas
1. IncomePerDependent = MonthlyIncome / (NumberOfDependents + 1)
2. DebtPerLoan = DebtRatio / (NumberOfOpenCreditLinesAndLoans + 1)
3. Crie outras variáveis que você considerar úteis para os modelos.