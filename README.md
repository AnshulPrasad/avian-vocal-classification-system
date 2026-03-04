# Bioacoustic Classification System

A practical end-to-end pipeline for animal audio (focused on Indian bird species):

1. Download raw recordings from Xeno-canto
2. Preprocess audio (resample, mono, trim, chunk)
3. Generate augmented Mel spectrograms
4. Split spectrograms into train/val/test folders

This repo is aimed at learning and building a foundation for sound-type or species classification models.

## Current Status

Implemented:
- Data download pipeline (`src/download.py`)
- Audio preprocessing pipeline (`src/preprocess.py`)
- Feature extraction + augmentation (`src/features.py`)
- End-to-end orchestration (`src/__init__.py`)
- Logging utilities (`src/logger.py`)

Scaffolded (to be implemented):
- Dataset class (`src/dataset.py`)
- Model API (`src/model.py`)
- Training/evaluation/prediction scripts (`src/train.py`, `src/evaluate.py`, `src/predict.py`)

## Project Structure

```text
bioacoustic-classification-system/
├── configs/
│   └── config.yaml               # Species list
├── data/
│   ├── raw/                      # Downloaded MP3 + per-species metadata CSV
│   ├── processed/                # Processed WAV chunks
│   └── spectrograms/
│       ├── all/                  # Full generated spectrogram set
│       ├── train/
│       ├── val/
│       └── test/
├── logs/                         # download.log, preprocess.log, features.log, pipeline.log
├── src/
│   ├── __init__.py               # Pipeline entrypoint
│   ├── download.py
│   ├── preprocess.py
│   ├── features.py
│   ├── logger.py
│   ├── dataset.py                # TODO
│   ├── model.py                  # TODO
│   ├── train.py                  # TODO
│   ├── evaluate.py               # TODO
│   └── predict.py                # TODO
├── pyproject.toml
├── uv.lock
└── README.md
```

## Requirements

- Python 3.12+
- `uv` (recommended) or `pip`
- Xeno-canto API key

## Setup

### 1) Install dependencies (uv)

From repo root:

```bash
uv sync
```

### 2) Create `.env`

Create `.env` in project root:

```env
XENO_CANTO_API_KEY=your_api_key_here
```

`src/download.py` loads this with `python-dotenv`.

### 3) Configure species list

Edit `configs/config.yaml`:

```yaml
species_list:
  - scientific_name: "Eudynamys scolopaceus"
    common_name: "Asian Koel"
  - scientific_name: "Pavo cristatus"
    common_name: "Indian Peafowl"
```

## Run The Pipeline

Important: current code uses relative paths like `../data/...` inside `src/`, so run from `src/`.

```bash
cd src
uv run python __init__.py
```

This runs:
- `download()`
- `preprocess()`
- `feature_extraction()`
- `split_dataset('../data/spectrograms/all', '../data/spectrograms')`

## Stage Details

### Download (`src/download.py`)

- Calls Xeno-canto API v3 per species
- Downloads MP3 files into `data/raw/<Common_Name>_mp3/`
- Writes species metadata CSV into `data/raw/`

### Preprocess (`src/preprocess.py`)

- Resample to 22050 Hz
- Convert to mono
- Trim silence
- Split into 5-second chunks
- Save WAV chunks to `data/processed/`

### Feature Extraction (`src/features.py`)

- Augment waveform:
  - time-stretch
  - pitch-shift
  - additive noise
- Generate Mel spectrogram (`fmin=500`, `fmax=8000`, `n_mels=128`)
- Save:
  - `.png` for visualization
  - `.npy` for numeric arrays

### Dataset Split (`split_dataset` in `src/__init__.py`)

- Reads all `.png` from `data/spectrograms/all`
- Splits using 70/15/15
- Copies files to:
  - `data/spectrograms/train`
  - `data/spectrograms/val`
  - `data/spectrograms/test`

## Logging

Logs are written to `logs/`:
- `download.log`
- `preprocess.log`
- `features.log`
- `pipeline.log`

Format:

```text
%(asctime)s | %(name)s | %(levelname)s :: %(message)s
```

## Troubleshooting

### 1) `XENO_CANTO_API_KEY is not set`

- Ensure `.env` exists at project root
- Ensure variable name is exactly `XENO_CANTO_API_KEY`
- Re-run script after updating `.env`

### 2) `n_samples=0` in `train_test_split`

- No PNG files were found in split source path
- Run `feature_extraction()` first
- Verify files exist in `data/spectrograms/all`
- Ensure you run from `src/` directory

### 3) `PySoundFile failed. Trying audioread instead`

- Usually non-fatal fallback warning
- Optional fix: install system `libsndfile` and keep `soundfile` updated

### 4) Path confusion (`../data/...`)

- Run entrypoint from `src/`
- Or refactor to absolute paths based on `Path(__file__).resolve()`

## Development Notes

- `.env` is gitignored (recommended)
- Do not hardcode API keys in source/config
- Current training/evaluation scripts are placeholders and should be implemented next

## Suggested Next Steps

1. Implement `BirdSoundDataset` in `src/dataset.py`
2. Implement model builder in `src/model.py`
3. Add real training loop + validation in `src/train.py`
4. Add confusion matrix and metrics in `src/evaluate.py`
5. Add `predict.py` for single-file inference


## Missing Pipeline Pieces (Planned)

The repository already has placeholders for model training, evaluation, and inference. The sections below define what should be added next.

### 1) Labeling + Metadata Builder (new utility)

Goal:
- Build a single metadata file for training.

Suggested output:
- `data/metadata.csv`

Suggested columns:
- `file_path`
- `species`
- `label` (e.g., song/call/alarm/unknown)
- `split` (train/val/test)
- `duration_sec`
- `sample_rate`

Why this is needed:
- Central source of truth for data loading and reproducible experiments.

### 2) Dataset + DataLoaders (`src/dataset.py`)

Implement:
- `BirdSoundDataset(Dataset)`
- `get_dataloaders(batch_size, num_workers, image_size)`

Expected behavior:
- Load spectrogram `.png` or `.npy`
- Encode labels to integer IDs
- Return `(tensor, label)`
- Create train/val/test DataLoaders

### 3) Model Factory (`src/model.py`)

Implement:
- `build_model(num_classes, backbone="efficientnet_b0", pretrained=True)`
- `save_checkpoint(...)`
- `load_checkpoint(...)`

Expected behavior:
- Replace classifier head to match `num_classes`
- Return PyTorch model ready for training or inference

### 4) Training Loop (`src/train.py`)

Implement:
- `train_one_epoch(...)`
- `validate(...)`
- `run_training(...)`

Recommended features:
- Optimizer + scheduler
- Early stopping
- Best-checkpoint saving to `models/`
- Metric logging (loss, accuracy, macro-F1)

Suggested outputs:
- `models/best.pt`
- `outputs/history.csv`
- `outputs/loss_curve.png`

### 5) Evaluation Pipeline (`src/evaluate.py`)

Implement:
- `evaluate_model(...)`
- `plot_confusion_matrix(...)`
- `generate_report(...)`

Suggested outputs:
- `outputs/confusion_matrix.png`
- `outputs/classification_report.txt`
- Per-class precision/recall/F1 table

### 6) Prediction Pipeline (`src/predict.py`)

Implement:
- `predict_species(audio_path, model_path)`
- Optional `predict_batch(input_dir, model_path)`

Expected behavior:
- Run same preprocessing + feature extraction as training
- Return top-k class probabilities
- Save predictions to `outputs/predictions.csv`

### 7) Config-Driven Runs (recommended)

Add more settings into `configs/config.yaml`, for example:
- audio params (`target_sr`, `chunk_sec`, `n_mels`)
- augmentation params
- training params (`batch_size`, `epochs`, `lr`)

Benefit:
- No hardcoded hyperparameters inside scripts.

### 8) Reproducibility + Quality Checks

Add:
- Global random seed setup
- Data leakage checks (same recording not in multiple splits)
- Minimum sample checks per class

Benefit:
- Stable and trustworthy model comparisons.

### 9) Optional Deployment Layer

Later you can add:
- Streamlit app for uploading audio and showing predictions
- Lightweight API wrapper for programmatic inference

## Suggested Implementation Order

1. `dataset.py`
2. `model.py`
3. `train.py`
4. `evaluate.py`
5. `predict.py`
6. config refinement + reproducibility checks

