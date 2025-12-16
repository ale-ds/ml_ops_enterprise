import numpy as np
import pandas as pd

def apply_log_transformation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica a transformação logarítmica (log(x+1)) na feature 'MedInc' 
    para reduzir a inclinação (skew) da distribuição.
    """
    # ⚠️ É crucial trabalhar em uma cópia para evitar SettingWithCopyWarning
    df = df.copy()
    
    # np.log1p é o log(x+1), seguro para valores próximos de zero
    df['MedInc_log'] = np.log1p(df['MedInc']) 
    
    # Remove a feature original
    df = df.drop(columns=['MedInc'])
    
    return df

def feature_engineering_pipeline(X: pd.DataFrame) -> pd.DataFrame:
    """
    Orquestra todas as etapas de Feature Engineering que devem ser aplicadas aos dados.
    """
    # 1. Aplica a transformação logarítmica
    X = apply_log_transformation(X)
    
    print("✨ Transformação de Features: Log aplicada em MedInc.")
    return X