from bd_base import my_bd
import pandas as pd
import numpy as np
import pickle
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier


class train_in:

    def treinando_ia(self):
        p1 = my_bd
        data = p1.le_bd()

        df = pd.DataFrame(data, columns=['HR_MEDICAO', 'CHUVA', 'PRE_MAX', 'PRE_MIN', 'PTO_INS',
                                         'TEM_MAX', 'TEM_MIN', 'PTO_MAX', 'PTO_MIN', 'UMD_MAX', 'UMD_MIN', 'VEN_DIR',
                                         'VEN_RAJ', 'VEN_VEL', 'DATA', 'BAIRRO', 'LOCAL', 'ARD'])

        np.unique(df['ARD'], return_counts=True)
        X_base = df.iloc[:, 0:17].values
        y_base = df.iloc[:,17].values


        scaler_df = StandardScaler()
        X_base = scaler_df.fit_transform((X_base))



        X_base_treinamento, X_base_teste, y_base_treinamento, y_base_teste = train_test_split(X_base, y_base, test_size = 0.30, random_state= 0)


        with open('base.pkl', mode ='wb') as f:
            pickle.dump([X_base_treinamento, y_base_treinamento, X_base_teste, y_base_teste], f)


        with open('base.pkl', mode='rb') as f:
            X_base_treinamento, y_base_treinamento, X_base_teste, y_base_teste = pickle.load(f)

        random_forest = RandomForestClassifier(n_estimators=50, criterion='entropy', random_state=0)
        random_forest.fit(X_base_treinamento, y_base_treinamento)

        previsoes_random = random_forest.predict(X_base_teste)

        joblib.dump(random_forest, 'ia03.pkl')
        from sklearn.metrics import accuracy_score, classification_report
        c = accuracy_score(y_base_teste, previsoes_random)


        return print(c)
