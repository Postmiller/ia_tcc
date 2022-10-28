from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import datetime
from datetime import datetime
import pytz
import requests
import mysql.connector

app = FastAPI()


class Produto(BaseModel):
    bairro: int
    local: int
    valueWater: int


@app.post('/produtos')
def produtos(produto: Produto):
    hoje = datetime.now(pytz.timezone('America/Sao_Paulo'))
    dia = datetime.strftime(hoje, "%d")
    mes = datetime.strftime(hoje, "%m")
    ano = datetime.strftime(hoje, "%y")
    hora = datetime.strftime(hoje, "%H") + '00'

    api = 'https://apitempo.inmet.gov.br/estacao/20{2}-{1}-{0}/20{2}-{1}-{0}/A771'.format(dia, mes, ano)
    response = requests.get(api)
    data = response.json()
    df = pd.DataFrame(data)
    df1 = df[['HR_MEDICAO', 'CHUVA', 'PRE_MAX', 'PRE_MIN', 'PTO_INS', 'TEM_MAX', 'TEM_MIN',
              'PTO_MAX', 'PTO_MIN', 'UMD_MAX', 'UMD_MIN', 'VEN_DIR', 'VEN_RAJ', 'VEN_VEL']]
    df1['DATA'] = '{0}{1}20{2}'.format(dia, mes, ano)
    df1['BAIRRO'] = produto.bairro
    df1['LOCAL'] = produto.local

    teste = df1.loc[df1['HR_MEDICAO'] == hora]
    s_colum = teste.pop('DATA')
    t_colum = teste.pop('BAIRRO')
    q_colum = teste.pop('LOCAL')
    teste.insert(1, 'DATA', s_colum)
    teste.insert(2, 'BAIRRO', t_colum)
    teste.insert(3, 'LOCAL', q_colum)

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='5747',
        database='bd_tcc'
    )

    cursor = conexao.cursor()
    comando = f'INSERT INTO registros (HR_MEDICAO, CHUVA, PRE_MAX, PRE_MIN, PTO_INS, TEM_MAX, TEM_MIN, PTO_MAX, PTO_MIN, UMD_MAX, UMD_MIN, VEN_DIR, VEN_RAJ, VEN_VEL, DATA, ARD, BAIRRO, LOCAL) VALUES ({teste.iloc[0, 0]}, {teste.iloc[0, 4]}, {teste.iloc[0, 5]}, {teste.iloc[0, 6]}, {teste.iloc[0, 7]}, {teste.iloc[0, 8]}, {teste.iloc[0, 9]}, {teste.iloc[0, 10]}, {teste.iloc[0, 11]}, {teste.iloc[0, 12]}, {teste.iloc[0, 13]}, {teste.iloc[0, 14]}, {teste.iloc[0, 15]}, {teste.iloc[0, 16]}, {teste.iloc[0, 1]}, {produto.valueWater}, {teste.iloc[0, 2]}, {teste.iloc[0, 3]})'
    cursor.execute(comando)

    conexao.commit()

    cursor.close()
    conexao.close()

    ia = joblib.load('ia02.pkl')
    rec = ia.predict(teste)
    return {f'{rec}'}
