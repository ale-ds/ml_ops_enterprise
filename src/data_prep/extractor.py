# src/data_prep/extractor.py

import yaml
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

def read_config(path: str):
    """Lê e retorna o conteúdo de um arquivo YAML."""
    try:
        with open(path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Erro ao ler arquivo de configuração em {path}: {e}")
        return None

def load_and_split_data():
    """
    Carrega o dataset California Housing e aplica o split de treino/teste,
    lendo os parâmetros de split de um arquivo de configuração.
    """
    # 1. Leitura da Configuração de Split
    data_config = read_config('config/data/raw.yaml')
    if not data_config:
        raise FileNotFoundError("Falha ao carregar a configuração de dados.")
    
    test_size = data_config['split']['test_size']
    random_state = data_config['split']['random_state']

    # 2. Carregamento do Dataset
    # Em um projeto real, aqui você conectaria ao S3/DB/Feature Store
    housing = fetch_california_housing(as_frame=True)
    X = housing.data
    y = housing.target

    # 3. Split de Dados
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    print(f"Dados carregados e divididos: Treino={len(X_train)}, Teste={len(X_test)}")
    return X_train, X_test, y_train, y_test

if __name__ == '__main__':
    # Exemplo de execução para verificar a função
    load_and_split_data()