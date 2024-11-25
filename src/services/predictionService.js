const { spawn } = require('child_process');
const path = require('path');
const config = require('../config/config');
const logger = require('../utils/logger');
const PredictionHistory = require('../models/PredictionHistory');

class PredictionService {
    constructor() {
        this.modelPath = path.join(__dirname, '../../ml/models/randomForest/model.py');
    }

    async predict(features) {
        try {
            const prediction = await this._executePythonModel(features);
            await this._savePredictionHistory(features, prediction);
            return prediction;
        } catch (error) {
            logger.error('Error in prediction service:', error);
            throw error;
        }
    }

    async _executePythonModel(features) {
        return new Promise((resolve, reject) => {
            const pythonProcess = spawn('python', [
                this.modelPath,
                features.join(',')
            ]);

            let result = '';
            let error = '';

            pythonProcess.stdout.on('data', (data) => {
                result += data.toString();
            });

            pythonProcess.stderr.on('data', (data) => {
                error += data.toString();
            });

            pythonProcess.on('close', (code) => {
                if (code !== 0) {
                    logger.error(`Python process exited with code ${code}`);
                    return reject(new Error(`Error en el modelo: ${error}`));
                }

                try {
                    const prediction = JSON.parse(result);
                    resolve(prediction);
                } catch (e) {
                    reject(new Error('Error al procesar la respuesta del modelo'));
                }
            });
        });
    }

    async _savePredictionHistory(features, prediction) {
        try {
            const history = new PredictionHistory({
                features,
                prediction: prediction.prediction,
                tumorType: prediction.tumor_type,
                probability: prediction.probability,
                timestamp: new Date()
            });

            await history.save();
            logger.info('Prediction saved to history');
        } catch (error) {
            logger.error('Error saving prediction history:', error);
        }
    }

    async getPredictionHistory(filters = {}) {
        try {
            const history = await PredictionHistory.find(filters)
                .sort({ timestamp: -1 })
                .limit(100);
            return history;
        } catch (error) {
            logger.error('Error fetching prediction history:', error);
            throw error;
        }
    }

    async getModelMetrics() {
        try {
            const pythonProcess = spawn('python', [
                path.join(__dirname, '../../ml/utils/metrics.py')
            ]);

            return new Promise((resolve, reject) => {
                let result = '';
                let error = '';

                pythonProcess.stdout.on('data', (data) => {
                    result += data.toString();
                });

                pythonProcess.stderr.on('data', (data) => {
                    error += data.toString();
                });

                pythonProcess.on('close', (code) => {
                    if (code !== 0) {
                        return reject(new Error(error));
                    }
                    resolve(JSON.parse(result));
                });
            });
        } catch (error) {
            logger.error('Error getting model metrics:', error);
            throw error;
        }
    }
}

module.exports = new PredictionService(); 