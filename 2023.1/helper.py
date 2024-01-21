#import streamlit as st
import pandas as pd
import numpy as np

import pandas as pd

# Leitura dos dataframes
dfVagas = pd.read_csv('./Brutos/vagas.csv', encoding='utf-8', decimal=',')
#dfVagas = dfVagas[dfVagas['NO_CURSO']=='MEDICINA']
dfInscricoes = pd.read_csv('./Brutos/inscricoes.csv', encoding='utf-8', decimal=',')
#dfInscricoes = dfInscricoes[dfInscricoes['NO_CURSO']=='MEDICINA']

# Colunas em comum
colunas_comuns = ['CO_IES', 'CO_IES_CURSO', 'NO_CURSO', 'DS_MOD_CONCORRENCIA', 'DS_TURNO',
                  'NO_CAMPUS', 'QT_VAGAS_CONCORRENCIA']

# Mesclar os dataframes usando as colunas em comum como chave
df_merged = pd.merge(dfVagas, dfInscricoes, on=colunas_comuns, how='inner', suffixes=('_vagas', '_PP'))

df_merged = df_merged.filter(regex='^(?!.*_vagas$)')
# Visualizar o dataframe resultante
df_merged['NU_NOTACORTE'].fillna(0, inplace=True)
df_merged['QT_INSCRICAO'].fillna(0, inplace=True)

df_merged.to_csv('sisu2023.1.csv', index=False, encoding='utf-8', decimal=',')
df_merged.to_excel('sisu2023.1.xlsx', index=False)