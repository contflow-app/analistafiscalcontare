import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd
from io import BytesIO

# Tabela de validação fiscal ampliada com CFOPs adicionais
TABELA_VALIDACAO = pd.DataFrame([
    {'CFOP': '5101', 'CST_ICMS': '00', 'CST_PIS': '01', 'CST_COFINS': '01', 'Regime': 'Lucro Presumido', 'Valido': True},
    {'CFOP': '5101', 'CST_ICMS': '40', 'CST_PIS': '04', 'CST_COFINS': '04', 'Regime': 'Lucro Presumido', 'Valido': False},
    {'CFOP': '6101', 'CST_ICMS': '00', 'CST_PIS': '01', 'CST_COFINS': '01', 'Regime': 'Lucro Presumido', 'Valido': True},
    {'CFOP': '6101', 'CST_ICMS': '40', 'CST_PIS': '04', 'CST_COFINS': '04', 'Regime': 'Lucro Presumido', 'Valido': False},
    {'CFOP': '5102', 'CST_ICMS': '20', 'CST_PIS': '01', 'CST_COFINS': '01', 'Regime': 'Lucro Presumido', 'Valido': True},
    {'CFOP': '5102', 'CST_ICMS': '60', 'CST_PIS': '04', 'CST_COFINS': '04', 'Regime': 'Lucro Presumido', 'Valido': False},
    {'CFOP': '6108', 'CST_ICMS': '41', 'CST_PIS': '05', 'CST_COFINS': '05', 'Regime': 'Lucro Real', 'Valido': True},
    {'CFOP': '6108', 'CST_ICMS': '41', 'CST_PIS': '01', 'CST_COFINS': '01', 'Regime': 'Lucro Real', 'Valido': False},
    {'CFOP': '6108', 'CST_ICMS': '41', 'CST_PIS': '04', 'CST_COFINS': '04', 'Regime': 'Lucro Presumido', 'Valido': False},
    {'CFOP': '1102', 'CST_ICMS': '00', 'CST_PIS': '01', 'CST_COFINS': '01', 'Regime': 'Lucro Presumido', 'Valido': True},
    {'CFOP': '2101', 'CST_ICMS': '00', 'CST_PIS': '01', 'CST_COFINS': '01', 'Regime': 'Lucro Presumido', 'Valido': True},
    {'CFOP': '2101', 'CST_ICMS': '40', 'CST_PIS': '04', 'CST_COFINS': '04', 'Regime': 'Lucro Presumido', 'Valido': False},
    {'CFOP': '5103', 'CST_ICMS': '00', 'CST_PIS': '01', 'CST_COFINS': '01', 'Regime': 'Lucro Presumido', 'Valido': True},
    {'CFOP': '5901', 'CST_ICMS': '41', 'CST_PIS': '04', 'CST_COFINS': '04', 'Regime': 'Lucro Presumido', 'Valido': True},
    {'CFOP': '5902', 'CST_ICMS': '41', 'CST_PIS': '04', 'CST_COFINS': '04', 'Regime': 'Lucro Presumido', 'Valido': True},
    {'CFOP': '5910', 'CST_ICMS': '40', 'CST_PIS': '04', 'CST_COFINS': '04', 'Regime': 'Lucro Presumido', 'Valido': True},
    {'CFOP': '5949', 'CST_ICMS': '49', 'CST_PIS': '49', 'CST_COFINS': '49', 'Regime': 'Lucro Presumido', 'Valido': True},
    {'CFOP': '1101', 'CST_ICMS': '00', 'CST_PIS': '01', 'CST_COFINS': '01', 'Regime': 'Lucro Presumido', 'Valido': True},
    {'CFOP': '1202', 'CST_ICMS': '00', 'CST_PIS': '01', 'CST_COFINS': '01', 'Regime': 'Lucro Presumido', 'Valido': True},
    {'CFOP': '1910', 'CST_ICMS': '41', 'CST_PIS': '04', 'CST_COFINS': '04', 'Regime': 'Lucro Presumido', 'Valido': True},
    {'CFOP': '1949', 'CST_ICMS': '49', 'CST_PIS': '49', 'CST_COFINS': '49', 'Regime': 'Lucro Presumido', 'Valido': True},
    {'CFOP': '5152', 'CST_ICMS': '20', 'CST_PIS': '01', 'CST_COFINS': '01', 'Regime': 'Lucro Presumido', 'Valido': True},
])

def extrair_dados(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    ns = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

    return {
        'chave': root.findtext('.//ns:infNFe', namespaces=ns, default='N/A'),
        'cfop': root.findtext('.//ns:det/ns:prod/ns:CFOP', namespaces=ns, default='N/A'),
        'cst_icms': root.findtext('.//ns:ICMS00/ns:CST', namespaces=ns, default='N/A'),
        'cst_pis': root.findtext('.//ns:PIS/ns:PISAliq/ns:CST', namespaces=ns, default='N/A'),
        'cst_cofins': root.findtext('.//ns:COFINS/ns:COFINSAliq/ns:CST', namespaces=ns, default='N/A'),
        'regime': 'Lucro Presumido'
    }

def validar_dados(dados):
    match = TABELA_VALIDACAO[(TABELA_VALIDACAO['CFOP'] == dados['cfop']) &
                              (TABELA_VALIDACAO['CST_ICMS'] == dados['cst_icms']) &
                              (TABELA_VALIDACAO['CST_PIS'] == dados['cst_pis']) &
                              (TABELA_VALIDACAO['CST_COFINS'] == dados['cst_cofins']) &
                              (TABELA_VALIDACAO['Regime'] == dados['regime'])]
    if match.empty:
        return ['Combinacao CFOP + CSTs não encontrada na base. Verifique os parâmetros.']
    elif not match.iloc[0]['Valido']:
        return ['Combinacao inválida segundo tabela de validação fiscal.']
    return []

st.title("Validador Fiscal de XML - Lucro Presumido e Real")

uploaded_files = st.file_uploader("Envie um ou mais arquivos XML da NF-e:", accept_multiple_files=True, type="xml")

if uploaded_files:
    resultados = []
    for file in uploaded_files:
        dados = extrair_dados(file)
        inconsistencias = validar_dados(dados)
        dados['inconsistencias'] = "; ".join(inconsistencias) if inconsistencias else "OK"
        resultados.append(dados)

    df = pd.DataFrame(resultados)
    st.write("### Resultado da Validação")
    st.dataframe(df)

    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    st.download_button("📥 Baixar relatório em Excel", data=buffer,
                       file_name="relatorio_validacao_fiscal.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
