# Quick Start - Development Guide

## For Developers

### Initial Setup
```bash
# Clone repository
git clone <repository-url>
cd Md_File_Reader

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Running the Application
```bash
# Development mode (debug ON - DEFAULT)
python run.py

# Or use CLI
docpresent start --debug

# Production/Release mode (debug OFF)
set PRODUCTION=true
python run.py

# Custom host/port
docpresent start --host 0.0.0.0 --port 5000
```

### Code Quality
```bash
# Format code
black doc_viewer/

# Sort imports
isort doc_viewer/

# Lint
flake8 doc_viewer/

# Type check
mypy doc_viewer/

# Run all pre-commit hooks
pre-commit run --all-files
```

### Testing
```bash
# Run all tests
pytest

# With coverage report
pytest --cov=doc_viewer --cov-report=html

# Run specific test file
pytest tests/test_toc.py

# Run specific test
pytest tests/test_toc.py::test_toc_basic_structure

# Watch mode (requires pytest-watch)
ptw
```

### Building
```bash
# Build Python package
python -m build

# Build executable
pyinstaller OmniDoc.spec

# Both will create artifacts in dist/
```

### Common Tasks
```bash
# Check what would change before formatting
black --check doc_viewer/

# Show what isort would change
isort --check-only --diff doc_viewer/

# Generate coverage report
pytest --cov=doc_viewer --cov-report=html
# Open htmlcov/index.html in browser

# Clean build artifacts
rm -rf build/ dist/ *.egg-info/  # Linux/Mac
rmdir /s build dist             # Windows
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes, then commit
git add .
git commit -m "feat: add amazing feature"
# Pre-commit hooks run automatically

# Push
git push origin feature/my-feature

# Create Pull Request on GitHub
```

### Environment Variables
```bash
# Production mode (debug OFF)
export PRODUCTION=true         # Linux/Mac
set PRODUCTION=true           # Windows

# Debug mode is ON by default, no env var needed
```

## For Users

### Installation
```bash
# Install from source
pip install .

# Install in editable mode (for development)
pip install -e .
```

### Usage
```bash
# Start server
docpresent start

# With options
docpresent start --host localhost --port 8000 --debug

# Show version
docpresent --version
```

### Quick Launch (Windows)
```bash
# Double-click start.bat
# Or run:
start.bat
```

## Troubleshooting

### Import Errors
```bash
# Ensure virtual environment is activated
# Check Python version (3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Test Failures
```bash
# Clear pytest cache
pytest --cache-clear

# Run with verbose output
pytest -vv

# Run specific failing test
pytest tests/test_file.py::test_name -vv
```

### Pre-commit Issues
```bash
# Skip hooks temporarily
git commit --no-verify -m "message"

# Update hooks
pre-commit autoupdate

# Clean and reinstall
pre-commit clean
pre-commit install
```

### Port Already in Use
```bash
# Windows: Find process
netstat -ano | findstr :8000
taskkill /PID <pid> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

## Project Structure
```
Md_File_Reader/
├── doc_viewer/          # Main package
│   ├── app.py          # Flask application
│   ├── cli.py          # Command-line interface
│   ├── core/           # Core rendering
│   ├── features/       # Feature modules
│   └── templates/      # HTML templates
├── tests/              # Test suite
├── doc/                # Documentation
├── doc_gallery/        # Sample documents
└── releases/           # Release artifacts
```

## Resources
- **Documentation**: `doc/USER_GUIDE.md`
- **Contributing**: `CONTRIBUTING.md`
- **Changelog**: `doc/CHANGELOG.md`
- **Build Guide**: `doc/BUILD.md`
- **Standards**: `doc/OPEN_SOURCE_STANDARDS.md`
