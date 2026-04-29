function BodyPartSelector({ bodyParts, selected, onSelect }) {
  return (
    <div className="body-part-selector animate-fade-in-up" id="body-part-selector">
      <h3 className="selector-title">🏷️ Select Body Part</h3>
      <p className="selector-hint">Choose which body part the image shows</p>
      <div className="selector-grid">
        {bodyParts.map((part) => (
          <button
            key={part.id}
            className={`selector-btn ${selected === part.id ? 'selected' : ''} ${!part.hasModel ? 'no-model' : ''}`}
            onClick={() => onSelect(part.id)}
            id={`select-${part.id.toLowerCase()}`}
            aria-pressed={selected === part.id}
          >
            <span className="selector-icon">{part.icon}</span>
            <span className="selector-label">{part.label}</span>
            {!part.hasModel && <span className="selector-warning">Mock</span>}
          </button>
        ))}
      </div>
      {selected && !bodyParts.find((p) => p.id === selected)?.hasModel && (
        <p className="selector-mock-notice animate-fade-in">
          ⚠️ No trained model available for <strong>{selected}</strong> - results will be simulated.
        </p>
      )}
    </div>
  );
}

export default BodyPartSelector;
