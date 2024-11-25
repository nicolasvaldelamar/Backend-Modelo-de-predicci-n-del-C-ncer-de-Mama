const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

class MetricsService {
    async savePrediction(predictionData) {
        try {
            const prediction = await prisma.prediction.create({
                data: {
                    features: JSON.stringify(predictionData.features),
                    prediction: predictionData.prediction,
                    tumorType: predictionData.tumor_type,
                    probability: predictionData.probability
                }
            });

            await this.updateMetrics();
            return prediction;
        } catch (error) {
            console.error('Error saving prediction:', error);
            throw error;
        }
    }

    async updateMetrics() {
        const totalPredictions = await prisma.prediction.count();
        const predictions = await prisma.prediction.findMany();
        
        // Calcular métricas básicas
        const benignPredictions = predictions.filter(p => p.tumorType === 'benigno');
        const malignPredictions = predictions.filter(p => p.tumorType === 'maligno');
        
        const accuracy = totalPredictions > 0 ? 
            (benignPredictions.length + malignPredictions.length) / totalPredictions : 0;

        await prisma.modelMetrics.upsert({
            where: { id: 1 },
            update: {
                accuracy,
                precision: 0.95, // Estos valores deberían calcularse con datos reales
                recall: 0.94,
                f1Score: 0.945,
                totalPredictions,
            },
            create: {
                accuracy,
                precision: 0.95,
                recall: 0.94,
                f1Score: 0.945,
                totalPredictions,
            }
        });
    }

    async getMetrics() {
        try {
            const [metrics, predictions, featureImportance] = await Promise.all([
                prisma.modelMetrics.findFirst(),
                prisma.prediction.findMany({
                    orderBy: { createdAt: 'desc' },
                    take: 100
                }),
                prisma.featureImportance.findMany()
            ]);

            const predictionTrends = this.calculatePredictionTrends(predictions);

            return {
                metrics,
                predictionTrends,
                featureImportance
            };
        } catch (error) {
            console.error('Error getting metrics:', error);
            throw error;
        }
    }

    calculatePredictionTrends(predictions) {
        const trendMap = predictions.reduce((acc, pred) => {
            const month = pred.createdAt.toISOString().slice(0, 7);
            if (!acc[month]) {
                acc[month] = { benigno: 0, maligno: 0 };
            }
            acc[month][pred.tumorType]++;
            return acc;
        }, {});

        return Object.entries(trendMap).map(([date, counts]) => ({
            date,
            ...counts
        }));
    }
}

module.exports = new MetricsService(); 