import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib
import os
from datetime import date

# Nome do arquivo do modelo com a data atual
nome_arquivo = f"treino-cpu-{date.today()}.pkl"

# Criar um DataFrame com os dados dos processadores
data = {
    "nome": [
        "Intel Atom Z3745",
        "Intel Atom Z3530",
        "Intel Atom N570",
        "Intel Celeron E1400",
    ],
    "nanometros": [22, 22, 45, 65],
    "ghz": [1.33 * 4, 1.33 * 4, 1.66 * 2, 2 * 2],  # Convertendo a string para um número
    "score": [15, 14, 13, 11],
    "bom": [1, 1, 1, 0],  # 1 para bom, 0 para não bom
}

# Converter para DataFrame
df = pd.DataFrame(data)

# Definir atributos e rótulos
X = df[["nanometros", "ghz", "score"]]  # Atributos
y = df["bom"]  # Rótulo

# Dividir os dados em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Verificar se o modelo já foi treinado e salvo
if os.path.exists(nome_arquivo):
    # Carregar o modelo existente
    model = joblib.load(nome_arquivo)
    print("Modelo carregado a partir do arquivo.")
else:
    # Criar e treinar o classificador
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)

    # Salvar o modelo treinado
    joblib.dump(model, nome_arquivo)
    print("Modelo treinado e salvo no arquivo.")

# Fazer previsões
predictions = model.predict(X_test)

# Avaliar o modelo
accuracy = accuracy_score(y_test, predictions)
print(f"Acurácia do modelo: {accuracy * 100:.2f}%")

# Testar com um novo processador
novo_processador = np.array([[22, 1.33 * 4, 14]])  # Exemplo: Intel Atom Z3530
resultado = model.predict(novo_processador)

if resultado[0] == 1:
    print("O processador é considerado bom.")
else:
    print("O processador não é considerado bom.")
