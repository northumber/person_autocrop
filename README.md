# person_autocrop
This is a Python script to auto-detect and auto-crop a person in a image.

This script uses **Tensorflow** and **SSD Mobilenet V2 (COCO)** to recognize people in a photo, then crop the photo to the single person.

![example](https://github.com/northumber/person_autocrop/assets/17114557/bd3d352a-de33-4583-bba3-62ea77b844ab)

### Specifications
- Windows and Linux command-line auto-install scripts
  - Creates automatically the Python virtual environment and install requirements
  - Downloads automatically the SSD Mobilenet V2 COCO model
- Supports GPU computing
- Images extension supported: .jpg, .jpeg, .png, .webp, .bmp
- Auto-crop a person if found
  - If there is more than one person in the photo, it will create more photos
  - Batch processing a input folder
- Option to save image in a specific format or save as input format

### Requirements
- Python 3.10 installed (with Python-pip)


## How to use
1. Download the repository
3. Just run the .bat or .sh scripts.
   - If Windows: `run.bat`
   - If Linux: `run.sh` (be sure to `chmod +x` the script)

## Manual installation and use
If the automatic script does not work or if you want to use the python script directly.

1. First, create a folder (name of your choice) and open a terminal in it.
2. Create a Python virtual environment:
   
`python -m venv venv`

3. Activate the environment:

   - If Windows: `./venv/Scripts/activate`
   - If Linux: `source venv/bin/activate`

4. Install the requirements:

`pip install -r requirements.txt`

5. Run the Python script `person_autocrop.py` with:

`python person_autocrop.py`
