import { useRef, useState } from 'react';

interface ImageUploadProps {
  onImageSelected: (file: File) => void;
  onAnalyze: () => void;
  isLoading: boolean;
  selectedImage: string | null;
}

const VALID_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
const MAX_SIZE_MB = 10;

export function ImageUpload({ onImageSelected, onAnalyze, isLoading, selectedImage }: ImageUploadProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [fileSizeWarning, setFileSizeWarning] = useState<string | null>(null);
  const [cameraSupported] = useState(typeof navigator !== 'undefined' && !!navigator.mediaDevices);
  const videoRef = useRef<HTMLVideoElement>(null);
  const [cameraActive, setCameraActive] = useState(false);
  const streamRef = useRef<MediaStream | null>(null);

  const validateFile = (file: File): boolean => {
    setError(null);
    setFileSizeWarning(null);
    if (!VALID_TYPES.includes(file.type)) {
      setError('Please upload a JPG, PNG, or WEBP image.');
      return false;
    }
    const sizeMB = file.size / (1024 * 1024);
    if (sizeMB > MAX_SIZE_MB) {
      setError(`File size exceeds ${MAX_SIZE_MB}MB. Please upload a smaller image.`);
      return false;
    }
    if (sizeMB > 5) {
      setFileSizeWarning(`File size is ${sizeMB.toFixed(1)}MB (recommended max: 5MB).`);
    }
    return true;
  };

  const handleFile = (file: File) => {
    if (validateFile(file)) onImageSelected(file);
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleFile(file);
  };

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
      streamRef.current = stream;
      if (videoRef.current) videoRef.current.srcObject = stream;
      setCameraActive(true);
    } catch {
      setError('Could not access camera. Please use file upload instead.');
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
    setCameraActive(false);
  };

  const capturePhoto = () => {
    if (videoRef.current) {
      const canvas = document.createElement('canvas');
      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.drawImage(videoRef.current, 0, 0);
        canvas.toBlob((blob) => {
          if (blob) {
            const file = new File([blob], 'captured.jpg', { type: 'image/jpeg' });
            handleFile(file);
          }
          stopCamera();
        }, 'image/jpeg', 0.9);
      }
    }
  };

  return (
    <div className="upload-section">
      {cameraActive && (
        <div className="camera-container">
          <video ref={videoRef} autoPlay playsInline className="camera-preview" />
          <div className="camera-controls">
            <button className="btn btn-primary" onClick={capturePhoto} disabled={isLoading}>Capture</button>
            <button className="btn btn-secondary" onClick={stopCamera}>Cancel</button>
          </div>
        </div>
      )}
      {!cameraActive && (
        <>
          <div className={`drop-zone ${isDragging ? 'dragging' : ''}`}
            onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
            onDragLeave={(e) => { e.preventDefault(); setIsDragging(false); }}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            {selectedImage ? (
              <img src={selectedImage} alt="Selected coffee leaf" className="image-preview" />
            ) : (
              <div className="drop-zone-placeholder">
                <p className="drop-zone-text">Drag and drop a coffee leaf image here<br />or click to browse</p>
                <p className="drop-zone-subtext">JPG, PNG, or WEBP up to 10MB</p>
              </div>
            )}
          </div>
          <input ref={fileInputRef} type="file" accept="image/jpeg,image/png,image/webp" onChange={handleFileInput} style={{ display: 'none' }} />
          {error && <p className="error-message">{error}</p>}
          {fileSizeWarning && <p className="warning-message">{fileSizeWarning}</p>}
          <div className="button-group">
            <button className="btn btn-secondary" onClick={() => fileInputRef.current?.click()} disabled={isLoading}>Choose File</button>
            {cameraSupported && <button className="btn btn-secondary" onClick={startCamera} disabled={isLoading}>Use Camera</button>}
            <button className="btn btn-primary" onClick={onAnalyze} disabled={!selectedImage || isLoading}>
              {isLoading ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
        </>
      )}
    </div>
  );
}
