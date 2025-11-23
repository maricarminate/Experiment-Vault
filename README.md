# ExperimentVault 🔬

> A comprehensive MLOps platform for experiment tracking, versioning, and comparison built with Python, React, and FastAPI.

Track your machine learning experiments with full reproducibility, automatic Git integration, parameter management, and side-by-side comparison features.

## ✨ Features

- **🎯 Experiment Tracking**: Log parameters, metrics, and artifacts automatically
- **📊 Git Integration**: Auto-detect branch and commit for full reproducibility
- **🔍 Comparison Dashboard**: Compare multiple experiments side-by-side
- **💾 Artifact Management**: Store models, plots, and any binary data
- **🏷️ Status Tracking**: Monitor experiment status (running, completed, failed)
- **👤 User Management**: Track which user ran each experiment
- **⚡ REST API**: Fast, filterable API with comprehensive endpoints
- **🎨 Modern UI**: Clean React dashboard with real-time updates
- **🐍 Python Client**: Simple decorator-based tracking for Python projects

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+ (or SQLite for development)

### 1️⃣ Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env`:
```env
DATABASE_URL=sqlite:///./test.db
UPLOAD_DIR=./uploads
```

Start backend:
```bash
uvicorn app.main:app --reload --port 8000
```

API docs available at `http://localhost:8000/docs`

### 2️⃣ Frontend Setup

```bash
cd frontend
npm install
npm start
```

Access at `http://localhost:3000`

### 3️⃣ Python Client Setup

```bash
cd client
pip install -e .
```

## 📖 Usage Examples

### Basic Experiment Tracking

```python
from tracker import Experiment

# Create experiment
exp = Experiment(
    name="model_v1",
    description="Baseline model with default parameters"
)

# Log hyperparameters
exp.log_params({
    "learning_rate": 0.001,
    "epochs": 100,
    "batch_size": 32,
    "optimizer": "adam"
})

# Train your model...
# model = train(...)

# Log metrics
exp.log_metrics({
    "accuracy": 0.95,
    "f1_score": 0.92,
    "loss": 0.15,
    "precision": 0.93,
    "recall": 0.91
})

# Save artifacts
exp.save_artifact("model", model)
exp.log_file("confusion_matrix", "plots/cm.png")
exp.log_file("training_log", "logs/train.log")

# Mark as completed
exp.end("completed")
```

### Using Decorators (Zero-Config)

```python
from tracker import track_experiment

@track_experiment(name="hyperparameter_search")
def train_model(learning_rate=0.001, epochs=100, batch_size=32):
    # Parameters logged automatically
    # Your training code...
    return {
        "accuracy": 0.95,
        "f1": 0.92,
        "training_time": 125.5
    }

# Metrics logged automatically from return value
train_model(learning_rate=0.0005, epochs=50)
```

### Frontend Dashboard

1. **List View**: See all experiments with filters
2. **Detail View**: Inspect experiment parameters and metrics
3. **Compare View**: Side-by-side comparison of multiple experiments
4. **Highlight Best**: Automatically highlights best metric values

## 📁 Project Structure

```
Experiment-Vault/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app
│   │   ├── db.py             # Database config
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── schemas.py        # Pydantic schemas
│   │   └── routes/
│   │       └── experiments.py # API endpoints
│   ├── requirements.txt
│   ├── .env
│   └── .gitignore
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── ExperimentList.jsx
│   │   │   ├── ExperimentDetail.jsx
│   │   │   ├── ExperimentCompare.jsx
│   │   │   ├── ExperimentList.css
│   │   │   ├── ExperimentDetail.css
│   │   │   └── ExperimentCompare.css
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── api.js
│   │   └── index.js
│   ├── package.json
│   ├── .env
│   └── .gitignore
│
├── client/
│   ├── tracker/
│   │   ├── __init__.py
│   │   ├── client.py         # Main client class
│   │   └── decorators.py     # Decorator utilities
│   ├── setup.py
│   ├── requirements.txt
│   └── .gitignore
│
├── README.md
├── .gitignore
└── LICENSE
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/experiments` | Create new experiment |
| `GET` | `/api/experiments` | List experiments (with filters) |
| `GET` | `/api/experiments/:id` | Get experiment details |
| `PATCH` | `/api/experiments/:id` | Update parameters/metrics/status |
| `POST` | `/api/experiments/compare` | Compare multiple experiments |
| `DELETE` | `/api/experiments/:id` | Delete experiment |

### Query Parameters

```bash
# List with filters
GET /api/experiments?skip=0&limit=20&status=completed&user=john

# Filter by status: running, completed, failed
GET /api/experiments?status=completed

# Filter by user
GET /api/experiments?user=john
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL/SQLite** - Database
- **Uvicorn** - ASGI server

### Frontend
- **React 18** - UI library
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **date-fns** - Date formatting
- **CSS3** - Styling

### Client SDK
- **Python 3.8+** - Language
- **Requests** - HTTP library
- **Git** - Auto-detection of branch/commit

## 🔧 Configuration

### Backend Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/experiment_vault
# or
DATABASE_URL=sqlite:///./test.db

# Storage
UPLOAD_DIR=./uploads
```

### Frontend Environment Variables

```env
REACT_APP_API_URL=http://localhost:8000/api
```

### Client SDK

```python
# Custom backend URL
exp = Experiment(
    name="my_exp",
    backend_url="http://custom-server:8000"
)

# Disable auto-git detection
exp = Experiment(name="my_exp", auto_git=False)
```

## ▶️ Running All Services

Open 3 terminals:

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

**Terminal 3 - Test Client:**
```bash
cd client
python -c "
from tracker import Experiment
exp = Experiment(name='test')
exp.log_params({'lr': 0.001})
exp.log_metrics({'acc': 0.95})
exp.end()
"
```

## 🧪 Testing

### Backend API
Visit `http://localhost:8000/docs` for interactive Swagger UI

### Frontend
Access `http://localhost:3000` in your browser

### Client
```bash
cd client
python test.py
```

## 📚 Database Setup

### Using SQLite (Development)
```env
DATABASE_URL=sqlite:///./test.db
```

### Using PostgreSQL (Production)

```bash
# Create user and database
sudo -u postgres psql
CREATE USER vault_user WITH PASSWORD 'secure_password';
CREATE DATABASE experiment_vault OWNER vault_user;
\q
```

Then set in `.env`:
```env
DATABASE_URL=postgresql://vault_user:secure_password@localhost:5432/experiment_vault
```

## 🚦 Status Codes

- `running` - Experiment in progress
- `completed` - Experiment finished successfully
- `failed` - Experiment failed

## 🐛 Troubleshooting

**Connection refused on port 8000:**
```bash
# Check if port is in use
lsof -i :8000

# Kill process using port
kill -9 <PID>
```

**PostgreSQL authentication failed:**
```bash
# Use SQLite instead for development
DATABASE_URL=sqlite:///./test.db
```

**Frontend can't connect to backend:**
```bash
# Ensure backend is running on port 8000
# Check REACT_APP_API_URL in frontend/.env
```

## 🗺️ Roadmap

- [ ] S3/Cloud storage integration
- [ ] Advanced analytics and insights
- [ ] Hyperparameter optimization recommendations
- [ ] Email notifications for completed experiments
- [ ] Team collaboration and sharing
- [ ] Model registry and versioning
- [ ] Integration with TensorBoard
- [ ] Experiment scheduling and automation
- [ ] Docker Compose setup

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Created with ❤️ for ML Engineers and Data Scientists

## 📞 Support

- 📖 [Documentation](./docs)
- 🐛 [Issue Tracker](https://github.com/maricarminate/Experiment-Vault/issues)
- 💬 [Discussions](https://github.com/maricarminate/Experiment-Vault/discussions)

---

**Made with ❤️ for the ML community**
