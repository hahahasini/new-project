import { useState } from 'react';

function DietPlan({ weeklyPlan, foodRecommendations, deficiency, allDietPlans }) {
  // Use allDietPlans (tabbed) if available, else fallback to the single plan
  const plans = allDietPlans && allDietPlans.length > 0
    ? allDietPlans
    : [{ deficiency, confidence: null, weekly_plan: weeklyPlan, food_recommendations: foodRecommendations }];

  const [activeTab, setActiveTab] = useState(0);
  const activePlan = plans[activeTab];

  const generateDietPlanText = () => {
    let text = '';
    plans.forEach((plan) => {
      text += `Diet Plan for ${plan.deficiency}`;
      if (plan.confidence !== null) text += ` (${plan.confidence.toFixed(1)}%)`;
      text += '\n' + '='.repeat(50) + '\n\n';
      if (plan.weekly_plan) {
        plan.weekly_plan.forEach((day) => {
          text += `${day.day}: ${day.foods.join(', ')}\n`;
        });
      }
      if (plan.food_recommendations && plan.food_recommendations.length > 0) {
        text += '\nRecommended Foods: ' + plan.food_recommendations.join(', ');
      }
      text += '\n\n';
    });
    return text.trim();
  };

  const handleDownload = () => {
    const text = generateDietPlanText();
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'diet_plans_all_deficiencies.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="diet-section" id="diet-plan">
      <h3>🥗 Diet Plans by Deficiency</h3>

      {/* Tabs */}
      {plans.length > 1 && (
        <div className="diet-tabs" role="tablist" aria-label="Deficiency diet plan tabs">
          {plans.map((plan, index) => (
            <button
              key={plan.deficiency}
              className={`diet-tab ${index === activeTab ? 'active' : ''}`}
              onClick={() => setActiveTab(index)}
              role="tab"
              aria-selected={index === activeTab}
              aria-controls={`diet-panel-${index}`}
              id={`diet-tab-${index}`}
            >
              <span className="diet-tab-label">{plan.deficiency}</span>
              {plan.confidence !== null && (
                <span className="diet-tab-confidence">{plan.confidence.toFixed(1)}%</span>
              )}
            </button>
          ))}
        </div>
      )}

      {/* Active Tab Content */}
      <div
        className="diet-tab-content animate-fade-in"
        key={activeTab}
        role="tabpanel"
        id={`diet-panel-${activeTab}`}
        aria-labelledby={`diet-tab-${activeTab}`}
      >
        <div className="diet-tab-header">
          <span className="diet-tab-header-icon">💊</span>
          <div>
            <span className="diet-tab-header-title">{activePlan.deficiency}</span>
            {activePlan.confidence !== null && (
              <span className="diet-tab-header-confidence">
                Detection confidence: {activePlan.confidence.toFixed(1)}%
              </span>
            )}
          </div>
        </div>

        {activePlan.weekly_plan && activePlan.weekly_plan.length > 0 && (
          <div className="diet-grid stagger-children">
            {activePlan.weekly_plan.map((day) => (
              <div key={day.day} className="diet-day">
                <span className="diet-day-name">{day.day}</span>
                <div className="diet-day-foods">
                  {day.foods.map((food, i) => (
                    <span key={i}>{food}</span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {activePlan.food_recommendations && activePlan.food_recommendations.length > 0 && (
          <>
            <h3 style={{ marginTop: 'var(--space-6)' }}>🍎 Recommended Foods</h3>
            <div className="food-tags">
              {activePlan.food_recommendations.map((food, i) => (
                <span key={i} className="food-tag">{food}</span>
              ))}
            </div>
          </>
        )}
      </div>

      <div className="download-section">
        <button
          className="btn btn-download"
          onClick={handleDownload}
          id="download-diet-button"
        >
          📥 Download All Diet Plans
        </button>
      </div>
    </div>
  );
}

export default DietPlan;
