# CLIP Colab

A Python package for generating image descriptions and prompts using CLIP and BLIP models. Converted from a Google Colab notebook to a standalone package.

## What it Does

This package helps you:
- Generate detailed text descriptions from images
- Create optimized prompts for image generation models like Stable Diffusion
- Process images in batch for efficient workflow
- Leverage both BLIP (for image captioning) and CLIP (for detailed analysis)

## Installation

1. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

2. Install the package:
```bash
pip install -r requirements.txt
pip install -e .
```

## Configuration

You can configure the package in several ways, in order of precedence:

1. Environment variable:
```bash
export CLIP_CONFIG_PATH=/path/to/your/config.json
```

2. User config file:
```bash
~/.clip_colab/config.json
```

3. Local config file:
```bash
./clip_colab_config.json
```

Example config.json:
```json
{
    "CLIP_MODEL": "ViT-L-14/openai",
    "CAPTION_MODEL": "blip-large",
    "MODELS_CACHE_DIR": "/path/to/models",
    "OUTPUT_DIR": "outputs"
}
```

Default models (if no config provided):
- Caption Model: 'blip-large'
- CLIP Model: 'ViT-L-14/openai'

Available caption models:
- 'blip-base'
- 'blip-large'
- 'git-large-coco'

Available CLIP models:
- 'ViT-L-14/openai'
- 'ViT-H-14/laion2b_s32b_b79k'

## Usage

Basic usage:
```python
from clip_colab import setup, image_to_prompt
from PIL import Image

# Initialize models
setup()

# Process single image
image = Image.open("your_image.jpg")
prompt = image_to_prompt(image, mode='best')
print(prompt)
```

For batch processing:
```python
from clip_colab import batch_process

# Process all images in a directory
batch_process.process_directory("path/to/images", output_file="prompts.txt")
```

## System Requirements

- Python 3.7+
- CUDA-capable GPU recommended for faster processing
- Minimum 8GB RAM (16GB+ recommended for larger models)
- ~10GB disk space for model downloads

## Notes

- For Stable Diffusion 1.X compatibility, use `ViT-L-14/openai`
- For Stable Diffusion 2.0, use `ViT-H-14/laion2b_s32b_b79k`
- Memory usage can be high with larger models
- First run will download models (~10GB total)
- Processing time varies by GPU/CPU capability
