# 🏙️ AI-Powered Community Problem Mapper

[![Django](https://img.shields.io/badge/Django-5.0.6-092E20?logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15.1-a30000?logo=django)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> An AI-powered Django application that automatically classifies, deduplicates, clusters, and prioritizes citizen complaints for smart city management.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [AI Pipeline](#ai-pipeline)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Performance Metrics](#performance-metrics)
- [Contributing](#contributing)
- [License](#license)
- [Team](#team)

---

## 🎯 Overview

### Problem Statement
Municipalities receive thousands of citizen complaints daily through scattered channels. Manual triage doesn't scale — duplicates are missed, hotspots go unnoticed, and urgent issues get buried.

### Solution
A complete system where every complaint is automatically enriched by an AI pipeline the moment it's submitted, before appearing on an authority dashboard. The system:
- **Classifies** complaints into 9 categories with 93% accuracy
- **Detects duplicates** using multi-tier similarity
- **Identifies hotspots** through DBSCAN clustering
- **Estimates priority** using Gemini LLM
- **Generates summaries** for clustered complaints

---

## ✨ Features

### For Citizens
- ✅ Submit complaints with text + GPS location + optional image
- ✅ View all submitted complaints
- ✅ Track complaint status (Received → In Review → In Progress → Resolved)
- ✅ Rate-limited submissions (10/hour)

### For Authorities/Admins
- ✅ **Dashboard**: Stats, charts, and hotspot map
- ✅ **Manage Complaints**: View grouped duplicates with AI summaries
- ✅ **Status Management**: One-click Resolved/Received toggle
- ✅ **Soft Delete**: Hide complaints from views (auditable)
- ✅ **Hotspot Detection**: AI-identified problem areas with summaries

### AI Features
- ✅ **Local Classification**: Logistic Regression (93% CV accuracy)
- ✅ **Multi-tier Duplicate Detection**: Location + Category + Embedding
- ✅ **Hotspot Clustering**: DBSCAN on GPS coordinates
- ✅ **Priority Scoring**: Gemini API (1-10 urgency)
- ✅ **Cluster Summarization**: Gemini API (AI-generated summaries)
- ✅ **Resilience**: Graceful degradation when Gemini unavailable

---

## 🛠️ Technology Stack

### Backend
| Category | Technology | Version |
|----------|------------|---------|
| Framework | Django | 5.0.6 |
| API | Django REST Framework | 3.15.1 |
| Database | PostgreSQL | 15+ |
| Auth | JWT (SimpleJWT) | - |
| AI/ML | scikit-learn | 1.3.0 |
| Embeddings | Sentence Transformers | 2.2.2 |
| LLM | Google Gemini API | - |

### Frontend
| Category | Technology |
|----------|------------|
| CSS | Bootstrap 5 |
| Charts | Chart.js |
| Maps | Leaflet + OpenStreetMap |
| JavaScript | Vanilla JS |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CITIZEN SUBMITS COMPLAINT (Text + GPS)                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    DJANGO + DRF BACKEND (JWT Auth)                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AI ENRICHMENT PIPELINE (Async)                          │
│                                                                             │
│    1. Embedding (Sentence Transformers) → 384-dim vector                   │
│    2. Duplicate Detection (Cosine + Location) → Multi-tier                 │
│    3. Classification (Logistic Regression) → 1 of 9 categories             │
│    4. Clustering (DBSCAN) → Hotspot detection                              │
│    5. Priority (Gemini API) → 1-10 urgency score                          │
│    6. Summary (Gemini API) → AI-generated hotspot summary                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AUTHORITY DASHBOARD                                     │
│     • Manage Complaints (grouped with duplicates)                         │
│     • Hotspot Map (Leaflet)                                               │
│     • Stats & Charts (Chart.js)                                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🤖 AI Pipeline

### 1. Embedding Generation
- **Model**: `paraphrase-multilingual-MiniLM-L12-v2`
- **Output**: 384-dim semantic vector
- **Time**: ~5 seconds (first load), ~1-2 seconds (subsequent)
- **Type**: LOCAL, FREE, OFFLINE

### 2. Duplicate Detection
- **Geo Prefilter**: 0.5km radius
- **Multi-tier System**:
  - Tier 1: Location <50m + Same Category → Immediate duplicate
  - Tier 2: Same Category → Lenient threshold (0.65)
  - Tier 3: Different Category → Strict threshold (0.85)
- **Time**: <100ms
- **Type**: LOCAL, FREE, OFFLINE

### 3. Classification
- **Primary**: Logistic Regression (trained on 450 examples)
  - 93.11% CV Accuracy (±3.54%)
  - 94.44% Held-out Accuracy
- **Fallback**: Gemini API (confidence < 0.35)
- **Time**: ~2ms (local), ~1-2 seconds (Gemini)

### 4. Clustering (Hotspot Detection)
- **Algorithm**: DBSCAN (scikit-learn)
- **Distance**: Haversine (GPS coordinates)
- **Parameters**: eps=0.3km, min_samples=3
- **Time**: <100ms
- **Type**: LOCAL, FREE, OFFLINE

### 5. Priority Scoring
- **Model**: Gemini API (few-shot prompted)
- **Output**: 1-10 urgency score
- **Time**: ~1-2 seconds
- **Type**: CLOUD (no ground-truth labels for training)

### 6. Cluster Summarization
- **Model**: Gemini API (few-shot prompted)
- **Output**: 2-4 sentence natural-language summary
- **Time**: ~1-2 seconds
- **Cost Control**: Only regenerated when cluster size crosses threshold

---

## 📦 Installation

### Prerequisites

- Python 3.12+
- PostgreSQL 15+
- Git
- Virtual Environment (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ai-community-problem-mapper.git
cd ai-community-problem-mapper
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Setup PostgreSQL Database

```sql
CREATE DATABASE smart_city_mapper;
CREATE USER youruser WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE smart_city_mapper TO youruser;
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=smart_city_mapper
DB_USER=youruser
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

# Gemini API
GEMINI_API_KEY=your-gemini-api-key

# JWT
ACCESS_TOKEN_LIFETIME_MINUTES=60
REFRESH_TOKEN_LIFETIME_DAYS=7

# AI Pipeline
SENTENCE_TRANSFORMER_MODEL=paraphrase-multilingual-MiniLM-L12-v2
GEMINI_MODEL_NAME=gemini-3.5-flash-lite

# Duplicate Detection
DUPLICATE_SIMILARITY_THRESHOLD=0.85
DUPLICATE_SIMILARITY_SAME_CATEGORY_THRESHOLD=0.65
DUPLICATE_GEO_RADIUS_KM=0.5
DUPLICATE_EXACT_LOCATION_RADIUS_KM=0.05
DUPLICATE_SIMILARITY_EXACT_LOCATION_THRESHOLD=0.55

# Clustering
CLUSTERING_WINDOW_DAYS=90
DBSCAN_EPS_KM=0.3
DBSCAN_MIN_SAMPLES=3
HOTSPOT_MIN_COMPLAINTS=5

# Local Classifier
LOCAL_CLASSIFIER_CONFIDENCE_THRESHOLD=0.35

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

### Step 6: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 7: Create Superuser

```bash
python manage.py createsuperuser
```

### Step 8: Train the Classifier

```bash
python scripts/train_classifier.py
```

### Step 9: Run the Server

```bash
python manage.py runserver
```

### Step 10: Access the Application

- **Home**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **API**: http://localhost:8000/api/

---

## 🗂️ Project Structure

```
ai-community-problem-mapper/
├── apps/
│   ├── accounts/          # User authentication & roles
│   │   ├── models.py      # Custom User model (citizen/authority/admin)
│   │   ├── views.py       # Login, registration, profile
│   │   └── permissions.py # Role-based permissions
│   ├── ai_engine/         # AI/ML pipeline
│   │   ├── services/
│   │   │   ├── embedding_service.py      # Sentence Transformers
│   │   │   ├── duplicate_service.py      # Duplicate detection
│   │   │   ├── classification_service.py # Gemini classification (fallback)
│   │   │   ├── local_classifier_service.py # Logistic Regression
│   │   │   ├── clustering_service.py     # DBSCAN
│   │   │   ├── priority_service.py       # Gemini priority scoring
│   │   │   ├── summarization_service.py  # Gemini summarization
│   │   │   └── enrichment_service.py     # Orchestrator
│   │   ├── ml_data/
│   │   │   └── training_data.py          # 450 labeled examples
│   │   └── ml_models/
│   │       └── classifier.joblib         # Trained model
│   ├── complaints/        # Complaint management
│   │   ├── models.py      # Complaint, Cluster, StatusHistory
│   │   ├── views.py       # CRUD, status update, soft delete
│   │   ├── serializers.py # API serializers
│   │   └── filters.py     # Filtering for manage page
│   ├── dashboard/         # Authority dashboard
│   │   ├── views.py       # Stats, hotspots, charts
│   │   └── serializers.py # Dashboard data
│   └── common/            # Shared utilities
│       └── validators.py  # Image validation, etc.
├── config/
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   └── exceptions.py      # Custom exception handlers
├── static/                # Static files (CSS, JS)
│   ├── complaints/
│   │   └── js/
│   │       ├── manage.js      # Manage page logic
│   │       └── location_picker.js # Map integration
│   └── accounts/
│       └── js/
│           └── auth.js        # Authentication
├── templates/             # HTML templates
│   ├── complaints/
│   │   ├── submit.html    # Complaint submission form
│   │   └── manage.html    # Authority manage page
│   └── dashboard/
│       └── base.html      # Base template
├── scripts/
│   ├── train_classifier.py   # Model training script
│   └── check_diversity.py    # Dataset diversity checker
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
├── manage.py              # Django management script
└── README.md              # This file
```

---

## 🔧 Configuration

### Important Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `DUPLICATE_SIMILARITY_THRESHOLD` | 0.85 | Strict threshold for different categories |
| `DUPLICATE_SIMILARITY_SAME_CATEGORY_THRESHOLD` | 0.65 | Lenient threshold for same category |
| `DUPLICATE_GEO_RADIUS_KM` | 0.5 | Max distance for duplicate check |
| `DUPLICATE_EXACT_LOCATION_RADIUS_KM` | 0.05 | 50m short-circuit radius |
| `DBSCAN_EPS_KM` | 0.3 | Max distance for clustering |
| `DBSCAN_MIN_SAMPLES` | 3 | Minimum complaints per cluster |
| `LOCAL_CLASSIFIER_CONFIDENCE_THRESHOLD` | 0.35 | Fallback to Gemini below this |
| `GEMINI_MODEL_NAME` | gemini-3.5-flash-lite | Gemini model |

---

## 🚀 Usage

### For Citizens

1. **Sign Up/Login**: Create an account or login
2. **Submit Complaint**: Fill in description, location, optional image
3. **Track Status**: View complaints and their status
4. **Receive Updates**: Status changes appear in real-time

### For Authorities/Admins

1. **Login**: Use authority/admin credentials
2. **Dashboard**: View stats, charts, and hotspot map
3. **Manage Complaints**: View grouped complaints with duplicates
4. **Toggle Status**: Mark complaints as Resolved/Received
5. **Soft Delete**: Remove complaints from views (auditable)
6. **Hotspot View**: Click on hotspots to see AI-generated summaries

---

## 📡 API Documentation

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Login (JWT) |
| POST | `/api/auth/refresh/` | Refresh JWT |

### Complaints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/complaints/` | Submit complaint (citizen) |
| GET | `/api/complaints/` | List complaints (role-scoped) |
| GET | `/api/complaints/{id}/` | Get complaint details |
| PATCH | `/api/complaints/{id}/status/` | Update status (authority/admin) |
| DELETE | `/api/complaints/{id}/delete/` | Soft delete (authority/admin) |
| GET | `/api/complaints/manage/` | Authority manage list |

### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/stats/` | Dashboard statistics |
| GET | `/api/dashboard/hotspots/` | Hotspot map data |

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.complaints

# Run with verbosity
python manage.py test -v 2
```

### Check Model Diversity

```bash
python scripts/check_diversity.py
```

### Retrain Model

```bash
# After adding new training examples
python scripts/train_classifier.py
```

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Training Examples** | 450 (50 per category) |
| **Unique Words** | 2,566 |
| **CV Accuracy** | 93.11% (±3.54%) |
| **Held-out Accuracy** | 94.44% |
| **Processing Time** | <10 seconds |
| **Embedding Dimension** | 384 |
| **Categories** | 9 |
| **Duplicate Detection** | 3-tier system |
| **Clustering Algorithm** | DBSCAN (eps=0.3km, min_samples=3) |

---

## 🎯 Key Design Decisions

| Decision | Why |
|----------|-----|
| **Local + Cloud Hybrid** | Removes Gemini from critical path; handles 90%+ calls locally |
| **English-only** | Roman Urdu embeddings were unreliable |
| **450 examples only** | Quality over quantity — 0 repeated patterns |
| **DBSCAN over K-Means** | No predefined clusters; explicit noise handling |
| **LLM for Priority/Summaries** | No ground-truth labels for priority; generative task for summarization |
| **Soft Delete only** | Citizen reports should never be hard-deleted |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

### Project Lead
- **Abdul Quddous** — [GitHub](https://github.com/abdulquddous)

### Developer
- **Abdur Rafay Akbar** — [GitHub](https://github.com/abdurrafayakbar)

### Mentors
- GIKI AI Bootcamp Faculty

---

## 🙏 Acknowledgments

- **GIKI AI Bootcamp** — For providing the platform and guidance
- **Google Gemini** — For LLM capabilities
- **Sentence Transformers** — For embedding models
- **scikit-learn** — For ML algorithms
- **OpenStreetMap** — For map data

---

## 📞 Contact

For questions or support, please open an issue on GitHub or contact the team.

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/yourusername/ai-community-problem-mapper.git
cd ai-community-problem-mapper

# Setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your settings

# Setup DB
python manage.py migrate
python manage.py createsuperuser

# Train model
python scripts/train_classifier.py

# Run
python manage.py runserver
```

---

**Built with ❤️ at GIKI AI Bootcamp**