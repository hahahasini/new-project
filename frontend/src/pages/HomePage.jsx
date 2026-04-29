import { Link } from 'react-router-dom';

const MODEL_CARDS = [
  {
    id: 'nail',
    to: '/nail',
    image: '/nail-icon.png',
    imageAlt: 'Close-up of a fingernail for vitamin deficiency analysis',
    title: 'Nail Analysis',
    subtitle: 'Iodine & Vitamin D',
    description: 'Your nails can reveal a surprising amount about your nutritional health. Our model reads nail color, texture, ridging patterns, and shape to identify early signs of deficiency - before symptoms become obvious.',
    color: 'indigo',
    btnId: 'card-cta-nail',
    cardId: 'model-card-nail',
  },
  {
    id: 'tongue',
    to: '/tongue',
    image: '/tongue-icon.png',
    imageAlt: 'Close-up of a tongue for vitamin B12 and iron deficiency analysis',
    title: 'Tongue Analysis',
    subtitle: 'Vitamin B12 & Iron',
    description: 'The tongue is one of the body\'s earliest indicators of nutritional gaps. Changes in color, surface texture, and coating are strong visual signals our model has learned to recognize with clinical precision.',
    color: 'rose',
    btnId: 'card-cta-tongue',
    cardId: 'model-card-tongue',
  },
  {
    id: 'skin',
    to: '/skin',
    image: '/skin-icon.png',
    imageAlt: 'Close-up of skin texture for vitamin A and D deficiency analysis',
    title: 'Skin Analysis',
    subtitle: 'Vitamin A & Vitamin D',
    description: 'Skin changes like dryness, roughness, and scaling are often the first signs of a deeper nutritional imbalance. Upload a clear photo of the affected area and let our model do the rest.',
    color: 'cyan',
    btnId: 'card-cta-skin',
    cardId: 'model-card-skin',
  },
];

const STATS = [
  { value: '3', label: 'Specialized Models' },
  { value: '< 2s', label: 'Average Analysis Time' },
  { value: '3+', label: 'Deficiencies Detected' },
  { value: '100%', label: 'Private - Runs Locally' },
];

const STEPS = [
  { step: '01', title: 'Upload a Photo', desc: 'Take a clear, well-lit photo of your nail, tongue, or skin and upload it directly from your device.' },
  { step: '02', title: 'Model Analysis', desc: 'Our trained CNN model scans the image for visual biomarkers associated with specific deficiencies.' },
  { step: '03', title: 'Review Your Results', desc: 'Get a confidence-scored diagnosis with a full prediction breakdown so you understand what was detected.' },
  { step: '04', title: 'Next Steps', desc: 'Receive a personalized weekly diet plan and find nearby specialists on an interactive map.' },
];

function HomePage() {
  return (
    <main className="home-page" id="home-page">

      {/* ── Hero ── */}
      <section className="home-hero animate-fade-in-up" id="hero-section">

        <h1 className="home-hero-title">
          Understand Your Body
          <br />
          <span className="gradient-text">From the Outside In</span>
        </h1>

        <p className="home-hero-subtitle">
          Your <strong>nails</strong>, <strong>tongue</strong>, and <strong>skin</strong> carry visible clues
          about what your body is missing. Upload a photo and our models will analyze it for potential
          vitamin and mineral deficiencies - in under a minute.
        </p>

        <div className="home-hero-actions">
          <Link to="/nail" className="btn btn-primary btn-lg" id="hero-cta-nail">
            Try It Now
          </Link>
          <a href="#models" className="btn btn-ghost btn-lg" id="hero-learn-more">
            See How It Works
          </a>
        </div>
      </section>

      {/* ── Stats Row ── */}
      <section className="home-stats stagger-children" aria-label="Key statistics">
        {STATS.map(({ value, label }) => (
          <div key={label} className="stat-item glass">
            <span className="stat-value">{value}</span>
            <span className="stat-label">{label}</span>
          </div>
        ))}
      </section>

      {/* ── Model Cards ── */}
      <section className="model-cards-section" id="models" aria-label="Models">
        <div className="section-header animate-fade-in-up">
          <h2 className="section-title">Choose Your Analysis</h2>
          <p className="section-subtitle">
            Each model is purpose-built and trained on clinical image datasets specific to that body part.
            Select the one that matches your concern.
          </p>
        </div>

        <div className="model-cards stagger-children">
          {MODEL_CARDS.map(({ id, to, image, imageAlt, title, subtitle, description, color, btnId, cardId }) => (
            <article key={id} className={`model-card model-card--${color}`} id={cardId} aria-label={title}>

              {/* Realistic image */}
              <div className="model-card-image-wrap">
                <img
                  src={image}
                  alt={imageAlt}
                  className="model-card-image"
                  loading="lazy"
                  draggable={false}
                />
                <div className={`model-card-image-overlay model-card-image-overlay--${color}`} />
              </div>

              <div className="model-card-body">
                <div className="model-card-header">
                  <h3 className="model-card-title">{title}</h3>
                  <span className={`model-card-subtitle-pill model-card-subtitle-pill--${color}`}>{subtitle}</span>
                </div>
                <p className="model-card-description">{description}</p>
              </div>

              <Link to={to} className="model-card-cta btn btn-primary" id={btnId}>
                Analyze Now →
              </Link>
            </article>
          ))}
        </div>
      </section>

      {/* ── How It Works ── */}
      <section className="how-it-works animate-fade-in-up" id="how-it-works">
        <h2 className="section-title">How It Works</h2>
        <div className="steps stagger-children">
          {STEPS.map(({ step, title, desc }) => (
            <div key={step} className="step-card glass">
              <span className="step-number">{step}</span>
              <h4 className="step-title">{title}</h4>
              <p className="step-desc">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── Disclaimer ── */}
      <div className="home-disclaimer animate-fade-in-up">
        <strong>Medical Disclaimer:</strong> VitaDetect is designed to provide helpful insights, not medical advice.
        Always consult a qualified healthcare professional before making any health decisions.
      </div>

    </main>
  );
}

export default HomePage;
