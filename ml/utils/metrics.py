import joblib
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, confusion_matrix
)
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelMetrics:
    def __init__(self, model_path, test_data_path):
        self.model = joblib.load(model_path)
        self.test_data = np.load(test_data_path)
        
    def calculate_metrics(self):
        """Calcula todas las métricas del modelo"""
        try:
            X_test = self.test_data['X_test']
            y_test = self.test_data['y_test']
            
            # Realizar predicciones
            y_pred = self.model.predict(X_test)
            y_pred_proba = self.model.predict_proba(X_test)[:, 1]
            
            # Calcular métricas
            metrics = {
                'accuracy': float(accuracy_score(y_test, y_pred)),
                'precision': float(precision_score(y_test, y_pred, average='weighted')),
                'recall': float(recall_score(y_test, y_pred, average='weighted')),
                'f1': float(f1_score(y_test, y_pred, average='weighted')),
                'roc_auc': float(roc_auc_score(y_test, y_pred_proba)),
                'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            raise
            
    def get_feature_importance(self):
        """Obtiene la importancia de las características"""
        try:
            feature_importance = self.model.feature_importances_
            return {
                'feature_importance': feature_importance.tolist()
            }
        except Exception as e:
            logger.error(f"Error getting feature importance: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        model_path = Path(__file__).parent.parent / 'data/models/model.pkl'
        test_data_path = Path(__file__).parent.parent / 'data/processed/test_data.npz'
        
        metrics_calculator = ModelMetrics(model_path, test_data_path)
        
        # Calcular todas las métricas
        metrics = metrics_calculator.calculate_metrics()
        feature_importance = metrics_calculator.get_feature_importance()
        
        # Combinar resultados
        results = {**metrics, **feature_importance}
        
        # Imprimir resultados como JSON
        print(json.dumps(results))
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        sys.exit(1) 