import type { PredictionResponse } from '../types';

interface PredictionResultProps {
  result: PredictionResponse;
}

export function PredictionResult({ result }: PredictionResultProps) {
  const confidencePercent = (result.confidence * 100).toFixed(1);
  const isHealthy = result.predicted_class === 'Healthy';

  return (
    <div className="prediction-result">
      {result.is_demo_prediction && (
        <div className="demo-banner">
          <strong>Demo Mode:</strong> No trained model loaded. This is a placeholder prediction.
          Run the Colab notebook to train the model and enable real predictions.
        </div>
      )}
      <div className={`prediction-header ${isHealthy ? 'healthy' : 'disease-detected'}`}>
        <span className="prediction-label">{isHealthy ? 'No Disease Detected' : 'Disease Detected'}</span>
        <h2 className="prediction-class">{result.predicted_class}</h2>
        <div className="confidence-bar-container">
          <div className="confidence-bar" style={{ width: `${confidencePercent}%` }} />
          <span className="confidence-text">{confidencePercent}% confidence</span>
        </div>
      </div>
      {result.warnings.length > 0 && (
        <div className="warnings-section">
          <h4>Warnings</h4>
          <ul className="warning-list">
            {result.warnings.map((w, i) => <li key={i} className="warning-item">{w}</li>)}
          </ul>
        </div>
      )}
      <div className="probabilities-section">
        <h4>All Predictions</h4>
        <div className="probability-list">
          {result.all_probabilities.map((prob, i) => (
            <div key={i} className="probability-item">
              <span className="prob-class-name">{prob.class_name}</span>
              <div className="prob-bar-container">
                <div className={`prob-bar ${prob.class_name === result.predicted_class ? 'highlighted' : ''}`}
                  style={{ width: `${(prob.probability * 100).toFixed(1)}%` }} />
              </div>
              <span className="prob-value">{(prob.probability * 100).toFixed(1)}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
