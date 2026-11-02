import { useState } from 'react';
import { Header } from './components/Header';
import { ImageUpload } from './components/ImageUpload';
import { PredictionResult } from './components/PredictionResult';
import { DiseaseInfoCard } from './components/DiseaseInfoCard';
import { predictImage } from './services/api';
import type { PredictionResponse } from './types';

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleImageSelected = (file: File) => {
    setSelectedFile(file);
    setResult(null);
    setError(null);
    setPreviewUrl(URL.createObjectURL(file));
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;
    setIsLoading(true);
    setError(null);
    try {
      const response = await predictImage(selectedFile);
      setResult(response);
    } catch (err: unknown) {
      if (err && typeof err === 'object' && 'response' in err) {
        const resp = err as { response?: { data?: { detail?: string }; status?: number } };
        if (resp.response?.status === 401) setError('Authentication failed. Check API key configuration.');
        else if (resp.response?.data?.detail) setError(resp.response.data.detail);
        else setError('Failed to analyze image. Please try again.');
      } else {
        setError('Could not connect to the server. Make sure the backend is running.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <div className="container">
          <div className="intro-text">
            <p>Upload or capture a coffee leaf image to detect diseases including Cercospora, Leaf Rust, Miner, and Phoma. This AI-assisted tool helps Ethiopian coffee farmers identify diseases early.</p>
          </div>
          <ImageUpload onImageSelected={handleImageSelected} onAnalyze={handleAnalyze} isLoading={isLoading} selectedImage={previewUrl} />
          {isLoading && (
            <div className="loading-indicator">
              <div className="spinner" />
              <p>Analyzing leaf image...</p>
            </div>
          )}
          {error && (
            <div className="error-container">
              <p className="error-text">{error}</p>
              <button className="btn btn-secondary" onClick={() => setError(null)}>Dismiss</button>
            </div>
          )}
          {result && (
            <div className="results-container">
              <PredictionResult result={result} />
              <DiseaseInfoCard info={result.disease_info} disclaimer={result.disclaimer} />
            </div>
          )}
          <footer className="footer">
            <p>AI-assisted analysis, not a confirmed diagnosis. Consult a qualified agronomist for confirmation and treatment recommendations.</p>
            <p className="footer-sub">Abole - Ethiopian AgTech | Powered by EfficientNet-B0</p>
          </footer>
        </div>
      </main>
    </div>
  );
}

export default App;
