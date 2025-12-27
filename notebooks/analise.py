# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick
import seaborn as sns

# %%
# Troque pelo nome do seu arquivo CSV
df = pd.read_csv('../data/DENGBR25.csv')

# Verifique se carregou
print(df.head())

nunique = df.nunique(dropna=False).sort_values()

# %%
df.describe()

# %%
#Drop das colunas 100% NaN
cols_100_nan = [
    "DOENCA_TRA","MANI_HEMOR","EPISTAXE","GENGIVO","METRO","PETEQUIAS",
    "HEMATURA","SANGRAM","LACO_N","PLASMATICO","EVIDENCIA","PLAQ_MENOR",
    "CON_FHD","COMPLICA","MIGRADO_W"
]
df = df.drop(columns=cols_100_nan, errors="ignore")

df.describe()

# %%
#Drop das colunas que não possuem valores uteis para a analise de casos graves de dengue 
colunas_sem_valor_analise = [
    "TP_NOT", "ID_AGRAVO", "DT_NOTIFIC", "SEM_NOT", "NU_ANO",
    "SG_UF_NOT", "ID_MUNICIP", "ID_REGIONA", "ID_UNIDADE",
    "DT_SIN_PRI", "SEM_PRI","ANO_NASC", "NU_IDADE_N", "CS_GESTANT", "CS_RACA", "CS_ESCOL_N",
    "SG_UF", "ID_MN_RESI", "ID_RG_RESI", "ID_PAIS","DT_INVEST", "ID_OCUPA_N","DOENCA_TRA", "MANI_HEMOR", 
    "EPISTAXE", "GENGIVO", "METRO", "PETEQUIAS", "HEMATURA", "SANGRAM", "LACO_N", "PLASMATICO",
    "EVIDENCIA", "PLAQ_MENOR", "CON_FHD", "COMPLICA", "MIGRADO_W",
    "DT_CHIK_S1", "DT_CHIK_S2", "DT_PRNT", "DT_SORO", "DT_NS1", "DT_VIRAL", 
    "DT_PCR", "DT_INTERNA", "DT_OBITO", "DT_ENCERRA", "DT_ALRM", "DT_GRAV", 
    "DT_DIGITA", "GRAV_PULSO", "GRAV_CONV", "GRAV_ENCH", "GRAV_INSUF", "GRAV_TAQUI",
    "GRAV_EXTRE", "GRAV_HIPOT", "GRAV_HEMAT", "GRAV_MELEN",
    "GRAV_METRO", "GRAV_SANG", "GRAV_AST", "GRAV_MIOC",
    "GRAV_CONSC", "GRAV_ORGAO", "UF", "MUNICIPIO", "COUFINF", "COPAISINF",
    "COMUNINF", "CLASSI_FIN", "NDUPLIC_N", "FLXRECEBI", "CRITERIO", "EVOLUCAO"
]

df = df.drop(columns=colunas_sem_valor_analise, errors="ignore")

# %%
nan_pct = (df.isna().mean() * 100).sort_values(ascending=False)

top = nan_pct.head(60)

plt.figure(figsize=(12, 6))
plt.bar(top.index.astype(str), top.values)
plt.xticks(rotation=90)
plt.ylabel('% NaN')
plt.title('Top 30 colunas com maior % de NaN (após drop)')
plt.tight_layout()
plt.show()


# %%
# O data_frame_subs será o data frame com valores substituidos, criando uma nova categoria
data_frame_subs = df.copy()

# O data_frame_convert será o data frame com valores convertidos, convertendo os nan em valores que ja existam
data_frame_convert = df.copy()

# %% [markdown]
# ### 4.1 Definição de Sintomas e Comorbidades
#
# Definição das colunas que representam sintomas clínicos, sinais de alarme e comorbidades. Estas variáveis binárias terão seus valores ausentes tratados de acordo com as duas estratégias definidas.

# %%
# Trantando os Nan como o valor 2(não), afim de ajustar os dados para o modelo
colunas_nan_nao = [
    "RENAL", "HEPATOPAT", "HIPERTENSA", "FEBRE", "MIALGIA", "CEFALEIA",
    "EXANTEMA", "VOMITO", "NAUSEA", "DOR_COSTAS", "CONJUNTVIT",
    "ARTRITE", "ARTRALGIA", "PETEQUIA_N", "LEUCOPENIA", "LACO",
    "DOR_RETRO", "DIABETES", "HEMATOLOG", "ACIDO_PEPT", "AUTO_IMUNE",
    "ALRM_HIPOT", "ALRM_PLAQ", "ALRM_VOM", "ALRM_SANG", "ALRM_HEMAT",
    "ALRM_ABDOM", "ALRM_LETAR", "ALRM_HEPAT", "ALRM_LIQ",
]


# %%
# Converter os valores Nan, tratando eles como se fossem 3(não informado)
data_frame_subs[colunas_nan_nao] = (
    data_frame_subs[colunas_nan_nao].fillna(3)
)

# %%
# Converter os valores Nan, tratando eles como se fossem 2(não)
data_frame_convert[colunas_nan_nao] = (
    data_frame_convert[colunas_nan_nao].fillna(2)
)

# %%
# Colunas com quatro opções possiveis de valor
colunas_quatro_valores_possiveis = [
    "RES_CHIKS1", "RES_CHIKS2", "RESUL_PRNT", "RESUL_SORO", "RESUL_NS1", 
    "RESUL_VI_N", "RESUL_PCR_", "HISTOPA_N", "IMUNOH_N"
]

# %%
# Converter os valores Nan, tratando eles como se fossem 4(não realizado)
data_frame_subs[colunas_quatro_valores_possiveis] = (
    data_frame_subs[colunas_quatro_valores_possiveis].fillna(4)
)

# Converter os valores Nan, tratando eles como se fossem 5(não informado)
data_frame_convert[colunas_quatro_valores_possiveis] = (
    data_frame_convert[colunas_quatro_valores_possiveis].fillna(4)
)

# %%
# Converter os valores Nan, em "SOROTIPO", tratando eles como se fossem 5(não informado)
data_frame_subs["SOROTIPO"] = (
    data_frame_subs["SOROTIPO"].fillna(5)
)

data_frame_convert["SOROTIPO"] = (
    data_frame_convert["SOROTIPO"].fillna(5)
)

# %%
# Converter os valores Nan, em "HOSPITALIZ", tratando eles como se 
# fossem 3(Não informado)
data_frame_subs["HOSPITALIZ"] = (
    data_frame_subs["HOSPITALIZ"].fillna(3)
)

# Converter os valores Nan, em "HOSPITALIZ", tratando eles como se 
# fossem 9(IGNORADO)
data_frame_convert["HOSPITALIZ"] = (
    data_frame_convert["HOSPITALIZ"].fillna(9)
)

# %%
# Converter os valores Nan, em "TPAUTOCTO", tratando eles como se 
# fossem 4(Não informado)
data_frame_subs["TPAUTOCTO"] = (
    data_frame_subs["TPAUTOCTO"].fillna(4)
)

# Converter os valores Nan, em "TPAUTOCTO", tratando eles como se 
# fossem 3(Indeterminado)
data_frame_convert["TPAUTOCTO"] = (
    data_frame_convert["TPAUTOCTO"].fillna(3)
)

# %%
# Converter os valores Nan, em "CLINC_CHIK", tratando eles como se 
# fossem 3(Não informado)
data_frame_subs["CLINC_CHIK"] = (
    data_frame_subs["CLINC_CHIK"].fillna(3)
)

data_frame_convert["CLINC_CHIK"] = (
    data_frame_convert["CLINC_CHIK"].fillna(3)
)

# %%
# Converter os valores Nan, em "TP_SISTEMA", tratando eles como se 
# fossem 3(Não informado)
data_frame_subs["TP_SISTEMA"] = (
    data_frame_subs["TP_SISTEMA"].fillna(3)
)

data_frame_convert["TP_SISTEMA"] = (
    data_frame_convert["TP_SISTEMA"].fillna(3)
)

# %%
colunas_com_nan = data_frame_convert.columns[
    data_frame_convert.isna().any()
].tolist()

colunas_com_nan

# %%
# Data frame com os valores substituidos, com novos valores
data_frame_subs.head()

# %%
# Data frame com os valores convertidos, para algum valor possivel
data_frame_convert.head()

# %%
regioes_unicas = data_frame_convert['TPAUTOCTO'].unique()

print(regioes_unicas)

# %% [markdown]
# ## Análise gráfica de fatores associados a hospitalização
#
#
# 1. Criação de variáveis binárias para facilitar a análise. A variável de hospitalização será convertida para formato binário onde 1 indica hospitalização e 0 indica não hospitalização.

# %%
def sinan_bin(x):
    if x == 1:
        return 1
    if x == 2:
        return 0
    return None  # ignora 9, NaN, etc
df_visualizer = df.copy()

df_visualizer["hosp_bin"] = df_visualizer["HOSPITALIZ"].apply(sinan_bin)
# %% [markdown]
#
# ### 1.1 Visualização Geral de Hospitalizações
#
# Grafico para mostrar proporção de casos hospitalizados vs total de casos notificados.
# %%

total_ocurrences = df_visualizer["hosp_bin"].notna().sum()
total_hospitalized = df_visualizer["hosp_bin"].sum()

labels = ["Casos", "Hospitalizações"]
values = [total_ocurrences, total_hospitalized]

plt.figure(figsize=(6,4))
plt.bar(labels, values)
plt.ylabel("Quantidade")
plt.title("Total de casos vs hospitalizações")
plt.show()

# %% [markdown]
# ### 1.2 Impacto de Sintomas e Comorbidades
#
# Análise do impacto cada sintoma e comorbidade na taxa de hospitalização. O objetivo é identificar quais variáveis clínicas estão associadas com casos graves que necessitam hospitalização.

# %%
symptoms = [
    "FEBRE",
    "MIALGIA",
    "CEFALEIA",
    "EXANTEMA",
    "VOMITO",
    "NAUSEA",
    "DOR_COSTAS",
    "CONJUNTVIT",
    "ARTRITE",
    "ARTRALGIA",
    "PETEQUIA_N",     
    "LEUCOPENIA",   
    "LACO",          
    "DOR_RETRO"      
]

deseases = [
    "DIABETES",
    "HEMATOLOG",
    "HEPATOPAT",
    "RENAL",
    "HIPERTENSA",
    "ACIDO_PEPT",
    "AUTO_IMUNE"
]

# %% [markdown]
# Conversão das variáveis clínicas para formato binário, onde 1 representa presença do sintoma/comorbidade e 0 representa ausência.

# %%
def sinan_bin(s):
    x = pd.to_numeric(s, errors="coerce")
    return x.map({1: 1.0, 2: 0.0})



variables = symptoms + deseases
X = df_visualizer[variables].apply(sinan_bin)


y = sinan_bin(df_visualizer["HOSPITALIZ"]).rename("hosp") 

# %% [markdown]
# Cálculo da diferença na taxa de hospitalização entre pacientes com e sem cada sintoma/comorbidade.
#
# **Como interpretar**: Valores positivos indicam que a presença do sintoma/doença aumenta a probabilidade de hospitalização. A diferença é medida em **pontos percentuais (pp)**.
#
# **Exemplo prático**: Se 5% dos pacientes sem diabetes são hospitalizados e 15% dos pacientes com diabetes são hospitalizados, a diferença é de +10 pontos percentuais. Isso significa que ter diabetes está associado a um aumento de 10 pontos percentuais na taxa de hospitalização.

# %%
rates = []
for col in variables:
    tmp = pd.concat([X[col], y.rename("hosp")], axis=1).dropna()


    grp = tmp.groupby(col)["hosp"].mean()

    hosp_rate_no  = grp.get(0.0, np.nan)  
    hosp_rate_yes = grp.get(1.0, np.nan)  

    rates.append({
        "symptom": col,
        "hosp_rate_no": hosp_rate_no,
        "hosp_rate_yes": hosp_rate_yes,
        "delta_pp": (hosp_rate_yes - hosp_rate_no) * 100
    })

rates_df = pd.DataFrame(rates).sort_values("delta_pp", ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

ax1.barh(rates_df["symptom"], rates_df["hosp_rate_yes"] * 100, color='coral', alpha=0.8)
ax1.set_xlabel("Taxa de Hospitalização (%)", fontsize=12)
ax1.set_ylabel("Sintoma ou Doença", fontsize=12)
ax1.set_title("COM o sintoma/doença", fontsize=13, fontweight='bold')
ax1.grid(axis='x', alpha=0.3, linestyle='--')

ax2.barh(rates_df["symptom"], rates_df["hosp_rate_no"] * 100, color='lightblue', alpha=0.8)
ax2.set_xlabel("Taxa de Hospitalização (%)", fontsize=12)
ax2.set_title("SEM o sintoma/doença", fontsize=13, fontweight='bold')
ax2.set_yticklabels([])  # Remove labels duplicados
ax2.grid(axis='x', alpha=0.3, linestyle='--')

fig.suptitle('Comparação: Taxa de Hospitalização por Dengue\nPacientes COM vs SEM cada sintoma/doença', 
             fontsize=15, fontweight='bold', y=0.98)

fig.text(0.5, 0.02, 
         'Quanto MAIOR a diferença entre as barras, MAIOR o impacto do sintoma/doença na hospitalização',
         ha='center', fontsize=11, style='italic',
         bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

plt.tight_layout(rect=[0, 0.03, 1, 0.96])
plt.show()

# %% [markdown]
# ### 5.3 Análise por Faixa Etária e Doença
#
# Investigação da relação entre idade, presença de doença(diabetes) e risco de hospitalização.
#  A idade é uma variável importante em dengue, especialmente quando combinada com comorbidades como diabetes.
#
#

# %% [markdown]
# Conversão da variável de idade do formato SINAN para anos. O campo NU_IDADE_N armazena idade codificada onde os primeiros dígitos indicam a unidade (horas, dias, meses ou anos).


# %%
bins = [0, 5, 15, 30, 50, 65, 120]
labels = ["0-4","5-14","15-29","30-49","50-64","65+"]

def age_years(nu_age):
    if pd.isna(nu_age):
        return np.nan

    try:
        nu_age = int(nu_age)
    except:
        return np.nan

    unidade = nu_age // 1000
    valor   = nu_age % 1000

    if unidade == 1:      # horas
        return valor / (24 * 365)
    elif unidade == 2:    # dias
        return valor / 365
    elif unidade == 3:    # meses
        return valor / 12
    elif unidade == 4:    # anos
        return valor
    else:
        return np.nan
    
df_visualizer["age_years"] = df_visualizer["NU_IDADE_N"].apply(age_years)

df_visualizer["age_range"] = pd.cut(df_visualizer["age_years"], bins=bins, labels=labels)

tmp = pd.concat([
    X["DIABETES"],
    y,
    df_visualizer["age_range"]
], axis=1).dropna()

rate_age = (
    tmp
    .groupby(["age_range", "DIABETES"])["hosp"]
    .mean()
    .reset_index()
)
rate_age

for v in [0.0, 1.0]:
    sub = rate_age[rate_age["DIABETES"] == v]
    plt.plot(sub["age_range"], sub["hosp"], marker="o", label=f"Diabetes={int(v)}")

plt.ylabel("Taxa de hospitalização")
plt.xlabel("Faixa etária")
plt.title("Hospitalização por diabetes, estratificada por idade")

plt.legend()
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 5.4 Sazonalidade da Hospitalização
#
# Análise temporal para identificar padrões sazonais na taxa de hospitalização.

# %%
df["dt_sint"] = pd.to_datetime(df["DT_SIN_PRI"], errors="coerce")
df["mes"] = df["dt_sint"].dt.month

tmp = pd.concat([y, df["mes"]], axis=1).dropna()

rate_month = (
    tmp
    .groupby("mes")["hosp"]
    .mean()
)

plt.figure(figsize=(8,4))
rate_month.plot(marker="o")
plt.xlabel("Mês")
plt.ylabel("Taxa de hospitalização")
plt.title("Sazonalidade da hospitalização (por mês)")
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.grid(True)
plt.show()

# %% [markdown]
# ### 5.5 Fatores de Risco Específicos
#
# Análise de grupos de risco específicos, incluindo gestantes e presença de sinais de alarme. Estes fatores são particularmente importantes para identificação precoce de casos graves.

x# sexo feminino

# %% [markdown]
# Comparação da taxa de hospitalização entre gestantes e não gestantes. A gravidez é um fator de risco conhecido para complicações de dengue.

# %%

df["sex_female"] = (df["CS_SEXO"] == "F").astype("Int64")
df_f = df[df["CS_SEXO"].eq("F")].copy()

def gestante_bin(v):
    if v in [1, 2, 3, 4]:
        return 1.0   # gestante
    if v == 5:
        return 0.0   # não gestante
    return None      # ignora 6, 9, NaN

df["pregnant"] = df["CS_GESTANT"].apply(gestante_bin)


tmp = pd.concat([df["pregnant"], y.loc[df_f.index]], axis=1).dropna()

resultado_gestantes = tmp.groupby("pregnant").mean()
print(resultado_gestantes)

# Gráfico de barras para gestantes
plt.figure(figsize=(8, 5))
resultado_gestantes.plot(kind='bar', legend=False)
plt.xlabel("Status de Gravidez")
plt.ylabel("Taxa de Hospitalização")
plt.title("Taxa de Hospitalização: Gestantes vs Não Gestantes")
plt.xticks([0, 1], ['Não Gestante', 'Gestante'], rotation=0)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.tight_layout()
plt.show()


# %% [markdown]
# ### 5.7 Distribuição de Casos por Faixa Etária
#
# Visualização da quantidade de casos em cada faixa etária para identificar os grupos mais afetados.

# %%
# Distribuição por faixa etária
faixa_counts = df_visualizer["age_range"].value_counts().sort_index()

plt.figure(figsize=(10, 5))
faixa_counts.plot(kind='bar', color='steelblue')
plt.xlabel("Faixa Etária")
plt.ylabel("Número de Casos")
plt.title("Distribuição de Casos de Dengue por Faixa Etária")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### 5.8 Correlação entre Sintomas
#
# Mapa de calor mostrando a correlação entre diferentes sintomas. Valores próximos a 1 indicam que os sintomas tendem a aparecer juntos.

# %%
# Heatmap de correlação entre sintomas
import seaborn as sns

correlacao = X[symptoms].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(correlacao, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title("Correlação entre Sintomas de Dengue")
plt.tight_layout()
plt.show()


