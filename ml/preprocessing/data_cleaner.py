import pandas as pd
import numpy as np
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self):
        self.columns_to_drop = ['Sample_code_number']
        self.target_column = 'Class'
        
    def clean_dataset(self, df):
        """
        Limpia el dataset aplicando varias transformaciones
        
        Args:
            df (pd.DataFrame): DataFrame original
            
        Returns:
            pd.DataFrame: DataFrame limpio
        """
        try:
            logger.info("Iniciando limpieza de datos...")
            
            # Hacer una copia para no modificar el original
            df_clean = df.copy()
            
            # Eliminar columnas no necesarias
            df_clean = df_clean.drop(columns=self.columns_to_drop)
            
            # Reemplazar valores faltantes
            df_clean = df_clean.replace('?', pd.NA)
            
            # Eliminar filas con valores faltantes
            df_clean = df_clean.dropna()
            
            # Convertir todas las columnas numéricas
            numeric_columns = df_clean.columns.drop(self.target_column)
            df_clean[numeric_columns] = df_clean[numeric_columns].apply(pd.to_numeric)
            
            # Validar rangos
            for col in numeric_columns:
                mask = (df_clean[col] >= 1) & (df_clean[col] <= 10)
                df_clean = df_clean[mask]
            
            logger.info(f"Limpieza completada. Filas restantes: {len(df_clean)}")
            
            return df_clean
            
        except Exception as e:
            logger.error(f"Error en la limpieza de datos: {str(e)}")
            raise 