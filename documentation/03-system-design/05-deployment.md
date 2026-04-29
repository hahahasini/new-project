# Deployment Architecture

> **Project**: PLACEHOLDER-PROJECT-NAME — Vitamin Deficiency Detection System  
> **Version**: 1.0.0 | **Last Updated**: PLACEHOLDER-YEAR

---

## Overview

This document describes the deployment architecture for PLACEHOLDER-PROJECT-NAME, covering the local development setup (primary deployment model), potential cloud deployment strategies, network architecture, and backup considerations.

See also: [Deployment Diagram](../diagrams/deployment.puml)

---

## 1. Local Development Deployment (Primary)

PLACEHOLDER-PROJECT-NAME is designed primarily for **local deployment**, ensuring maximum privacy by keeping all image data on the user's machine.

### 1.1 Component Placement

| Component | Host | Port | Process |
|:---|:---|:---:|:---|
| Frontend (React SPA) | localhost | 5173 | `npm run dev` → Vite dev server |
| Backend (FastAPI API) | localhost | 8000 | `uvicorn app.main:app --reload` |
| ML Models | localhost | N/A | Loaded into backend process memory at startup |
| Database | N/A | N/A | No database — configuration-driven data model |

### 1.2 Startup Sequence
```
1. Backend startup:
   cd backend
   pip install -r requirements.txt
   python -m uvicorn app.main:app --reload --port 8000
   
   → Loads 3 ML models (~3.9s total)
   → FastAPI app ready at http://localhost:8000
   → Swagger docs at http://localhost:8000/docs

2. Frontend startup:
   cd frontend
   npm install
   npm run dev
   
   → Vite dev server starts at http://localhost:5173
   → Hot Module Replacement enabled
```

### 1.3 Communication Architecture
```
Browser (localhost:5173)
  ├── HTTP GET → Vite Dev Server (serves React SPA)
  ├── HTTP POST/GET → FastAPI (localhost:8000/api/*)
  ├── HTTP POST → Overpass API (overpass-api.de) [external]
  └── HTTPS GET → CartoDB tiles (basemaps.cartocdn.com) [external]
```

CORS is configured to allow requests from the frontend origins:
- `http://localhost:5173`
- `http://localhost:3000`
- `http://127.0.0.1:5173`

---

## 2. Production Deployment (Optional)

### 2.1 Frontend Static Hosting

For production, the React SPA is built into static assets:
```bash
cd frontend
npm run build  # → dist/ folder with optimized HTML/CSS/JS
```

The `dist/` folder can be deployed to:
| Platform | Method | Cost |
|:---|:---|:---|
| Nginx | Serve static files with reverse proxy to backend | Free (self-hosted) |
| Vercel | Auto-deploy from Git; edge CDN | Free tier available |
| Netlify | Static site hosting with CI/CD | Free tier available |
| AWS S3 + CloudFront | S3 bucket with CDN | Pay-per-use |

### 2.2 Backend Deployment

The FastAPI backend requires a Python runtime with TensorFlow:

| Platform | Method | Notes |
|:---|:---|:---|
| **Docker** | Containerize with `Dockerfile` | Recommended for reproducibility; include model files in image |
| **AWS EC2** | Direct deployment on Linux instance | Requires 4GB+ RAM for models |
| **Google Cloud Run** | Serverless container hosting | Cold start includes model loading (~4s) |
| **Railway / Render** | Platform-as-a-Service | Simple deployment; may have memory limits |

### 2.3 Sample Docker Configuration
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
COPY backend/models/ ./models/
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2.4 Production Architecture
```
                    ┌────────────────────────┐
                    │   Load Balancer (Nginx) │
                    │   SSL Termination       │
                    └──────┬─────────────────┘
                           │
              ┌────────────┼────────────────┐
              │            │                │
     ┌────────▼───┐  ┌─────▼───────┐  ┌─────▼───────┐
     │ Uvicorn    │  │ Uvicorn     │  │ Uvicorn     │
     │ Worker 1   │  │ Worker 2    │  │ Worker 3    │
     │ (+ Models) │  │ (+ Models)  │  │ (+ Models)  │
     └────────────┘  └─────────────┘  └─────────────┘
```

**Note**: Each worker loads its own copy of the models, so memory scales linearly with workers.

---

## 3. Network Architecture

### 3.1 Request Flow
```
User Browser
  │
  ├─→ Frontend (localhost:5173 or CDN)
  │     Serves: HTML, CSS, JS, static assets
  │
  ├─→ Backend API (localhost:8000 or cloud)
  │     Accepts: multipart/form-data (images)
  │     Returns: JSON (analysis results)
  │     CORS: Restricted to allowed origins
  │
  ├─→ Overpass API (overpass-api.de)
  │     Sends: OverpassQL query (URL-encoded POST)
  │     Returns: JSON (hospital/clinic data)
  │     Note: Called directly from browser (no backend proxy)
  │
  └─→ CartoDB (basemaps.cartocdn.com)
        Fetches: Map tile images (PNG)
        Pattern: /{z}/{x}/{y}{r}.png
```

### 3.2 Ports & Protocols
| Service | Port | Protocol | TLS |
|:---|:---:|:---|:---:|
| Vite Dev Server | 5173 | HTTP/1.1 | No (dev) |
| FastAPI Backend | 8000 | HTTP/1.1 | No (dev) |
| Overpass API | 443 | HTTPS | Yes |
| CartoDB Tiles | 443 | HTTPS | Yes |
| Leaflet CDN | 443 | HTTPS | Yes |

---

## 4. Load Balancing Strategy

For local deployment, load balancing is not required. For production:

| Strategy | Configuration | Use Case |
|:---|:---|:---|
| **Single Worker** | `uvicorn app.main:app` | Development, low traffic |
| **Multiple Workers** | `uvicorn app.main:app --workers 4` | Medium traffic, multi-core CPU |
| **Gunicorn + Uvicorn** | `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app` | Production with process management |
| **Nginx Reverse Proxy** | Upstream to multiple Uvicorn instances | High availability, SSL, static file serving |

---

## 5. Backup & Disaster Recovery

### 5.1 What Needs Backup
| Asset | Size | Backup Method |
|:---|:---:|:---|
| ML Model files (`.keras`) | ~432 MB | Store in version control (Git LFS) or cloud storage |
| Source code | ~2 MB | Git repository (GitHub/GitLab) |
| Configuration (`config.py`, `.env`) | < 1 KB | Version control |
| Training notebooks | ~1.2 MB | Version control |

### 5.2 What Does NOT Need Backup
- User-uploaded images (processed in-memory, never stored)
- Session data (stateless architecture)
- Database (no database used)
- Cache (no caching layer)

### 5.3 Recovery Procedure
1. Clone repository from Git
2. Place model files in `backend/models/` (from backup storage)
3. Install Python dependencies: `pip install -r requirements.txt`
4. Install Node dependencies: `cd frontend && npm install`
5. Start backend: `uvicorn app.main:app --port 8000`
6. Start frontend: `npm run dev`
7. Verify: `curl http://localhost:8000/api/health`

---

## 6. System Requirements Summary

| Requirement | Minimum | Recommended |
|:---|:---:|:---:|
| Operating System | Linux / macOS / Windows | Linux (Ubuntu 22.04+) |
| CPU | 2 cores (x86_64) | 4+ cores |
| RAM | 2 GB | 4+ GB |
| Disk | 1 GB | 2+ GB |
| Python | 3.9+ | 3.11+ |
| Node.js | 18+ | 20+ LTS |
| GPU | Not required | NVIDIA CUDA (optional) |
| Internet | For Nearby Doctors only | Recommended |

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
