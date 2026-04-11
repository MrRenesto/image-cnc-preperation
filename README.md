# CNC Image Preparation Tool

A simple Python application for converting images into line art suitable for CNC wood carving.

## Features (MVP)
- Load images (JPG, PNG, BMP)
- Convert to black & white
- Apply Canny edge detection
- Save processed images as PNG

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MrRenesto/image-cnc-preperation.git
cd image-cnc-preperation
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Quick Start (Windows)
1. Run `create_shortcut.ps1` to create a desktop shortcut
2. Double-click **CNC Image Tool** on your desktop to launch

### Manual Start
Run the application:
```bash
python src/main.py
# or simply double-click launch.bat
```

### Workflow:
1. Click **Load Image** to select an image file
2. Click **Convert to B&W** to convert the image to black & white
3. Click **Detect Edges** to apply Canny edge detection
4. Click **Select Object (ROI)** and drag a rectangle around your object
5. Click **Generate Line Art** to extract contour-based line art (outer + inner details)
6. Click **Save PNG** to export the processed image

## Requirements
- Python 3.8 or higher
- OpenCV
- NumPy
- Pillow

## Future Enhancements
See [todo.md](todo.md) for planned features and improvements.

## License
Apache License 2.0
