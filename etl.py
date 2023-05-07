import requests
import json
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import plotly.graph_objects as go
import matplotlib.dates as mdates
from pathlib import Path

# ETL
url = "https://elasticsearch-saps.saude.gov.br/desc-esus-notifica-estado-*/_search"

payload = json.dumps({"size": 10000})
headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic dXNlci1wdWJsaWMtbm90aWZpY2Fjb2VzOlphNHFOWGR5UU5TYTlZYUE=",
}

response = requests.request("POST", url, headers=headers, data=payload)

visual = response.json()

csv = pd.json_normalize(visual["hits"]["hits"])
csv.columns = csv.columns.str.replace("_source.", "")
csv["has_numbers"] = csv["codigoDosesVacina"].apply(lambda x: len(x) > 0)
csv["sintomas"] = csv["sintomas"].str.replace(", ", ",")
timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

csv.to_csv(f"csv/datasus_sindromegripal_{timestamp}.csv", index=False, sep=",")


# 1
# Qual o estado com a maior proporção de casos confirmados?
# Gráfico de barras empilhadas
df_estados = csv[["estado"]]
counts = df_estados.value_counts()
fig, ax = plt.subplots(figsize=(15, 6))

counts.plot.bar(stacked=True, ax=ax, width=0.8, edgecolor="white", linewidth=0.5)

ax.set_title("Ocorrências de Síndrome Gripal por Unidade de Federação (UF)")
ax.set_xlabel("Unidades da Federação")
ax.set_ylabel("Frequência de casos")

for p in ax.containers:
    ax.bar_label(p, label_type="edge", fontsize=8)

ax.grid(color="lightgrey", linestyle="-", linewidth=0.5)
ax.spines["bottom"].set_color("white")
ax.spines["top"].set_color("white")
ax.spines["right"].set_color("white")
ax.spines["left"].set_color("white")

plt.savefig(f"imagens/ocorrencia_por_UF_{timestamp}.png", dpi=300)


# 2
# Dentre os casos confirmados, qual a proporção de pacientes que
# receberam ao menos 1 dose de vacina?
# Grafico de pizza, rosca ou barra
# df_vacinados = csv[['has_numbers']]
csv_filtrado = csv[["has_numbers", "estado"]]
counts = csv_filtrado.groupby("estado")["has_numbers"].value_counts().unstack()

ax = counts.plot.bar(figsize=(15, 10), width=0.8)

for p in ax.containers:
    ax.bar_label(p, label_type="edge", fontsize=8)

ax.grid(color="lightgrey", linestyle="solid", linewidth=0.5)
ax.spines["bottom"].set_color("white")
ax.spines["top"].set_color("white")
ax.spines["right"].set_color("white")
ax.spines["left"].set_color("white")

ax.set_title(
    "Frequência entre vacinados e não-vacinados com Síndrome Gripal, por Unidade da Federação"
)
ax.set_xlabel("Estado")
ax.set_ylabel("Frequência")
ax.legend(labels=["Não-vacinados", "Vacinados"])


plt.savefig(f"imagens/ocorrencia_vacinados_por_UF_{timestamp}.png", dpi=300)

# 3
# Como é a distribuição de idade entre pacientes sintomáticos e
# assintomáticos entre os casos confirmados?
df_sintomas = csv[["idade", "sintomas"]]

df_sintomas["sintomatico"] = df_sintomas["sintomas"].apply(
    lambda x: "sim" if x != "Assintomático" else "nao"
)

faixas_etarias = pd.cut(
    df_sintomas["idade"], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
)

counts = pd.crosstab(faixas_etarias, df_sintomas["sintomatico"])

ax = counts.plot.barh(width=0.8, figsize=(10, 15))
for i in ax.containers:
    ax.bar_label(i, label_type="edge", fontsize=10)

ax.grid(color="lightgrey", linestyle="solid", linewidth=0.5)
ax.spines["bottom"].set_color("white")
ax.spines["top"].set_color("white")
ax.spines["right"].set_color("white")
ax.spines["left"].set_color("white")

ax.set_title("Frequência de Sintomáticos e Assintomáticos por Faixa Etária")
ax.set_xlabel("Contagem")
ax.set_ylabel("Faixa Etária")
ax.invert_xaxis()


plt.savefig(f"ocorrencia_por_idade_vacina_{timestamp}.png", dpi=300)

# 4
# Para (pelo menos um) estados a sua escolha, construa uma
# visualização para acompanhar a evolução dos casos ao longo do
# período amostrado.
nordeste = [
    "Pernambuco",
    "Alagoas",
    "Sergipe",
    "Rio Grande do Norte",
    "Maranhão",
    "Paraíba",
    "Bahia",
    "Ceará",
    "Piauí",
]
ne = csv[csv["estado"].isin(nordeste)]
ne["dataNotificacao"] = pd.to_datetime(ne["dataNotificacao"])
ne["data"] = ne["dataNotificacao"].dt.strftime("%m-%Y")
ne_casos_tempo = ne.groupby(["estado", "data"]).size().reset_index(name="casos")

ne_casos_tempo["data"] = pd.to_datetime(ne_casos_tempo["data"], format="%m-%Y")

ne_casos_tempo = ne_casos_tempo.sort_values(["data"])

pivot_table = pd.pivot_table(
    ne_casos_tempo, values="casos", index="estado", columns="data", fill_value=0
)


locator = mdates.MonthLocator(interval=3)

ax.xaxis.set_major_locator(locator)

ax = pivot_table.T.plot(kind="line", figsize=(20, 10))
ax.legend(loc="lower center", ncol=3)
ax.set_xlabel("Mês/Ano")
ax.set_ylabel("Número de casos")
ax.set_title("Evolução dos casos de síndrome gripal por Estados do Nordeste")

ax.grid(color="lightgrey", linestyle="solid", linewidth=0.5)
ax.spines["bottom"].set_color("white")
ax.spines["top"].set_color("white")
ax.spines["right"].set_color("white")
ax.spines["left"].set_color("white")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=3)

plt.savefig(f"imagens/evolucao_ne_{timestamp}.png", dpi=300)


# INTERATIVO QUARTA QUESTAO
fig_dict = {}
ne_casos_tempo = ne_casos_tempo.sort_values(by="data")

# itera pelos estados
for estado in ne_casos_tempo["estado"].unique():
    df_estado = ne_casos_tempo[ne_casos_tempo["estado"] == estado]

    fig_dict[estado] = go.Scatter(
        x=df_estado["data"], y=df_estado["casos"], line=dict(width=3), name=estado
    )

fig = go.Figure(list(fig_dict.values()))

fig.update_layout(
    title="Evolução do número de casos de síndrome gripal nos estados entre Abril/2021 e Abril/2023",
)

fig.update_layout(
    legend=dict(
        x=0,
        y=1,
        traceorder="normal",
        font=dict(family="sans-serif", size=12, color="black"),
        bgcolor="White",
        bordercolor="Black",
        borderwidth=1,
    )
)

fig.write_html(f"imagens/interativo_{timestamp}.html")
# 5
# Entre os pacientes sintomáticos, qual o sintoma mais frequente?

sintomas_dummies = csv["sintomas"].str.get_dummies(sep=",")
sintomas_freq_por_paciente = sintomas_dummies.sum().sort_values(ascending=False)

ax = sintomas_freq_por_paciente.plot(kind="bar", stacked=True)

ax.grid(color="lightgrey", linestyle="solid", linewidth=0.5)
ax.spines["bottom"].set_color("white")
ax.spines["top"].set_color("white")
ax.spines["right"].set_color("white")
ax.spines["left"].set_color("white")

ax.set_title("Frequência dos sintomas em afetados por Síndrome Gripal")
ax.set_xlabel("Sintoma")
ax.set_ylabel("Frequência")

for i, v in enumerate(sintomas_freq_por_paciente.values):
    ax.annotate(str(v), xy=(i, v), ha="center", va="bottom")


plt.savefig(f"imagens/frequencia_sintomas_{timestamp}.png", dpi=300)
