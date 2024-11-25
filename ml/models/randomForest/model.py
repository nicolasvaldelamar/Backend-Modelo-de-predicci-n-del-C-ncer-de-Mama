import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import json
import logging
import sys
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BreastCancerPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.base_path = Path(__file__).parent.parent.parent  # ml folder
        self.feature_names = [
            'Clump_Thickness', 'Uniformity_of_Cell_Size', 
            'Uniformity_of_Cell_Shape', 'Marginal_Adhesion',
            'Single_Epithelial_Cell_Size', 'Bare_Nuclei',
            'Bland_Chromatin', 'Normal_Nucleoli', 'Mitoses'
        ]

    def train_model(self):
        """Entrena el modelo con los datos proporcionados"""
        try:
            # Construir ruta al dataset
            data_path = Path(__file__).parent.parent.parent / 'data' / 'raw' / 'breast-cancer-wisconsin-with-headers.csv'
            logger.info(f"Iniciando entrenamiento con datos de {data_path}")
            
            # Cargar y preparar datos
            df = pd.read_csv(data_path)
            df = df.drop(columns=['Sample_code_number'])
            df = df.replace('?', pd.NA)
            df = df.dropna()

            # Separar features y target
            X = df[self.feature_names]
            y = df['Class']

            # Escalar características
            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)

            # Entrenar modelo
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            )
            self.model.fit(X_scaled, y)

            # Guardar modelo y scaler
            self.save_model()
            
            logger.info("Modelo entrenado y guardado exitosamente")
            
            # Calcular y mostrar métricas de importancia
            importances = self.get_feature_importance()
            logger.info("Importancia de características:")
            for feature, importance in importances.items():
                logger.info(f"{feature}: {importance:.4f}")
            
        except Exception as e:
            logger.error(f"Error en entrenamiento: {str(e)}")
            raise

    def predict(self, features):
        """Realiza una predicción"""
        try:
            if self.model is None or self.scaler is None:
                self.load_model()

            # Validar features
            if len(features) != len(self.feature_names):
                raise ValueError("Se requieren 9 características")

            # Preparar datos
            features_df = pd.DataFrame([features], columns=self.feature_names)
            features_scaled = self.scaler.transform(features_df)

            # Realizar predicción
            prediction = self.model.predict(features_scaled)[0]
            probabilities = self.model.predict_proba(features_scaled)[0]

            # Obtener importancia de características
            feature_importance = self.get_feature_importance()

            return {
                "prediction": int(prediction),
                "tumor_type": "benigno" if prediction == 2 else "maligno",
                "probability": float(max(probabilities)),
                "probabilities": {
                    "benigno": float(probabilities[0]),
                    "maligno": float(probabilities[1])
                },
                "feature_importance": feature_importance
            }

        except Exception as e:
            logger.error(f"Error en predicción: {str(e)}")
            raise

    def save_model(self):
        """Guarda el modelo y el scaler"""
        try:
            model_dir = self.base_path / 'data' / 'models'
            model_dir.mkdir(parents=True, exist_ok=True)
            
            joblib.dump(self.model, model_dir / 'model.pkl')
            joblib.dump(self.scaler, model_dir / 'scaler.pkl')
            logger.info(f"Modelo guardado en {model_dir}")
        except Exception as e:
            logger.error(f"Error guardando modelo: {str(e)}")
            raise

    def load_model(self):
        """Carga el modelo y el scaler"""
        try:
            model_dir = self.base_path / 'data' / 'models'
            self.model = joblib.load(model_dir / 'model.pkl')
            self.scaler = joblib.load(model_dir / 'scaler.pkl')
            logger.info(f"Modelo cargado desde {model_dir}")
        except Exception as e:
            logger.error(f"Error cargando modelo: {str(e)}")
            raise

    def get_feature_importance(self):
        """Obtiene la importancia de las características"""
        if self.model is None:
            self.load_model()
        return dict(zip(self.feature_names, self.model.feature_importances_))

def main():
    """Función principal para ejecución desde línea de comandos"""
    try:
        predictor = BreastCancerPredictor()
        
        if len(sys.argv) > 1:
            # Modo predicción
            logger.info("Modo predicción")
            features = [float(x) for x in sys.argv[1].split(',')]
            result = predictor.predict(features)
            print(json.dumps(result))
        else:
            # Modo entrenamiento
            logger.info("Modo entrenamiento")
            predictor.train_model()
            logger.info("Entrenamiento completado exitosamente")
            
    except Exception as e:
        logger.error(f"Error en ejecución: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 