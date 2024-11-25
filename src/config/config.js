const config = {
    environment: process.env.NODE_ENV || 'development',
    port: process.env.PORT || 3000,
    modelPaths: {
        randomForest: {
            model: 'data/models/randomForest/model.pkl',
            scaler: 'data/models/randomForest/scaler.pkl',
            config: 'ml/models/randomForest/config.json'
        },
        neuralNetwork: {
            model: 'data/models/neuralNetwork/model.h5',
            scaler: 'data/models/neuralNetwork/scaler.pkl',
            config: 'ml/models/neuralNetwork/config.json'
        }
    },
    logging: {
        level: process.env.LOG_LEVEL || 'info',
        file: 'logs/app.log'
    },
    validation: {
        features: {
            min: 1,
            max: 10,
            required: [
                'Clump_Thickness',
                'Uniformity_of_Cell_Size',
                'Uniformity_of_Cell_Shape',
                'Marginal_Adhesion',
                'Single_Epithelial_Cell_Size',
                'Bare_Nuclei',
                'Bland_Chromatin',
                'Normal_Nucleoli',
                'Mitoses'
            ]
        }
    }
};

module.exports = config; 