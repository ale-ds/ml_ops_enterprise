import os
import sys
import mlflow
import pandas as pd
import numpy as np
from mlflow.tracking import MlflowClient

# Ajusta o path para importar módulos personalizados
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(project_root)

# Importando nossos módulos
from src.data_prep.extractor import read_config

def test_model_integrity():
    """
    Valida o contrato do modelo.
    Busca o modelo mais recente do Model Registry e checa se a entrada/saída
    estão conforme o esperado.
    """
    # Adicionado para garantir que o teste use o backend de banco de dados correto
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    
    # 1. Carregar Configurações de Treino (apenas para ler hiperparâmetros)
    model_config = read_config('config/model/random_forest.yaml')

    # Nome do modelo registrado, conforme definido em 'random_forest.yaml'
    model_name = model_config['registered_model_name']
    
    # 1. Conectar ao MLflow e buscar a última versão do modelo
    client = MlflowClient()
    
    # Busca a última versão do modelo usando o método recomendado 'search_model_versions'
    try:
        versions = client.search_model_versions(f"name='{model_name}'")
        if not versions:
            raise IndexError  # Lança para ser pego pelo bloco except

        # Ordena as versões pela 'version' (convertida para int) em ordem decrescente
        latest_version_info = sorted(versions, key=lambda v: int(v.version), reverse=True)[0]
        model_version = latest_version_info.version
        model_uri = f"models:/{model_name}/{model_version}"
        print(f"Modelo encontrado: {model_uri}")
    except IndexError:
        raise AssertionError(f"Nenhum modelo com o nome '{model_name}' foi encontrado no MLflow Registry.")

    # 2. Carregar o modelo
    try:
        model = mlflow.pyfunc.load_model(model_uri)
        print(f"Modelo {model_uri} carregado com sucesso.")
    except Exception as e:
        raise AssertionError(f"Falha ao carregar o modelo da URI '{model_uri}'. Erro: {e}")

    # 3. Criar uma amostra de dados (payload) que respeita o contrato de entrada
    # As colunas são baseadas em 'config/data/raw.yaml'
    feature_columns = [
        "MedInc_log", "HouseAge", "AveRooms", "AveBedrms", 
        "Population", "AveOccup", "Latitude", "Longitude"
    ]
    # Usamos uma linha de dados fictícios para o teste
    sample_data = pd.DataFrame([[41.0, 6.9841, 1.0238, 322.0, 2.5555, 37.88, -122.23, 2.2327]], columns=feature_columns)
    
    print("Amostra de dados para predição:")
    print(sample_data)

    # 4. Realizar uma predição e validar a saída
    try:
        prediction = model.predict(sample_data)
        print(f"Predição realizada com sucesso. Resultado: {prediction}")
    except Exception as e:
        raise AssertionError(f"Falha durante a predição do modelo. Erro: {e}")

    # 5. Garantir que o contrato de saída foi respeitado
    assert isinstance(prediction, np.ndarray), "A predição deve ser um numpy array."
    assert len(prediction) == 1, "O número de predições deve ser igual ao de linhas de entrada (1)."
    assert np.issubdtype(prediction.dtype, np.number), "O tipo de dado da predição deve ser numérico."

    print("Contrato de Entrada/Saída do modelo validado com sucesso!")

