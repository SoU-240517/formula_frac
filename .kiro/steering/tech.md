# Technology Stack

## Core Technologies
- **Python 3.12+**: Primary programming language
- **PyQt6**: GUI framework for the main application interface
- **Virtual Environment**: `venv` for dependency isolation

## Key Libraries
- `PyQt6.QtWidgets`: UI components (QApplication, QMainWindow, QLineEdit, etc.)
- `PyQt6.QtGui`: Graphics handling (QImage, QPixmap)
- `PyQt6.QtCore`: Threading and signals (QThread, pyqtSignal, QTimer)
- `math` & `cmath`: Mathematical operations for complex number calculations

## Development Environment
- **Language**: Japanese comments and documentation
- **IDE**: VSCode (excluded from version control)
- **Version Control**: Git with standard Python .gitignore

## Common Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies (if requirements.txt exists)
pip install -r requirements.txt
```

### Running the Application
```bash
# Run main application
python main.py
```

### Development
```bash
# Install PyQt6 (main dependency)
pip install PyQt6
```

## Architecture Notes
- Multi-threaded design using QThread for non-blocking image generation
- Safe expression evaluation using restricted eval() with controlled namespace
- Signal-slot pattern for UI updates and thread communication