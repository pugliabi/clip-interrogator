from PIL import Image
from clip_setup import setup, image_to_prompt

def main():
    # Initialize CLIP and other models
    setup()
    
    # Load and process an image
    image_path = "path/to/your/image.jpg"  # Replace with actual path
    image = Image.open(image_path).convert('RGB')
    
    # Generate prompt
    prompt = image_to_prompt(image, mode='best')
    print(f"Generated prompt: {prompt}")

if __name__ == "__main__":
    main() 