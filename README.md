ExperimentVault 🔬

A comprehensive MLOps platform for experiment tracking, versioning, and comparison. Track your machine learning experiments with full reproducibility, parameter management, and collaborative features.
Features

✨ Core Features:

📊 Experiment tracking with automatic Git integration
🔍 Side-by-side experiment comparison
📈 Metrics and parameters management
💾 Artifact storage and versioning
🏷️ Status tracking (running, completed, failed)
🔐 User and dataset version tracking
🎯 Fast REST API with filtering and search

Quick Start
Prerequisites

Python 3.8+
Node.js 16+
PostgreSQL 12+ (or SQLite for development)

Installation
1. Clone the repository:
bashgit clone https://github.com/yourusername/experimentvault.git
cd experimentvault
2. Backend Setup:
bashcd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configure .env:
DATABASE_URL=sqlite:///./test.db
UPLOAD_DIR=./uploads
Run backend:
bashuvicorn app.main:app --reload --port 8000
3. Frontend Setup:
bashcd frontend
npm install
npm start
Frontend runs on http://localhost:3000
4. Python Client Setup:
bashcd client
pip install -e .
Usage
Python Client Example
pythonfrom tracker import Experiment

# Create and track an experiment
exp = Experiment(name="v1_baseline", description="Initial model")
exp.log_params({"lr": 0.001, "epochs": 100, "batch_size": 32})

# Train model...
exp.log_metrics({"accuracy": 0.95, "f1": 0.92, "loss": 0.15})
exp.save_artifact("model", trained_model)
exp.log_file("plot", "confusion_matrix.png")

exp.end()  # Mark as completed
Using Decorator
pythonfrom tracker import track_experiment

@track_experiment(name="baseline_run")
def train_model(lr=0.001, epochs=100):
    # Parameters are logged automatically
    # Training code...
    return {"accuracy": 0.95, "f1": 0.92}

train_model(lr=0.001, epochs=50)
Project Structure
experimentvault/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── db.py
│   │   └── routes/
│   │       └── experiments.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── api.js
│   │   └── App.jsx
│   ├── package.json
│   └── public/
├── client/
│   ├── tracker/
│   │   ├── __init__.py
│   │   ├── client.py
│   │   └── decorators.py
│   ├── setup.py
│   └── requirements.txt
└── README.md
API Endpoints
MethodEndpointDescriptionPOST/api/experimentsCreate experimentGET/api/experimentsList experiments with filtersGET/api/experiments/:idGet experiment detailsPATCH/api/experiments/:idUpdate params/metrics/statusPOST/api/experiments/compareCompare multiple experimentsDELETE/api/experiments/:idDelete experiment
Technology Stack
Backend:

FastAPI
SQLAlchemy
PostgreSQL / SQLite
Uvicorn

Frontend:

React 18
React Router
Axios
CSS3

Client SDK:

Python 3.8+
Requests
Git integration

Configuration
Environment Variables
Backend (.env):
DATABASE_URL=sqlite:///./test.db
UPLOAD_DIR=./uploads
Frontend (.env):
REACT_APP_API_URL=http://localhost:8000/api
Running All Services
Terminal 1 - Backend:
bashcd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
Terminal 2 - Frontend:
bashcd frontend
npm start
Terminal 3 - Client Tests:
bashcd client
python test.py
Development
Backend Development

Hot reload enabled with --reload
API docs at http://localhost:8000/docs
Database schema auto-migration on startup

Frontend Development

React Fast Refresh enabled
CSS-in-JS with Tailwind (optional)
Component structure in src/components/

Client SDK Development

Editable install with pip install -e .
Git info auto-detection
Decorator support for zero-config tracking

Future Roadmap

 S3/Cloud storage integration
 Advanced analytics dashboard
 Hyperparameter optimization suggestions
 Experiment notifications
 Team collaboration features
 ML model registry
 Integration with popular ML frameworks

Contributing
Contributions are welcome! Please:

Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit changes (git commit -m 'Add amazing feature')
Push to branch (git push origin feature/amazing-feature)
Open a Pull Request

License
This project is licensed under the MIT License - see LICENSE file for details.
Support
Need help? Open an issue on GitHub or check our documentation.

Built with ❤️ for ML Engineers
