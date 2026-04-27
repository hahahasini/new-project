# 🔬 Vitamin Deficiency Detection System

An AI-powered system that detects vitamin deficiencies from images of **nails, tongues, and skin** using deep learning (CNN) models. Built with a **FastAPI** backend and a modern **React** frontend.

---

## 🏗️ Architecture

```
┌─────────────────┐     HTTP/JSON      ┌──────────────────┐
│   React Frontend │ ◄──────────────► │  FastAPI Backend   │
│   (Vite + CSS)   │    /api/analyze   │  (TensorFlow/Keras)│
└─────────────────┘                    └──────────────────┘
                                              │
                                       ┌──────┴──────┐
                                       │  ML Models   │
                                       │ (Nail,       │
                                       │ Tongue, Skin)│
                                       └─────────────┘
```

## 📂 Project Structure

```
├── backend/           # FastAPI REST API
│   ├── app/
│   │   ├── main.py         # App entry point
│   │   ├── config.py       # Settings & model config
│   │   ├── models/         # Pydantic schemas
│   │   ├── services/       # Business logic (classifier, predictor, diet)
│   │   ├── routers/        # API endpoints
│   │   └── utils/          # Image processing utilities
│   └── models/             # ML model weight files
├── frontend/          # React + Vite UI
│   └── src/
│       ├── components/     # UI components
│       └── services/       # API client
├── data/              # Training/test/validation datasets
├── notebooks/         # Jupyter notebooks for model training
└── docs/              # Project documentation & reports
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- TensorFlow model files (place in `backend/models/`)

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

The frontend runs on `http://localhost:5173` and the backend API on `http://localhost:8000`.

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/analyze` | Upload an image for analysis |
| `GET`  | `/api/health` | Health check |

## 🧠 Models

| Model | Body Part | Input Size | Classes |
|-------|-----------|------------|---------|
| Classifier | All | 224×224 | Nail, Skin, Tongue |
| Nail Model | Nails | 224×224 | No Deficiency, Iodine, Vit D |
| Tongue Model | Tongue | 224×224 | Vit B12, Iron |
| Skin Model | Skin | 224×224 | Vit D, Vit A |

## 📄 License

This project is for educational purposes.
