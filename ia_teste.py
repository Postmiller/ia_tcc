import datetime
from datetime import datetime
import pytz
import requests
import pandas as pd
import joblib
from bd_base import my_bd


class chamar_ia:

    def __init__(self, bairro, local, vWater):
        self.bairro = bairro
        self.local = local
        self.vWater = vWater

        global dia, mes, ano, hora
        day_now = datetime.now(pytz.timezone('America/Sao_Paulo'))
        dia = datetime.strftime(day_now, "%d")
        mes = datetime.strftime(day_now, "%m")
        ano = datetime.strftime(day_now, "%y")
        hora = datetime.strftime(day_now, "%H") + '00'

    @staticmethod
    def req_site():
        url = "https://apitempo.inmet.gov.br/estacao/20{2}-{1}-{0}/20{2}-{1}-{0}/A771".format(dia, mes, ano)
        response = requests.get(url)
        data = response.json()
        return data

    def df_base(self):
        df = pd.DataFrame(chamar_ia.req_site())
        df1 = df[['HR_MEDICAO', 'CHUVA', 'PRE_MAX', 'PRE_MIN', 'PTO_INS', 'TEM_MAX', 'TEM_MIN',
                  'PTO_MAX', 'PTO_MIN', 'UMD_MAX', 'UMD_MIN', 'VEN_DIR', 'VEN_RAJ', 'VEN_VEL']]
        teste = df1.loc[df1['HR_MEDICAO'] == hora]
        teste = teste.assign(DATA=[f'{dia}{mes}20{ano}'],
                             BAIRRO=[self.bairro],
                             LOCAL=[self.local])

        s_colum = teste.pop('DATA')
        t_colum = teste.pop('BAIRRO')
        q_colum = teste.pop('LOCAL')
        teste.insert(1, 'DATA', s_colum)
        teste.insert(2, 'BAIRRO', t_colum)
        teste.insert(3, 'LOCAL', q_colum)

        #connect = bd_base()
        #connect.gravar_db(teste, self.vWater)

        return teste

    def main(self):
        ia = joblib.load('ia02.pkl')

        rec = ia.predict(chamar_ia.df_base(self))

        return print('{0}'.format(rec))