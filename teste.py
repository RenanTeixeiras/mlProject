import pandas as pd
import random
from tqdm import tqdm

df = pd.read_csv(r'https://raw.githubusercontent.com/infoslack/ml-book-exemplos/main/data/venda-de-carros.csv')


df['Preco'] = list(map(lambda x: x.replace('R$ ','').replace('.00','').replace(',','.'), df['Preco']))


fabricantes = list(set(df['Fabricante']))
cores = list(set(df['Cor']))
fabricantes_ = list(df['Fabricante'])
cores_ = list(df['Cor'])
quilometragem = list(df['Quilometragem'])
quilometragem_ = list(df['Quilometragem'])
portas = list(df['Portas'])
portas_ = list(df['Portas'])
preco = list(df['Preco'])
preco_ = list(df['Preco'])


cada_fabricante = list(set(df['Fabricante']))
cada_cor = list(set(df['Cor']))

dict_fabricante = {
    'FABRICANTE':cada_fabricante,
    'N_FABRICANTE': [num +1 for num in range(len(list(cada_fabricante)))]
}

dict_cor = {
    'COR': cada_cor,
    'N_COR' : [num +1 for num in range(len(list(cada_cor)))]
}

df_fabricante = pd.DataFrame(dict_fabricante)
df_cor = pd.DataFrame(dict_cor)

pd.DataFrame(dict_fabricante).to_excel("fabricantes.xlsx", index=False)
pd.DataFrame(dict_cor).to_excel("cores.xlsx", index=False)



for i in tqdm(range(100000)):
    fabricantes_.append(random.choice(fabricantes))
    cores_.append(random.choice(cores))
    quilometragem_.append(random.randint(11179,213095))
    preco_.append(random.choice(preco))
    portas_.append(4)


dict_dataframe = pd.DataFrame({
    "FABRICANTE":fabricantes_,
    "CORES":cores_,
    "QUILOMETRAGEM": quilometragem_,
    "PORTAS": portas_,
    "PRECO": preco_,
})


dict_dataframe = pd.merge(dict_dataframe,df_cor, how='left',  left_on='CORES', right_on='COR')

dict_dataframe = pd.merge(dict_dataframe, df_fabricante, how='left', left_on = 'FABRICANTE', right_on= 'FABRICANTE')


dict_dataframe.to_excel('resultado.xlsx', index=False)



features = ['N_COR', 'N_FABRICANTE', 'QUILOMETRAGEM', 'PORTAS']

X = dict_dataframe[features]
y = dict_dataframe.PRECO


from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state = 35)

car_model = DecisionTreeRegressor()
print(f'DADOS TREINO: \n{train_X.head()}')
print(f'DADOS TESTE: \n{train_y.head()}')

car_model.fit(train_X.head(), train_y.head())

# get predicted prices on validation data
val_predictions = car_model.predict(val_X.head())
print(f'PREVISOES: \n{val_predictions}')
print(mean_absolute_error(val_y.head(), val_predictions))


