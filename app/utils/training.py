import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
from app.upgradify.settings import MIN_GPU_SCORE
import datetime

print("Hoje é", datetime.date.today())
data = {
    "Modelo": [
        "Asus HD 6570 2GB",
        "MSI GeForce GT 1030 2GHD4 LP OC Gaming",
        "Gigabyte HD 6450 1GB Rev. 2",
        "NVIDIA GeForce GTX 1050 Ti",
        "AMD Radeon RX 570",
        "MSI GeForce GTX 1660",
        "NVIDIA GeForce RTX 2060",
        "AMD Radeon RX 580",
        "NVIDIA GeForce GTX 1080",
        "ASUS ROG Strix GTX 1070",
        "Gigabyte GeForce GTX 1650",
        "EVGA GeForce RTX 3070",
        "NVIDIA GeForce RTX 3080",
        "AMD Radeon RX 6900 XT",
        "NVIDIA GeForce GTX 960",
        "AMD Radeon RX 560",
    ],
    "Preço (R$)": [
        None,
        629,
        None,
        850,
        1200,
        1500,
        2000,
        1800,
        2500,
        2400,
        800,
        3500,
        4000,
        6000,
        500,
        700,
    ],
    "TFLOPS": [
        0.62,
        1.1,
        0.24,
        2.1,
        5.0,
        5.5,
        7.2,
        6.5,
        8.5,
        8.0,
        3.0,
        15.0,
        20.0,
        23.0,
        4.0,
        2.5,
    ],
    "Memória (GB)": [
        2,
        2,
        1,
        4,
        8,
        6,
        8,
        8,
        8,
        8,
        4,
        8,
        10,
        16,
        4,
        2,
    ],
    "GPixels (GPixel/s)": [
        5.2,
        22.88,
        3,
        48,
        128,
        150,
        200,
        180,
        250,
        230,
        120,
        250,
        300,
        350,
        90,
        30,
    ],
    "Pontuação": [
        31,
        30,
        30,
        70,
        85,
        90,
        95,
        90,
        99,
        97,
        75,
        99,
        100,
        110,
        60,
        50,
    ],
}

# Criando o DataFrame
df = pd.DataFrame(data)

# Definindo a classificação com base na pontuação
df["Classificação"] = df["Pontuação"].apply(lambda x: 1 if x > MIN_GPU_SCORE else 0)

# Selecionando as características e a variável alvo
X = df[["Preço (R$)", "TFLOPS", "Memória (GB)", "GPixels (GPixel/s)", "Pontuação"]]
y = df["Classificação"]

# Preenchendo valores ausentes (se houver)
X.fillna(X.mean(), inplace=True)

# Caminho do arquivo onde o modelo será salvo
model_filename = f"random_forest_model_gpu_{str(datetime.date.today())}.joblib"

# Verifica se o modelo já foi salvo, caso contrário, treina e salva
try:
    # Carrega o modelo salvo
    model = joblib.load(model_filename)
    print("Modelo carregado do arquivo.")
except FileNotFoundError:
    # Dividindo os dados em conjuntos de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Treinando o modelo
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Salvando o modelo em um arquivo
    joblib.dump(model, model_filename)
    print("Modelo treinado e salvo no arquivo.")

    # Fazendo previsões e avaliando o modelo
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=["Não Boa", "Boa"]))

# Exemplo de previsão com novos dados
novo_dado = pd.DataFrame(
    {
        "Preço (R$)": [500],
        "TFLOPS": [1.0],
        "Memória (GB)": [4],
        "GPixels (GPixel/s)": [20],
        "Pontuação": [55],  # Nova pontuação
    }
)

# Prevendo a classificação
classificacao_nova = model.predict(novo_dado)
print(
    "Classificação da nova placa:", "Boa" if classificacao_nova[0] == 1 else "Não Boa"
)

# Treinamento da CPU

model_filename = f"random_forest_model_cpu_{str(datetime.date.today())}.joblib"
