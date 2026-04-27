function DietPlan({ weeklyPlan, foodRecommendations, deficiency }) {
  const generateDietPlanText = () => {
    let text = `Weekly Diet Plan for ${deficiency}\n`;
    text += '='.repeat(40) + '\n\n';
    weeklyPlan.forEach((day) => {
      text += `${day.day}: ${day.foods.join(', ')}\n`;
    });
    text += '\nRecommended Foods: ' + foodRecommendations.join(', ');
    return text;
  };

  const handleDownload = () => {
    const text = generateDietPlanText();
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `diet_plan_${deficiency.replace(/\s+/g, '_').toLowerCase()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="diet-section" id="diet-plan">
      <h3>🥗 Weekly Diet Plan</h3>

      {weeklyPlan && weeklyPlan.length > 0 && (
        <div className="diet-grid stagger-children">
          {weeklyPlan.map((day) => (
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

      {foodRecommendations && foodRecommendations.length > 0 && (
        <>
          <h3 style={{ marginTop: 'var(--space-6)' }}>🍎 Recommended Foods</h3>
          <div className="food-tags">
            {foodRecommendations.map((food, i) => (
              <span key={i} className="food-tag">{food}</span>
            ))}
          </div>
        </>
      )}

      <div className="download-section">
        <button
          className="btn btn-download"
          onClick={handleDownload}
          id="download-diet-button"
        >
          📥 Download Diet Plan
        </button>
      </div>
    </div>
  );
}

export default DietPlan;
