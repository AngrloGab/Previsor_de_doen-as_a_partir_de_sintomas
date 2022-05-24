import joblib
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner
import requests

# Importando os datasets
naive_symtoms = joblib.load("modeloTreinadoSintomas")
Descricao_sintomas = pd.read_csv("symptom_Description.csv")
symptomsAndDisiases = pd.read_csv("dataset.csv")
Precaucao = pd.read_csv("symptom_precaution.csv")
sintomas = []

# Recuperando os sintomas
with open("sintomas.txt", "r") as f:
    for sintoma in f:
        sintoma = sintoma.replace("\n", "")
        if "_" in sintoma:
            sintoma = sintoma.split("_")
            sintoma = " ".join(sintoma)
        sintomas.append(sintoma)
    f.close()

# Função que diagnostica a doença a partir dos sintomas


def diagnosticar(sintms):
    global sintomas
    global naive_symtoms

    sintms = sintms.split(", ")
    entrada = [0] * len(sintomas)
    i = 0
    for sintoma in sintomas:
        for sinP in sintms:
            if sintoma == sinP:
                entrada[i] = 1
        i += 1
    prev = naive_symtoms.predict([entrada])
    val = prev[0]
    return val


# Função que realiza o load do gif
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


st.set_page_config(page_title="Disiase predictor",
                   page_icon='👨‍⚕️', layout="centered")

lottieURL = "https://assets7.lottiefiles.com/packages/lf20_otmfyizb.json"
lottie_doc = load_lottieurl(lottieURL)
st_lottie(lottie_doc, key="doc")

st.write('Diseases and their symptoms: ')
st.dataframe(symptomsAndDisiases)

st.title('Tell me how you feel')

# Capturando os sintomas e prevendo a doença
sintomasEntrada = st.text_input('Write your symptoms', '')
if st.button('Diagnose'):
    sintomasEntrada = diagnosticar(sintomasEntrada)

    doenca_desc = Descricao_sintomas[Descricao_sintomas['Disease']
                                     == sintomasEntrada]
    doenca_desc = doenca_desc["Description"]
    doenca_desc = doenca_desc.iloc[0]

    Precaucao = Precaucao[Precaucao["Disease"] == sintomasEntrada]
    Precaucao.fillna("", inplace=True)
    listaPrecaucoes = []

    clmn = list(Precaucao)
    listaDePrecaucoes = []

    for i in clmn:
        # printing a third element of column
        pre = Precaucao[i].iloc[0]
        if pre != sintomasEntrada:
            listaDePrecaucoes.append(pre)

    if "" in listaDePrecaucoes:
        listaDePrecaucoes.remove("")
    precaucoes = ", ".join(listaDePrecaucoes)

    st.write('You were diagnosed with: ')
    st.write('# ', sintomasEntrada)
    st.write('', doenca_desc)
    st.write('Precautions: ', precaucoes)
else:
    st.write('your disiase will appear here')
