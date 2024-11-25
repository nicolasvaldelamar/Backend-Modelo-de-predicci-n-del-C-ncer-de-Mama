const predictionService = require('../services/predictionService');
const metricsService = require('../services/metricsService');

class PredictionController {
    async predict(req, res) {
        try {
            const { features } = req.body;
            const prediction = await predictionService.predict(features);
            
            // Guardar la predicción en la base de datos
            await metricsService.savePrediction({
                features,
                ...prediction
            });

            res.json(prediction);
        } catch (error) {
            res.status(500).json({
                error: 'Error al procesar la predicción',
                details: error.message
            });
        }
    }

    async getMetrics(req, res) {
        try {
            const metrics = await metricsService.getMetrics();
            res.json(metrics);
        } catch (error) {
            res.status(500).json({
                error: 'Error al obtener métricas',
                details: error.message
            });
        }
    }
}

module.exports = new PredictionController(); 