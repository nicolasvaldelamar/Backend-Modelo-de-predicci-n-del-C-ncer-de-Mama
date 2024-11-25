import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import logging

logger = logging.getLogger(__name__)

class FeatureEngineer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = [
            'Clump_Thickness', 'Uniformity_of_Cell_Size', 
            'Uniformity_of_Cell_Shape', 'Marginal_Adhesion',
            'Single_Epithelial_Cell_Size', 'Bare_Nuclei',
            'Bland_Chromatin', 'Normal_Nucleoli', 'Mitoses'
        ]
        
    def create_features(self, df):
        """
        Crea y transforma características para el modelo
        
        Args:
            df (pd.DataFrame): DataFrame limpio
            
        Returns:
            tuple: (X, y) features y target procesados
        """
        try:
            logger.info("Iniciando ingeniería de características...")
            
            # Separar features y target
            X = df[self.feature_names]
            y = df['Class']
            
            # Crear características adicionales
            X = self._add_interaction_features(X)
            
            # Escalar características
            X_scaled = self.scaler.fit_transform(X)
            
            logger.info(f"Procesamiento de características completado. Shape: {X_scaled.shape}")
            
            return X_scaled, y
            
        except Exception as e:
            logger.error(f"Error en feature engineering: {str(e)}")
            raise
            
    def _add_interaction_features(self, X):
        """
        Añade características de interacción entre variables importantes
        """
        X = X.copy()
        
        # Interacción entre tamaño y forma de células
        X['Size_Shape_Interaction'] = X['Uniformity_of_Cell_Size'] * X['Uniformity_of_Cell_Shape']
        
        # Ratio de características nucleares
        X['Nuclear_Ratio'] = X['Bare_Nuclei'] / X['Normal_Nucleoli'].replace(0, 1)
        
        return X
        
    def transform_prediction_features(self, features):
        """
        Transforma características para predicción
        """
        try:
            features_df = pd.DataFrame([features], columns=self.feature_names)
            features_df = self._add_interaction_features(features_df)
            return self.scaler.transform(features_df)
        except Exception as e:
            logger.error(f"Error transformando características: {str(e)}")
            raise 