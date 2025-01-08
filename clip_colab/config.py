import os
import json
from pathlib import Path

# Default values
DEFAULT_CONFIG = {
    "CLIP_MODEL": "ViT-L-14/openai",
    "CAPTION_MODEL": "blip-large",
    "MODELS_CACHE_DIR": None,  # Will use default HuggingFace cache
    "OUTPUT_DIR": "outputs"
}

def load_config():
    """Load config from various locations in order of precedence:
    1. Environment variable CLIP_CONFIG_PATH
    2. User home directory: ~/.clip_colab/config.json
    3. Current working directory: ./clip_colab_config.json
    4. Default values
    """
    config = DEFAULT_CONFIG.copy()
    
    # Check environment variable
    env_config = os.environ.get('CLIP_CONFIG_PATH')
    if env_config and os.path.exists(env_config):
        try:
            with open(env_config) as f:
                config.update(json.load(f))
            return config
        except Exception as e:
            print(f"Warning: Failed to load config from {env_config}: {e}")
    
    # Check home directory
    home_config = Path.home() / '.clip_colab' / 'config.json'
    if home_config.exists():
        try:
            with open(home_config) as f:
                config.update(json.load(f))
            return config
        except Exception as e:
            print(f"Warning: Failed to load config from {home_config}: {e}")
    
    # Check current directory
    local_config = Path('clip_colab_config.json')
    if local_config.exists():
        try:
            with open(local_config) as f:
                config.update(json.load(f))
        except Exception as e:
            print(f"Warning: Failed to load config from {local_config}: {e}")
    
    return config

# Load config at module import
config = load_config()

# Export variables
DEFAULT_CLIP_MODEL = config['CLIP_MODEL']
DEFAULT_CAPTION_MODEL = config['CAPTION_MODEL']
MODELS_CACHE_DIR = config['MODELS_CACHE_DIR']
OUTPUT_DIR = config['OUTPUT_DIR'] 