import pandas as pd

def validation_clean_data(df: pd.DataFrame, column_date: list = None, format_date: str = None) -> tuple:
    """
    Valida y limpia un DataFrame: elimina duplicados, nulos y corrige formato de fechas.

    Args:
        df (pd.DataFrame): DataFrame a procesar.
        column_date (list): Lista de columnas a convertir a datetime.
        format_date (str): Formato de fecha (opcional), e.g., '%Y-%m-%d'.

    Returns:
        tuple: (df_limpio: pd.DataFrame, resumen_dict: dict)
    """
    resumen = {}
    df = df.copy()  # Evita modificar el DataFrame original

    # 1. Eliminar duplicados por columna
    duplicados_col = {}
    for col in df.columns:
        duplicados = df[col].duplicated(keep='first')
        count = duplicados.sum()
        if count > 0:
            df.loc[duplicados, col] = pd.NA
            duplicados_col[col] = int(count)
    resumen["duplicados_en_columnas_eliminados"] = duplicados_col

    # 2. Eliminar filas duplicadas
    filas_duplicadas = df.duplicated().sum()
    df = df.drop_duplicates()
    resumen["filas_duplicadas_eliminadas"] = int(filas_duplicadas)

    # 3. Eliminar filas con valores nulos
    nulos_totales = df.isnull().sum().sum()
    resumen["valores_nulos_eliminados"] = int(nulos_totales)
    df = df.dropna()

    # 4. Corregir formato de columnas de fecha
    errores_fecha = {}
    if column_date:
        for col in column_date:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], format=format_date, errors='coerce')
                errores = df[col].isnull().sum()
                if errores > 0:
                    errores_fecha[col] = int(errores)
            else:
                errores_fecha[col] = "Columna no encontrada"
        resumen["errores_formato_fecha"] = errores_fecha

    return df, resumen
