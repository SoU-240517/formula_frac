# Project Structure

## Root Directory
```
├── main.py              # Main application entry point
├── docs/                # Documentation
│   └── coding_guidelines.md  # Japanese coding standards
├── sample/              # Sample implementations and variations
│   ├── jules_frac/      # Complex fractal editor with MVC architecture
│   ├── kiro_frac/       # Advanced fractal editor with plugin system
│   └── max_frac/        # Additional fractal implementation
├── venv/                # Python virtual environment (excluded from git)
├── .gitignore           # Git ignore rules
└── .kiro/               # Kiro AI assistant configuration
    └── steering/        # AI guidance documents
```

## Code Organization Patterns

### Main Application (`main.py`)
- **Functions**: Utility functions for mathematical operations
  - `mandelbrot_point()`: Core fractal calculation
  - `complex_from_pixel()`: Coordinate transformation
  - `pixel_color()`: Color mapping
  - `generate_mandelbrot_image()`: Image generation
- **Classes**: 
  - `MandelbrotWorker`: Background thread for computation
  - `MandelbrotWindow`: Main GUI window
- **Entry Point**: `main()` function

### Sample Projects
- **jules_frac/**: Full MVC architecture with separate controllers, models, views
- **kiro_frac/**: Plugin-based system with comprehensive testing suite
- **max_frac/**: Minimal implementation example

## File Naming Conventions
- Snake_case for Python files and functions
- Descriptive names reflecting functionality
- Test files prefixed with `test_`
- Documentation in markdown format

## Key Directories to Understand
- `sample/`: Contains reference implementations showing different architectural approaches
- `docs/`: Project documentation, primarily in Japanese
- `.kiro/steering/`: AI assistant guidance documents (this directory)

## Development Notes
- Virtual environment should always be activated when working on the project
- Sample projects serve as both examples and testing grounds for different approaches
- Main application is intentionally simple while samples show more complex architectures