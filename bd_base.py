import mysql.connector

class my_bd:

    @staticmethod
    def conexao_db():
        global conexao, cursor
        conexao = mysql.connector.connect(
            host='localhost',
            user='root',
            password='5747',
            database='bd_tcc'
        )

        cursor = conexao.cursor()

    @staticmethod
    def desconexao():
        cursor.close()
        conexao.close()

    @staticmethod
    def gravar_db(teste, valueWater):
        my_bd.conexao_db()

        comando = f'INSERT INTO registros (HR_MEDICAO, CHUVA, PRE_MAX, PRE_MIN, PTO_INS, TEM_MAX, TEM_MIN, PTO_MAX, PTO_MIN, UMD_MAX, UMD_MIN, VEN_DIR, VEN_RAJ, VEN_VEL, DATA, ARD, BAIRRO, LOCAL) VALUES (' \
                  f'{teste.iloc[0, 0]}, {teste.iloc[0, 4]}, {teste.iloc[0, 5]}, {teste.iloc[0, 6]}, {teste.iloc[0, 7]}, {teste.iloc[0, 8]}, {teste.iloc[0, 9]}, {teste.iloc[0, 10]}, {teste.iloc[0, 11]}, {teste.iloc[0, 12]}, ' \
                  f'{teste.iloc[0, 13]}, {teste.iloc[0, 14]}, {teste.iloc[0, 15]}, {teste.iloc[0, 16]}, {teste.iloc[0, 1]}, {valueWater}, {teste.iloc[0, 2]}, {teste.iloc[0, 3]})'
        cursor.execute(comando)

        conexao.commit()

        my_bd.desconexao()

    @staticmethod
    def le_bd():
        my_bd.conexao_db()

        comando = f'SELECT HR_MEDICAO, CHUVA, PRE_MAX, PRE_MIN, PTO_INS, TEM_MAX, TEM_MIN, PTO_MAX, PTO_MIN, UMD_MAX, UMD_MIN, VEN_DIR, VEN_RAJ, VEN_VEL, DATA, BAIRRO, LOCAL, ARD FROM registros'
        cursor.execute(comando)
        resultado_db = cursor.fetchall()

        my_bd.desconexao()

        return resultado_db
