import streamlit as st
import pandas as pd
import numpy as np

import pandas as pd

dfSisu = pd.read_csv('./2023.1/sisu2023.1.csv', encoding='utf-8', decimal=',')
dfSisu['NU_NOTACORTE'].fillna(0, inplace=True)
dfSisu['QT_INSCRICAO'].fillna(0, inplace=True)
