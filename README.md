# AI Coffee Leaf Disease Detection — Abole

An AI-assisted coffee leaf disease detection system for Ethiopian coffee farmers, built for **Abole**, an Ethiopian AgTech startup. The system classifies coffee leaf images into five categories: **Healthy**, **Cercospora**, **Leaf Rust**, **Miner**, and **Phoma**.

> **Disclaimer:** All predictions are AI-assisted, not confirmed diagnoses. Consult a qualified agronomist or plant pathologist for confirmation and treatment recommendations.

## Architecture

```
Frontend (React + Vite + TypeScript)         Backend (FastAPI + ONNX)
┌────────────────────────────────┐         ┌──────────────────────────────┐
│  Image Upload / Camera Capture  │         │  API Key Auth (X-API-Key)    │
│  Image Preview                  │  POST   │  ↓                            │
│  Analyze Button                 │ ──────> │  Image Preprocessing Service  │
│  Prediction Display + Confidence│ /predict│  ↓                            │
│  Disease Info + Management      │ <────── │  ONNX Inference Service       │
│  Disclaimer                     │  JSON   │  ↓                            │
└────────────────────────────────┘         │  Disease Info Service         │
                                           │  ↓                            │
                                           │  Structured JSON Response     │
                                           └──────────────────────────────┘
```

## Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- Node.js 20+
- npm

### 1. Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # Edit API_KEY if needed
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend runs on `http://localhost:8000`. It starts in **demo mode** (returns placeholder predictions) when no trained ONNX model is present.

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env  # Edit API_KEY if needed
npm run dev
```

The frontend runs on `http://localhost:3000`.

### 3. Docker (Both Services)

```bash
docker-compose up
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`

## Training the Model (Google Colab)

1. Open `colab/coffee_leaf_disease_detection.ipynb` in Google Colab
2. Set runtime to GPU (T4 or better)
3. Run all cells — the notebook will:
   - Load the JMuBEN/JMuBEN2 dataset from HuggingFace (58,549 images)
   - Perform EDA and visualize class distribution
   - Detect near-duplicates using perceptual hashing and create a source-aware split
   - Build augmentation pipelines with targeted oversampling for minority classes
   - Train EfficientNet-B0 with weighted cross-entropy loss
   - Evaluate with accuracy, precision, recall, F1-score, and confusion matrix
   - Export the model to ONNX format
4. Download `efficientnet_b0_coffee.onnx` and `label_mapping.json` from Google Drive
5. Place them in the `model/` directory
6. Set `DEMO_MODE=false` in `backend/.env`
7. Restart the backend — it will now use the real trained model

## API Documentation

### Health Check
```bash
curl http://localhost:8000/health
```

### Predict Disease
```bash
curl -X POST http://localhost:8000/predict \
  -H "X-API-Key: abole-demo-key-change-me" \
  -F "file=@coffee_leaf.jpg"
```

### Response Format
```json
{
  "predicted_class": "Leaf Rust",
  "confidence": 0.87,
  "all_probabilities": [
    {"class_name": "Leaf Rust", "probability": 0.87},
    {"class_name": "Healthy", "probability": 0.05},
    {"class_name": "Cercospora", "probability": 0.03},
    {"class_name": "Miner", "probability": 0.03},
    {"class_name": "Phoma", "probability": 0.02}
  ],
  "disease_info": {
    "name": "Leaf Rust",
    "scientific_name": "Hemileia vastatrix",
    "description": "...",
    "symptoms": ["..."],
    "management_practices": ["..."],
    "ethiopian_context": "...",
    "citations": ["..."]
  },
  "warnings": [],
  "disclaimer": "This is AI-assisted analysis, not a confirmed diagnosis...",
  "is_demo_prediction": false
}
```

## Abole Integration Guide

### Connecting to the API
1. Obtain an API key from the Abole team
2. Send image files as `multipart/form-data` to the `/predict` endpoint
3. Include the API key in the `X-API-Key` header
4. Parse the JSON response for prediction, confidence, and disease information

### Example Integration (Python)
```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    headers={"X-API-Key": "your-api-key"},
    files={"file": open("coffee_leaf.jpg", "rb")},
)
data = response.json()
print(f"Disease: {data['predicted_class']} ({data['confidence']*100:.1f}% confidence)")
```

## Fine-Tuning with Ethiopian Coffee Leaf Images

1. Collect Ethiopian coffee leaf images across all 5 classes
2. Add them to the dataset directory (follow JMuBEN format)
3. Update the Colab notebook to include the new images in the training set
4. Re-run the notebook to train an updated model
5. Export the new ONNX model and replace the file in `model/`
6. Restart the backend

## Project Structure
```
├── colab/           # Google Colab training notebook
├── backend/         # FastAPI backend with ONNX inference
├── frontend/        # React + Vite + TypeScript frontend
├── model/           # Trained ONNX model + label mapping
├── docs/            # Evaluation report
├── docker-compose.yml
└── README.md
```

## Disease Information Sources

All disease information is sourced from published agricultural extension literature:
- University of Hawai'i at Manoa, CTAHR
- CABI (Coffee Pests, Diseases & Their Management)
- APS Compendium of Coffee Diseases and Pests
- Peer-reviewed publications (see citations in API responses)

## License

This project is developed for Abole, an Ethiopian AgTech startup.
