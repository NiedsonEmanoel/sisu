import streamlit as st
import pandas as pd
import numpy as np

import pandas as pd

def make_soups(dfSOUP):
    if len(dfSOUP) == 0: return '<h4>Sem opções viáveis<h6>Estou triste... estude mais!</h6></h4>'
    final_soup = ''
    dfSOUP.reset_index()

    countsoup = 1


    for i in dfSOUP.index:

        dif = round(dfSOUP.loc[i, 'DIF'],2)
        recomDIF = ''
        if dif <= 0:
            recomDIF = 'Aguardar remanejamento.'
        elif dif <= 8:
            recomDIF = 'Zona de Ponto de Corte'
        else:
            recomDIF = 'Praticamente aprovado.'
        
        soups = f'''
<div class="card">
<div class="card-body">
<h5 class="card-title">{countsoup}º Opção: {dfSOUP.loc[i, 'NO_CURSO']} - {dfSOUP.loc[i, 'SG_IES_PP']}</h5>
<p class="card-text">{dfSOUP.loc[i, 'NO_CAMPUS']} - {dfSOUP.loc[i, 'NO_MUNICIPIO_CAMPUS_PP']}/{dfSOUP.loc[i, 'SG_UF_CAMPUS_PP']}</p>
<p class="card-text"><i>{dfSOUP.loc[i, 'DS_MOD_CONCORRENCIA']}</i></p>

<hr>
<p class="card-text"><b>Sua nota final da modalidade: {round(dfSOUP.loc[i, 'MEDIA_COM_BONUS'],2)}</b></p>
<hr>
<p class="card-text"><i><b>Diferença para o corte ({round(dfSOUP.loc[i, 'NU_NOTACORTE'],2)}): {round(dfSOUP.loc[i, 'DIF'],2)}</b></i>  <i>({recomDIF})</i></p>
</div>
</div>
<br>
'''
        final_soup = final_soup + soups
        countsoup = countsoup+1
    return final_soup

def main():
    st.set_page_config(layout="wide")
    st.markdown(f'<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>',unsafe_allow_html=True)
    st.markdown(f'<script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>',unsafe_allow_html=True)
    st.markdown(f'<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>',unsafe_allow_html=True)
    st.markdown(f'<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',unsafe_allow_html=True)
    

    st.header('Relatório SISU')
    luel = 0
    inheader = st.selectbox(
    'Qual sua edição de interesse?',
    ('2023.2', '2023.1', '2022.2', '2022.1', '2021.2', '2021.1', '2020.2', '2020.1', '2019.2', '2019.1'), index=None, placeholder="Selecione o sisu de interesse...")

    if inheader != None: luel =1
    if luel == 1:
        dfSisu = pd.read_csv(f'https://cdn.enemaster.app.br/Relat%C3%B3rios_SISU/{inheader}/sisu.csv', encoding='utf-8', decimal=',')

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

        if ((lc+ch+cn+mt+redacao)/5) > 100:
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
        continuoc = 0
        if len(uf) > 0:
            dfSisu = dfSisu.query('SG_UF_CAMPUS_PP == @uf')
            continuob = 0

            modalidade = st.multiselect(
                'Modalidade Concorrência',
                dfSisu['DS_MOD_CONCORRENCIA'].unique(), ['Ampla concorrência'])
            if len(modalidade) > 0:
                dfSisu = dfSisu.query('DS_MOD_CONCORRENCIA == @modalidade')
                continuoc = 1
                continuob =1

        if continuob==1:
            nome = st.multiselect(
                'Nome Universidade',
                dfSisu['SG_IES_PP'].unique(), dfSisu['SG_IES_PP'].unique())
            dfSisu = dfSisu.query('SG_IES_PP == @nome')
        #
        #(1-(dfSisu['QT_INSCRICAO']/(dfSisu['QT_VAGAS_CONCORRENCIA']+1)))*-1
        #dfSisu['QT_INSCRICAO']/(dfSisu['QT_VAGAS_CONCORRENCIA']
        try:
            dfSisu['CAND_VAGA'] = np.where(dfSisu['QT_VAGAS_CONCORRENCIA'] == 0,
                                        (1 - (dfSisu['QT_INSCRICAO'] / (dfSisu['QT_VAGAS_CONCORRENCIA'] + 1))) * -1,
                                        dfSisu['QT_INSCRICAO'] / dfSisu['QT_VAGAS_CONCORRENCIA'])
        except:
             dfSisu['CAND_VAGA'] = 0                       

        dfSisu['MEDIA_SEM_BONUS'] = ((dfSisu['PESO_REDACAO']*redacao+dfSisu['PESO_LINGUAGENS']*lc+dfSisu['PESO_MATEMATICA']*mt+dfSisu['PESO_CIENCIAS_HUMANAS']*ch+dfSisu['PESO_CIENCIAS_NATUREZA']*cn)/(dfSisu['PESO_REDACAO']+dfSisu['PESO_LINGUAGENS']+dfSisu['PESO_MATEMATICA']+dfSisu['PESO_CIENCIAS_HUMANAS']+dfSisu['PESO_CIENCIAS_NATUREZA']))
        dfSisu['MEDIA_COM_BONUS'] = ((100+dfSisu['NU_PERCENTUAL_BONUS_PP'])/100)*((dfSisu['PESO_REDACAO']*redacao+dfSisu['PESO_LINGUAGENS']*lc+dfSisu['PESO_MATEMATICA']*mt+dfSisu['PESO_CIENCIAS_HUMANAS']*ch+dfSisu['PESO_CIENCIAS_NATUREZA']*cn)/(dfSisu['PESO_REDACAO']+dfSisu['PESO_LINGUAGENS']+dfSisu['PESO_MATEMATICA']+dfSisu['PESO_CIENCIAS_HUMANAS']+dfSisu['PESO_CIENCIAS_NATUREZA']))
        mediaSimples = round(((lc+ch+cn+mt+redacao)/5),2)
        initialLEN = len(dfSisu)
        if redacao <= 39:
            dfSisu['MEDIA_SEM_BONUS'] = 0
            dfSisu['MEDIA_COM_BONUS'] = 0
            mediaSimples = 0

        dfSisu = dfSisu[dfSisu['NU_NOTACORTE']!= 0]

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
            if continuoc == 1:
                st.divider()
                col1, col2, col3 = st.columns(3)

                dfSisu = dfSisu[dfSisu['DIF']>= -30]

                if notaMenor != 0:
                    col1.metric(label="Menor nota de corte", value=f"{round(notaMenor,2)}", delta=f"{nomeMenor} - {ufMenor}")

                col1.metric(label="Sua 1ª melhor opção:", value=f"{max_value_row['SG_IES_PP']}", delta=f"{round(max_value_row['DIF'],2)} DIF p/ o Corte em {max_value_row['NO_MUNICIPIO_CAMPUS_PP']}/{max_value_row['SG_UF_CAMPUS_PP']}")

                col2.metric("Sua melhor média (com pesos)", f"{round(NotaMaiorMed,2)}", f'{nomeMaiorMed}/{ufMaiorMed}; Corte: {dorteMaiorMed}')
                loco = 0
                if NotaMaiorMeda != NotaMaiorMed:
                    col2.metric("Sua melhor média (com Bônus)", f"{round(NotaMaiorMeda,2)}", f'{nomeMaiorMeda}/{ufMaiorMeda}; Corte: {dorteMaiorMeda}')
                    loco = 1
                else:
                    col2.metric("Sua média (simples)", f"{mediaSimples}") 
                if CVMenor != 0:
                    col3.metric("Menor relação candidato/vaga", f"{round(CVMenor,2)} - {nomeMenorCV}", f"Corte: {round(notaMenorCV,2)}")
                else:
                    if loco == 0:
                        if NotaMaiorMeda!=NotaMaiorMed:
                            col3.metric("Sua melhor média (com Bônus)", f"{round(NotaMaiorMeda,2)}", f'{nomeMaiorMeda}/{ufMaiorMeda}; Corte: {dorteMaiorMeda}')
                        else:
                            col3.metric("Opções viáveis", f"{len(dfSisu)}", f'{len(dfSisu)} de {initialLEN} opções')

                col3.metric(label="Sua 2ª melhor opção:", value=f"{second_largest_value_row['SG_IES_PP']}", delta=f"{round(second_largest_value_row['DIF'],2)} DIF p/ o Corte em {second_largest_value_row['NO_MUNICIPIO_CAMPUS_PP']}/{second_largest_value_row['SG_UF_CAMPUS_PP']}")


                dfSisu.sort_values('DIF', ascending=False, inplace=True)
                st.divider()
            
                pre_soups = f'''<h5>Suas melhores opções (viáveis):</h5><div class="card-rows">'''

                soups = make_soups(dfSisu)

                pos_soups = f'''</div>'''
                st.markdown(f'''{pre_soups}{soups}{pos_soups}''',
            unsafe_allow_html=True)

                st.markdown(f'<img class="rounded mx-auto d-block" width="30%" src="https://cdn.enemaster.app.br/Images/logo.png">',unsafe_allow_html=True)


if __name__ == "__main__":
    main()