# Skin Cancer Analyzer — Agent Guidance

## Stack
- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLAlchemy, Pydantic, JWT auth
- **ML**: PyTorch + torchvision, MobileNetV3-Small (consumer PC friendly)

## Directory Ownership
- `frontend/`, `backend/`, `ml/` — Nikola

## Key Commands

### Backend
```bash
cd backend
pip install -r requirements.txt
pytest -v                    # Run tests
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm test                     # Vitest (--watch on save)
npm run build                # Production build
```

### ML Training
```bash
cd ml
pip install -r requirements.txt
python prepare_dataset.py   # Download & preprocess HAM10000
python train.py             # Fine-tune MobileNetV3-Small
python export_model.py       # Save to ../backend/models/
pytest tests/                # Dataset and training tests
```

## Constraints
- Model must run on consumer hardware (no GPU assumed)
- Images: max 10MB, formats: jpg/png/jpeg
- Auth: JWT, 24h token expiry
- ML tests mock inference to avoid loading model on every test run

## Project Structure
```
skin-cancer-analyzer/
├── frontend/               # Next.js 14, TypeScript, Tailwind CSS
│   ├── src/app/           # App Router pages
│   ├── src/components/    # React components
│   └── src/__tests__/     # Vitest component tests
├── backend/                # FastAPI, SQLAlchemy, JWT auth
│   ├── app/
│   │   ├── routers/       # API endpoints
│   │   ├── models/        # SQLAlchemy models
│   │   └── core/          # Auth, config, schemas
│   └── tests/             # pytest unit/integration tests
├── ml/                    # MobileNetV3-Small, HAM10000 dataset
│   ├── src/               # Training scripts
│   ├── data/              # HAM10000 dataset
│   ├── models/            # Checkpoints
│   └── tests/             # pytest tests
└── docker-compose.yml     # Full stack
```

## API Endpoints

### Auth
- `POST /api/auth/register` — Create account
- `POST /api/auth/login` — Get JWT token

### Analysis
- `POST /api/analyze` — Upload image, get prediction (auth required)
- `GET /api/analyze/history` — Get user's past analyses (auth required)

## Skin Lesion Classes (HAM10000)
| Index | Class | Description |
|-------|-------|-------------|
| 0 | nv | Melanocytic nevi (benign) |
| 1 | mel | Melanoma (malignant) |
| 2 | bkl | Benign keratosis |
| 3 | vasc | Vascular lesions |
| 4 | bcc | Basal cell carcinoma |
| 5 | akiec | Actinic keratoses |
| 6 | df | Dermatofibroma |

## Version Control
- Commit incrementally after each completed feature/test/fix
- Push to remote after every commit (never batch multiple changes)
- Use `gh auth login` if not already authenticated
- Commit message format: `{type}: {brief description}`
  - Types: `feat`, `fix`, `test`, `docs`, `refactor`
- Create PRs with `gh pr create` after pushing feature branches
- Remote: `https://github.com/activatethefud/skin-cancer-analyzer`

## Documentation
- Update `README.md` incrementally as features are added
- Keep README in sync with actual commands and capabilities
- Document new API endpoints, environment variables, or constraints as added
