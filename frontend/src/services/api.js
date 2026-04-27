import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60s — model inference can be slow
});

/**
 * Upload an image for vitamin deficiency analysis.
 * @param {File} imageFile - The image file to analyze.
 * @param {string} bodyPart - The body part type: "Nail", "Skin", or "Tongue".
 * @returns {Promise<Object>} Analysis results.
 */
export async function analyzeImage(imageFile, bodyPart) {
  const formData = new FormData();
  formData.append('file', imageFile);
  formData.append('body_part', bodyPart);

  const response = await api.post('/analyze', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

  return response.data;
}

/**
 * Check API health status.
 * @returns {Promise<Object>} Health check response.
 */
export async function healthCheck() {
  const response = await api.get('/health');
  return response.data;
}

export default api;
