# Evaluation Report — AI Coffee Leaf Disease Detection

## Status: Awaiting Model Training

This report will be populated with actual metrics after running the Colab notebook (`colab/coffee_leaf_disease_detection.ipynb`) on Google Colab with GPU runtime.

## Model: EfficientNet-B0 (Transfer Learning)

### Dataset
- Source: JMuBEN/JMuBEN2 via HuggingFace (`Project-AgML/arabica_coffee_leaf_disease_classification`)
- Total images: 58,549
- Classes: 5 (Cercospora, Healthy, Leaf Rust, Miner, Phoma)
- Split: 70% train / 15% validation / 15% test (source-aware, perceptual hashing)

### Class Distribution
| Class | Count | Percentage |
|-------|-------|-----------|
| Cercospora | 7,681 | 13% |
| Healthy | 18,983 | 32% |
| Leaf Rust | 8,336 | 14% |
| Miner | 16,978 | 29% |
| Phoma | 6,571 | 11% |

### Training Configuration
- Optimizer: AdamW (lr=1e-4, weight_decay=1e-4)
- Scheduler: Cosine Annealing
- Loss: Weighted CrossEntropyLoss (class weights inversely proportional to frequency)
- Augmentation: RandomHorizontalFlip, RandomVerticalFlip, RandomRotation, ColorJitter, RandomAffine
- Oversampling: Cercospora and Phoma (2x) — minority class targeted augmentation
- Batch size: 32
- Max epochs: 30 (early stopping patience: 7)
- Mixed precision: enabled

### Results

_Metrics will be filled in after training. Only actual results are reported — never invented._

### Data Leakage Prevention
- Perceptual hashing (pHash) computed for all 58,549 images
- Near-duplicate clusters identified using Hamming distance threshold
- Source-aware split ensures all near-duplicates stay in the same split
- Verified: no near-duplicate overlap between train/validation/test sets

> This is AI-assisted analysis, not a confirmed diagnosis.
> Consult a qualified agronomist or plant pathologist for confirmation.
