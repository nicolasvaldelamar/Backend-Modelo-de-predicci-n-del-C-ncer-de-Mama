const { validateFeatures } = require('../utils/validators');

const validatePredictionInput = (req, res, next) => {
    const { features } = req.body;
    
    const validationError = validateFeatures(features);
    if (validationError) {
        return res.status(400).json({ error: validationError });
    }
    
    next();
};

module.exports = {
    validatePredictionInput
}; 