import { useState, useRef } from 'react';

function ImageUploader({ onImageSelect, previewUrl, onAnalyze, onReset, loading, hasImage, canAnalyze }) {
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      onImageSelect(file);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onImageSelect(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="uploader-card" id="image-uploader">
      <h2>📷 Upload Image</h2>

      {!previewUrl ? (
        <div
          className={`dropzone ${dragOver ? 'drag-over' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleClick}
          role="button"
          tabIndex={0}
          aria-label="Upload image for analysis"
          onKeyDown={(e) => e.key === 'Enter' && handleClick()}
        >
          <span className="dropzone-icon">📤</span>
          <p className="dropzone-text">
            Drag & drop your image here, or <strong>click to browse</strong>
          </p>
          <p className="dropzone-hint">Supports JPG, JPEG, PNG</p>
        </div>
      ) : (
        <div className="image-preview-container">
          <img
            src={previewUrl}
            alt="Selected image preview"
            className="image-preview"
            id="image-preview"
          />
        </div>
      )}

      <input
        ref={fileInputRef}
        type="file"
        accept="image/jpeg,image/png,image/jpg"
        onChange={handleFileChange}
        style={{ display: 'none' }}
        id="file-input"
        aria-hidden="true"
      />

      {hasImage && (
        <div className="btn-group">
          <button
            className="btn btn-primary"
            onClick={onAnalyze}
            disabled={loading || !canAnalyze}
            id="analyze-button"
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Analyzing...
              </>
            ) : (
              <>🔬 Analyze Image</>
            )}
          </button>
          <button
            className="btn btn-ghost"
            onClick={onReset}
            disabled={loading}
            id="reset-button"
          >
            ✕ Clear
          </button>
        </div>
      )}
    </div>
  );
}

export default ImageUploader;
