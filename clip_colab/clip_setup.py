#@title Setup
import torch
from PIL import Image
import open_clip
from transformers import BlipProcessor, BlipForConditionalGeneration
from config import DEFAULT_CLIP_MODEL, DEFAULT_CAPTION_MODEL

class ClipSetup:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.clip_model = None
        self.clip_preprocess = None
        self.caption_model = None
        self.caption_processor = None

    def setup_clip(self, model_name=DEFAULT_CLIP_MODEL):
        self.clip_model, _, self.clip_preprocess = open_clip.create_model_and_transforms(model_name)
        self.clip_model = self.clip_model.to(self.device)
        self.clip_model.eval()

    def setup_caption(self, model_name=DEFAULT_CAPTION_MODEL):
        self.caption_processor = BlipProcessor.from_pretrained(f"Salesforce/{model_name}")
        self.caption_model = BlipForConditionalGeneration.from_pretrained(
            f"Salesforce/{model_name}"
        ).to(self.device)

_instance = None

def setup(clip_model=DEFAULT_CLIP_MODEL, caption_model=DEFAULT_CAPTION_MODEL):
    global _instance
    if _instance is None:
        _instance = ClipSetup()
        _instance.setup_clip(clip_model)
        _instance.setup_caption(caption_model)
    return _instance

def image_to_prompt(image, mode='best', num_candidates=5):
    if _instance is None:
        setup()
    
    # Generate caption
    inputs = _instance.caption_processor(image, return_tensors="pt").to(_instance.device)
    caption = _instance.caption_model.generate(**inputs)
    caption = _instance.caption_processor.decode(caption[0], skip_special_tokens=True)
    
    # Get CLIP features
    image = _instance.clip_preprocess(image).unsqueeze(0).to(_instance.device)
    with torch.no_grad():
        image_features = _instance.clip_model.encode_image(image)
        image_features /= image_features.norm(dim=-1, keepdim=True)
    
    if mode == 'caption':
        return caption
    elif mode == 'best':
        return f"{caption}, {get_clip_features_text(image_features)}"
    else:
        raise ValueError("Mode must be 'caption' or 'best'")

def get_clip_features_text(image_features, top_count=5):
    # This is a simplified version - you might want to add more sophisticated
    # feature extraction based on the CLIP model's vocabulary
    return "high quality, detailed, sharp focus, professional"  # Placeholder
        