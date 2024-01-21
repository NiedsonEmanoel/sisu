import streamlit as st
import pandas as pd
import numpy as np

import pandas as pd

dfSisu = pd.read_csv('./2023.1/sisu2023.1.csv', encoding='utf-8', decimal=',')

st.header('Simulador SISU (2023.1)')
st.divider()
st.subheader('Notas Enem:')
col1, col2 = st.columns(2)
with col1:
    lc = st.number_input('Linguagens', min_value = 0.0, max_value=1000.0, step=0.1)
    ch = st.number_input('Humanas', min_value = 0.0, max_value=1000.0, step=0.1)
with col2:
    cn = st.number_input('Natureza', min_value = 0.0, max_value=1000.0, step=0.1)
    mt = st.number_input('Matemática', min_value = 0.0, max_value=1000.0, step=0.1)
redacao = st.number_input('Redação', min_value = 0, max_value=1000, step=20)
st.divider()

uf = []
cursos = []

if ((lc+ch+cn+mt)/5) > 100:
    st.subheader('Preferências:')
    cursos = st.multiselect(
        'Cursos de sua preferência',
        dfSisu['NO_CURSO'].unique(),
        ['MEDICINA'])
if len(cursos) > 0:
    dfSisu = dfSisu.query('NO_CURSO == @cursos')

    uf = st.multiselect(
        'Estados',
        dfSisu['SG_UF_CAMPUS_PP'].unique())

continuob = 0

if len(uf) > 0:
    dfSisu = dfSisu.query('SG_UF_CAMPUS_PP == @uf')
    continuob = 0

    modalidade = st.multiselect(
        'Modalidade Concorrência',
        dfSisu['DS_MOD_CONCORRENCIA'].unique(), ['Ampla concorrência'])
    if len(modalidade) > 0:
        dfSisu = dfSisu.query('DS_MOD_CONCORRENCIA == @modalidade')
        continuob =1

if continuob==1:
    nome = st.multiselect(
        'Nome Universidade',
        dfSisu['SG_IES_PP'].unique(), dfSisu['SG_IES_PP'].unique())
    dfSisu = dfSisu.query('SG_IES_PP == @nome')
#
#(1-(dfSisu['QT_INSCRICAO']/(dfSisu['QT_VAGAS_CONCORRENCIA']+1)))*-1
#dfSisu['QT_INSCRICAO']/(dfSisu['QT_VAGAS_CONCORRENCIA']

dfSisu['CAND_VAGA'] = np.where(dfSisu['QT_VAGAS_CONCORRENCIA'] == 0,
                               (1 - (dfSisu['QT_INSCRICAO'] / (dfSisu['QT_VAGAS_CONCORRENCIA'] + 1))) * -1,
                               dfSisu['QT_INSCRICAO'] / dfSisu['QT_VAGAS_CONCORRENCIA'])
                               

dfSisu['MEDIA_SEM_BONUS'] = ((dfSisu['PESO_REDACAO']*redacao+dfSisu['PESO_LINGUAGENS']*lc+dfSisu['PESO_MATEMATICA']*mt+dfSisu['PESO_CIENCIAS_HUMANAS']*ch+dfSisu['PESO_CIENCIAS_NATUREZA']*cn)/(dfSisu['PESO_REDACAO']+dfSisu['PESO_LINGUAGENS']+dfSisu['PESO_MATEMATICA']+dfSisu['PESO_CIENCIAS_HUMANAS']+dfSisu['PESO_CIENCIAS_NATUREZA']))
dfSisu['MEDIA_COM_BONUS'] = ((100+dfSisu['NU_PERCENTUAL_BONUS_PP'])/100)*((dfSisu['PESO_REDACAO']*redacao+dfSisu['PESO_LINGUAGENS']*lc+dfSisu['PESO_MATEMATICA']*mt+dfSisu['PESO_CIENCIAS_HUMANAS']*ch+dfSisu['PESO_CIENCIAS_NATUREZA']*cn)/(dfSisu['PESO_REDACAO']+dfSisu['PESO_LINGUAGENS']+dfSisu['PESO_MATEMATICA']+dfSisu['PESO_CIENCIAS_HUMANAS']+dfSisu['PESO_CIENCIAS_NATUREZA']))


ls = dfSisu[dfSisu['NU_NOTACORTE'] == dfSisu['NU_NOTACORTE'].min()].reset_index()
nomeMenor = ''
notaMenor = 0
ufMenor = ''
for i in ls.index:
    nomeMenor = ls.loc[i, 'SG_IES_PP']
    notaMenor = ls.loc[i, 'NU_NOTACORTE']
    ufMenor = ls.loc[i, 'SG_UF_CAMPUS_PP']

ls = dfSisu[dfSisu['CAND_VAGA'] == dfSisu['CAND_VAGA'].min()].reset_index()
nomeMenorCV = ''
notaMenorCV = 0
ufMenorCV = ''
CVMenor = 0

for i in ls.index:
    nomeMenorCV = ls.loc[i, 'SG_IES_PP']
    notaMenorCV = ls.loc[i, 'NU_NOTACORTE']
    ufMenorCV = ls.loc[i, 'SG_UF_CAMPUS_PP']
    CVMenor = round(ls.loc[i, 'CAND_VAGA'],2)
#
ls = dfSisu[dfSisu['MEDIA_SEM_BONUS'] == dfSisu['MEDIA_SEM_BONUS'].max()].reset_index()
nomeMaiorMed = ''
NotaMaiorMed = 0
ufMaiorMed = ''
dorteMaiorMed = 0

for i in ls.index:
    nomeMaiorMed = ls.loc[i, 'SG_IES_PP']
    dorteMaiorMed = ls.loc[i, 'NU_NOTACORTE']
    ufMaiorMed = ls.loc[i, 'SG_UF_CAMPUS_PP']
    NotaMaiorMed = ls.loc[i,'MEDIA_SEM_BONUS']

ls = dfSisu[dfSisu['MEDIA_COM_BONUS'] == dfSisu['MEDIA_COM_BONUS'].max()].reset_index()
nomeMaiorMeda = ''
NotaMaiorMeda = 0
ufMaiorMeda = ''
dorteMaiorMeda = 0

for i in ls.index:
    nomeMaiorMeda = ls.loc[i, 'SG_IES_PP']
    dorteMaiorMeda = ls.loc[i, 'NU_NOTACORTE']
    ufMaiorMeda = ls.loc[i, 'SG_UF_CAMPUS_PP']
    NotaMaiorMeda = ls.loc[i,'MEDIA_COM_BONUS']

dfSisu['DIF'] = dfSisu['MEDIA_COM_BONUS'] - dfSisu['NU_NOTACORTE']
max_value_row = dfSisu.loc[dfSisu['DIF'].idxmax()].to_dict()

# Encontrar o índice do segundo maior valor
second_largest_index = dfSisu['DIF'].nlargest(2).index[-1]

# Usar o índice para obter a linha correspondente
second_largest_value_row = dfSisu.loc[second_largest_index].to_dict()

#nu_notacorte_value = max_value_row['NU_NOTACORTE']
#st.write(f'Valor máximo em formato de dicionário:\n{max_value_row}')
#st.write(f'Segundo maior valor em formato de dicionário:\n{second_largest_value_row}')

if continuob==1:
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Menor nota de corte", value=f"{round(notaMenor,2)}", delta=f"{nomeMenor} - {ufMenor}")
    col1.metric(label="Sua 1ª melhor opção:", value=f"{max_value_row['SG_IES_PP']}", delta=f"{round(max_value_row['DIF'],2)} DIF p/ o Corte em {max_value_row['NO_MUNICIPIO_CAMPUS_PP']}/{max_value_row['SG_UF_CAMPUS_PP']}")

    col2.metric("Sua melhor média (com pesos)", f"{round(NotaMaiorMed,2)}", f'{nomeMaiorMed}/{ufMaiorMed}; Corte: {dorteMaiorMed}')
    if NotaMaiorMeda != NotaMaiorMed:
        col2.metric("Sua melhor média (com Bônus)", f"{round(NotaMaiorMeda,2)}", f'{nomeMaiorMeda}/{ufMaiorMeda}; Corte: {dorteMaiorMeda}')
    else:
        col2.metric("Sua média (simples)", f"{round(((lc+ch+cn+mt+redacao)/5),2)}") 
    col3.metric("Menor relação candidato/vaga", f"{round(CVMenor,2)} - {nomeMenorCV}", f"Corte: {round(notaMenorCV,2)}")
    col3.metric(label="Sua 2ª melhor opção:", value=f"{second_largest_value_row['SG_IES_PP']}", delta=f"{round(second_largest_value_row['DIF'],2)} DIF p/ o Corte em {second_largest_value_row['NO_MUNICIPIO_CAMPUS_PP']}/{second_largest_value_row['SG_UF_CAMPUS_PP']}")


    dfSisu = dfSisu[dfSisu['DIF']>= -28]
    dfSisu.sort_values('DIF', ascending=False, inplace=True)
    st.divider()
    st.caption('Suas melhores opções...')
    st.write(dfSisu.reset_index())

    st.subheader('*feito por: Niedson Emanoel.')


