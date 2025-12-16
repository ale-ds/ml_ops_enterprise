import os
import sys
import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error

# Ajusta o path para importar módulos personalizados
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(project_root)

# Importando nossos módulos
from src.data_prep.extractor import load_and_split_data, read_config
from src.features.transformer import feature_engineering_pipeline
from src.validation.schema import validate_schema

def train_pipeline():
    # O URI já vem injetado pelo Makefile via variável de ambiente.
    # 1. Carregar Configurações de Treino (apenas para ler hiperparâmetros)
    model_config = read_config('config/model/random_forest.yaml')
    
    # O experimento já foi definido no comando 'mlflow run' do Makefile.
    # O script já nasce dentro do contexto correto.
    print(f"Logando no Tracking URI ativo: {mlflow.get_tracking_uri()}")

    # 3. Carregar, Dividir e Validar Dados
    X_train_raw, X_test_raw, y_train, y_test = load_and_split_data()
    
    # Quality Gate de Dados
    validate_schema(pd.concat([X_train_raw, X_test_raw, y_train, y_test], axis=0))

    # 4. Feature Engineering
    X_train = feature_engineering_pipeline(X_train_raw)
    X_test = feature_engineering_pipeline(X_test_raw)
    
    # 5. Treinamento
    params = model_config['params']
    model = RandomForestRegressor(**params)
    model.fit(X_train, y_train)
    
    # 6. Avaliação
    predictions = model.predict(X_test)
    rmse = root_mean_squared_error(y_test, predictions)
    
    # 7. LOGGING MLFLOW
    # O MLflow detecta automaticamente o ID da run ativa criado pelo Makefile
    mlflow.log_params(params)
    mlflow.log_metric("rmse", rmse)
    
    # Log de artefatos de configuração para reprodutibilidade
    mlflow.log_artifact('config/model/random_forest.yaml', "config")
    mlflow.log_artifact('config/data/raw.yaml', "config")
    
    mlflow.sklearn.log_model(
        sk_model=model,
        name="model",
        input_example=X_train.iloc[:1],
        registered_model_name=model_config['registered_model_name']
    )
    print(f"✅ Treinamento concluído. RMSE: {rmse:.4f}")

if __name__ == "__main__":
    train_pipeline()