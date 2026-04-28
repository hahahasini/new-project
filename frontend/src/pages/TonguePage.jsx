import { useState } from 'react';
import { Link } from 'react-router-dom';
import ImageUploader from '../components/ImageUploader';
import ResultsPanel from '../components/ResultsPanel';
import { analyzeImage } from '../services/api';

const BODY_PART = 'Tongue';

function TonguePage() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [previewUrl,    setPreviewUrl]    = useState(null);
  const [results,       setResults]       = useState(null);
  const [loading,       setLoading]       = useState(false);
  const [error,         setError]         = useState(null);

  const handleImageSelect = (file) => {
    setSelectedImage(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResults(null);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!selectedImage) return;
    setLoading(true);
    setError(null);
    try {
      const data = await analyzeImage(selectedImage, BODY_PART);
      setResults(data);
    } catch (err) {
      if (err.response?.data?.detail) setError(err.response.data.detail);
      else if (err.message?.includes('Network Error')) setError('Cannot connect to the server. Please ensure the backend is running on port 8000.');
      else setError('Analysis failed. Please try again with a different image.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedImage(null);
    setPreviewUrl(null);
    setResults(null);
    setError(null);
  };

  return (
    <main className="model-page animate-fade-in" id="tongue-page">
      <div className="container">

        <div className="page-header animate-fade-in-up">
          <Link to="/" className="back-btn" id="tongue-back-btn">← Back to Models</Link>
          <div className="page-header-content">
            <div className="page-header-img-wrap page-header-img-wrap--rose">
              <img src="/tongue-icon.png" alt="Tongue" className="page-header-img" />
            </div>
            <div>
              <h1 className="page-title">Tongue Analysis</h1>
              <p className="page-subtitle">Detects <strong>Vitamin B12</strong> &amp; <strong>Iron</strong> Deficiencies</p>
            </div>
          </div>
          <div className="page-header-tags">
            <span className="model-tag">Vitamin B12</span>
            <span className="model-tag">Iron Deficiency</span>
            <span className="model-tag">Glossitis</span>
            <span className="model-tag">Anemia</span>
          </div>
        </div>

        <div className="upload-tips glass animate-fade-in-up">
          <span className="upload-tips-icon">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          </span>
          <p><strong>Tips for best results:</strong> Photograph your tongue extended, in bright natural light. Keep the camera level with your mouth. Avoid food or drink for 10 minutes beforehand.</p>
        </div>

        <div className={`analysis-layout ${(!results && !loading) ? 'centered' : ''}`}>
          <div className="upload-section animate-fade-in-up" style={{ animationDelay: '0.1s' }}>
            <ImageUploader
              onImageSelect={handleImageSelect}
              previewUrl={previewUrl}
              onAnalyze={handleAnalyze}
              onReset={handleReset}
              loading={loading}
              hasImage={!!selectedImage}
              canAnalyze={true}
            />
            {error && (
              <div className="error-card animate-fade-in">
                <span className="error-icon">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                </span>
                <p>{error}</p>
              </div>
            )}
          </div>
          {(results || loading) && (
            <div className="results-section animate-slide-in-right">
              <ResultsPanel results={results} loading={loading} />
            </div>
          )}
        </div>

      </div>
    </main>
  );
}

export default TonguePage;
