const express = require('express');
const router = express.Router();
const predictionController = require('../controllers/predictionController');

router.post('/predict', predictionController.predict);
router.get('/metrics', predictionController.getMetrics);

module.exports = router; 