import ConfidenceChart from './ConfidenceChart';
import DietPlan from './DietPlan';
import NearbyDoctors from './NearbyDoctors';

function ResultsPanel({ results, loading }) {
  if (loading) {
    return (
      <div className="results-card" id="results-panel">
        <h2>Analysis Results</h2>
        <div className="result-items">
          <div className="skeleton skeleton-block" />
          <div className="skeleton skeleton-line" style={{ width: '80%' }} />
          <div className="skeleton skeleton-line" style={{ width: '60%' }} />
          <div className="skeleton skeleton-line" style={{ width: '70%' }} />
        </div>
        <div className="skeleton skeleton-block" style={{ height: '180px' }} />
      </div>
    );
  }

  if (!results) return null;

  const confidenceColor =
    results.confidence >= 80 ? '#10b981'
    : results.confidence >= 50 ? '#f59e0b'
    : '#ef4444';

  return (
    <div className="results-card animate-fade-in" id="results-panel">
      <h2>Analysis Results</h2>

      {!results.model_available && (
        <div className="selector-mock-notice animate-fade-in" style={{ marginBottom: '20px', padding: '10px', borderLeft: '4px solid #ef4444' }}>
          <strong>Mock Prediction:</strong> The model could not be loaded. These results are simulated.
        </div>
      )}

      <div className="result-items stagger-children">
        <div className="result-item">
          <div className="result-item-icon body-part">
            <svg viewBox="0 0 20 20" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"><circle cx="10" cy="10" r="8"/><path d="M10 6v4l3 2"/></svg>
          </div>
          <div className="result-item-content">
            <div className="result-item-label">Detected Body Part</div>
            <div className="result-item-value">{results.body_part}</div>
          </div>
        </div>

        <div className="result-item">
          <div className="result-item-icon disease">
            <svg viewBox="0 0 20 20" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"><path d="M10 3a7 7 0 1 0 0 14A7 7 0 0 0 10 3zm0 4v3m0 3h.01"/></svg>
          </div>
          <div className="result-item-content">
            <div className="result-item-label">Detected Condition</div>
            <div className="result-item-value">{results.disease}</div>
          </div>
        </div>

        <div className="result-item">
          <div className="result-item-icon deficiency">
            <svg viewBox="0 0 20 20" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"><rect x="6" y="2" width="8" height="16" rx="2"/><line x1="10" y1="6" x2="10" y2="14"/><line x1="7" y1="10" x2="13" y2="10"/></svg>
          </div>
          <div className="result-item-content">
            <div className="result-item-label">Vitamin Deficiency</div>
            <div className="result-item-value">{results.deficiency}</div>
          </div>
        </div>

        <div className="result-item">
          <div className="result-item-icon confidence">
            <svg viewBox="0 0 20 20" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"><path d="M3 17l4-8 4 4 3-5 3 9"/></svg>
          </div>
          <div className="result-item-content">
            <div className="result-item-label">Confidence</div>
            <div className="result-item-value" style={{ color: confidenceColor }}>
              {results.confidence.toFixed(1)}%
            </div>
            <div className="confidence-bar-container">
              <div className="confidence-bar" style={{ width: `${results.confidence}%` }} />
            </div>
          </div>
        </div>
      </div>

      <div className="results-divider" />

      {results.prediction_scores?.length > 0 && (
        <div className="chart-section">
          <h3>Confidence Breakdown</h3>
          <div className="chart-container">
            <ConfidenceChart scores={results.prediction_scores} />
          </div>
        </div>
      )}

      <div className="results-divider" />

      <DietPlan
        weeklyPlan={results.weekly_diet_plan}
        foodRecommendations={results.food_recommendations}
        deficiency={results.deficiency}
        confidence={results.confidence}
        allDietPlans={results.all_diet_plans}
      />

      <div className="results-divider" />

      <NearbyDoctors deficiency={results.deficiency} />
    </div>
  );
}

export default ResultsPanel;
