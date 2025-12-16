import pandas as pd
from src.data_prep.extractor import read_config

def validate_schema(df: pd.DataFrame, is_target=False):
    """
    Checa se o DataFrame contém todas as colunas esperadas e no tipo correto,
    prevenindo o Schema Skew.
    """
    # 1. Carrega as features esperadas do arquivo YAML
    config = read_config('config/data/raw.yaml')
    expected_features = config['features']
    target = config['target_feature']

    # 2. Checagem de Colunas Faltantes
    missing_cols = [col for col in expected_features if col not in df.columns]
    if missing_cols:
        raise ValueError(f"❌ Erro de Schema: Colunas faltantes: {missing_cols}")

    # 3. Checagem da Coluna Target (se aplicável)
    if not is_target and target not in df.columns:
        raise ValueError(f"❌ Erro de Schema: Coluna target '{target}' ausente.")
    
    # 4. Checagem de Tipo Simplificada (Garantindo que são numéricas)
    for col in expected_features:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise TypeError(f"❌ Erro de Tipo: Coluna '{col}' não é numérica.")

    # A validação de sucesso é silenciosa, mas essencial
    return True