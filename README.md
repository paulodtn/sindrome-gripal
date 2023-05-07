# Tratamento de dados de Síndrome Gripal

Este repositório visa tratar os dados sobre Síndrome Gripal presentes na API do [OpenSUS](https://opendatasus.saude.gov.br) de forma a responder os seguintes questionamentos:
 
* Qual o estado com a maior proporção de casos confirmados?
* Dentre os casos confirmados, qual a proporção de pacientes que
receberam ao menos 1 dose de vacina?
* Como é a distribuição de idade entre pacientes sintomáticos e
assintomáticos entre os casos confirmados?
* Para (pelo menos um) estados a sua escolha, construa uma
visualização para acompanhar a evolução dos casos ao longo do
período amostrado.
● Entre os pacientes sintomáticos, qual o sintoma mais frequente?

## Metodologia

Para completar esta tarefa, foram utilizadas as bibliotecas requests, json, pandas, XXX, YYYY, ZZZ nas seguintes versões

|library|version|
|---|---|
|pandas|vXXX|
|requests|vXXX|

## Gráfico de Número de Casos por Estado

A partir dos dados referentes ao número de casos de síndrome gripal por estado, podemos fazer a seguinte análise:

- **São Paulo** é o estado com maior número absoluto de casos, com 4382 registros, o que representa cerca de **40%** do total nacional.
- **Rio Grande do Sul** e **Rio de Janeiro** são os estados com o segundo e terceiro maior número de casos, respectivamente, com 1021 e 874 registros cada um, o que corresponde a cerca de **9%** e **8%** do total nacional.
- **Espírito Santo** é o estado com menor número de casos, com apenas 2 registros, o que representa menos de **0,1%** do total nacional.
- A região **Sudeste** é a que concentra o maior número de casos, com 5897 registros, o que equivale a cerca de **54%** do total nacional.
- A região **Norte** é a que apresenta o menor número de casos, com 349 registros, o que corresponde a cerca de **3%** do total nacional.

Esses dados podem refletir diferentes fatores, como a densidade populacional, o clima, a circulação de vírus, as medidas de prevenção e controle, entre outros.

## Gráfico de Casos em que o Paciente Tomou ao menos 1 Dose da Vacina

Os dados mostram que, dos 10000 casos de síndrome gripal registrados, **6699 (66,99%)** tomaram ao menos uma dose de vacina (**vacinados**), enquanto **3301 (33,01%)** não tomaram nenhuma dose (**não vacinados**). Isso significa que a maioria dos casos ocorreu em pessoas que se vacinaram parcial ou totalmente. Isso pode indicar que:

- A vacina não foi eficaz contra os vírus que causaram a síndrome gripal;
- As pessoas não completaram o esquema vacinal recomendado;
- As pessoas se expuseram a situações de risco de contágio após a vacinação;
- As pessoas apresentaram outras condições que afetaram a resposta imunológica à vacina;
- Houve algum problema na qualidade ou na aplicação da vacina.

Para confirmar essas hipóteses, seria necessário realizar mais estudos e análises sobre os casos de síndrome gripal e a vacinação. Também seria importante reforçar as medidas de prevenção não farmacológicas, como o uso de máscara, o distanciamento social e a higiene das mãos.

## Gráfico de Pacientes Sintomáticos e Assintomáticos por Faixa Etária

Uma possível análise dos dados referentes ao número de casos de síndrome gripal é a seguinte:

- O número total de casos **sintomáticos** é maior do que o de **assintomáticos** em todas as faixas etárias, o que indica que a doença tem uma alta taxa de manifestação clínica.
- A faixa etária com maior número absoluto de casos sintomáticos é a de **20 a 30 anos**, seguida pela de **30 a 40 anos**. Isso pode sugerir que esses grupos são mais expostos ao vírus ou que têm uma menor imunidade.
- A faixa etária com menor número absoluto de casos sintomáticos é a de **90 a 100 anos**, seguida pela de **80 a 90 anos**. Isso pode indicar que esses grupos são mais protegidos ou que têm uma maior letalidade.
- O gráfico de barras empilhadas permite visualizar a proporção relativa de casos sintomáticos e assintomáticos em cada faixa etária. Observa-se que essa proporção varia pouco entre as faixas, exceto pela de **90 a 100 anos**, que tem uma maior porcentagem de casos assintomáticos.

## Gráfico da Frequência de Sintomas por Paciente

![Gráfico de colunas](grafico.png)

De acordo com o gráfico, o sintoma mais frequente entre os pacientes com síndrome gripal é a tosse, com 5130 casos, seguido por coriza, com 3838 casos. O sintoma menos frequente é a alteração do olfato, com 289 casos. O gráfico também mostra que 2144 pacientes não apresentaram nenhum sintoma, ou seja, foram assintomáticos.
