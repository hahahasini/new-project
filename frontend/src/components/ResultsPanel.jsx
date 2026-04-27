import ConfidenceChart from './ConfidenceChart';
import DietPlan from './DietPlan';

function ResultsPanel({ results, loading }) {
  if (loading) {
    return (
      <div className="results-card" id="results-panel">
        <h2>🔍 Analysis Results</h2>
        <div className="result-items">
          <div className="skeleton skeleton-block"></div>
          <div className="skeleton skeleton-line" style={{ width: '80%' }}></div>
          <div className="skeleton skeleton-line" style={{ width: '60%' }}></div>
          <div className="skeleton skeleton-line" style={{ width: '70%' }}></div>
        </div>
        <div className="skeleton skeleton-block" style={{ height: '180px' }}></div>
      </div>
    );
  }

  if (!results) return null;

  const confidenceColor =
    results.confidence >= 80
      ? '#10b981'
      : results.confidence >= 50
      ? '#f59e0b'
      : '#ef4444';

  return (
    <div className="results-card animate-fade-in" id="results-panel">
      <h2>🔍 Analysis Results</h2>

      {/* Key Results */}
      <div className="result-items stagger-children">
        <div className="result-item">
          <div className="result-item-icon body-part">🏷️</div>
          <div className="result-item-content">
            <div className="result-item-label">Detected Body Part</div>
            <div className="result-item-value">{results.body_part}</div>
          </div>
        </div>

        <div className="result-item">
          <div className="result-item-icon disease">🦠</div>
          <div className="result-item-content">
            <div className="result-item-label">Detected Disease</div>
            <div className="result-item-value">{results.disease}</div>
          </div>
        </div>

        <div className="result-item">
          <div className="result-item-icon deficiency">💊</div>
          <div className="result-item-content">
            <div className="result-item-label">Vitamin Deficiency</div>
            <div className="result-item-value">{results.deficiency}</div>
          </div>
        </div>

        <div className="result-item">
          <div className="result-item-icon confidence">📊</div>
          <div className="result-item-content">
            <div className="result-item-label">Confidence</div>
            <div className="result-item-value" style={{ color: confidenceColor }}>
              {results.confidence.toFixed(1)}%
            </div>
            <div className="confidence-bar-container">
              <div
                className="confidence-bar"
                style={{ width: `${results.confidence}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      <div className="results-divider"></div>

      {/* Confidence Chart */}
      {results.prediction_scores && results.prediction_scores.length > 0 && (
        <div className="chart-section">
          <h3>📊 Confidence Breakdown</h3>
          <div className="chart-container">
            <ConfidenceChart scores={results.prediction_scores} />
          </div>
        </div>
      )}

      <div className="results-divider"></div>

      {/* Diet Plan */}
      <DietPlan
        weeklyPlan={results.weekly_diet_plan}
        foodRecommendations={results.food_recommendations}
        deficiency={results.deficiency}
      />
    </div>
  );
}

export default ResultsPanel;
