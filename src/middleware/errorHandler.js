const logger = require('../utils/logger');

const errorHandler = (err, req, res, next) => {
    logger.error('Error:', err);

    // Errores de validación
    if (err.name === 'ValidationError') {
        return res.status(400).json({
            error: 'Error de validación',
            details: Object.values(err.errors).map(e => e.message)
        });
    }

    // Errores del modelo
    if (err.name === 'ModelError') {
        return res.status(500).json({
            error: 'Error en el modelo de predicción',
            details: err.message
        });
    }

    // Error por defecto
    res.status(500).json({
        error: 'Error interno del servidor',
        details: process.env.NODE_ENV === 'development' ? err.message : 'Contacte al administrador'
    });
};

module.exports = errorHandler; 