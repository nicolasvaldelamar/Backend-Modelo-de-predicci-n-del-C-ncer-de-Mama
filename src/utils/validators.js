const config = require('../config/config');

const validateFeatures = (features) => {
    // Verificar si features es un array
    if (!Array.isArray(features)) {
        return 'Las características deben ser un array';
    }

    // Verificar la longitud correcta
    if (features.length !== config.validation.features.required.length) {
        return `Se requieren exactamente ${config.validation.features.required.length} características`;
    }

    // Verificar que todos los valores sean números y estén en el rango correcto
    for (let i = 0; i < features.length; i++) {
        const value = features[i];
        
        if (typeof value !== 'number') {
            return `La característica ${config.validation.features.required[i]} debe ser un número`;
        }

        if (value < config.validation.features.min || value > config.validation.features.max) {
            return `La característica ${config.validation.features.required[i]} debe estar entre ${config.validation.features.min} y ${config.validation.features.max}`;
        }
    }

    return null;
};

module.exports = {
    validateFeatures
}; 