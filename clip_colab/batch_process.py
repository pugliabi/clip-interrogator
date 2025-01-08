#@title Batch process a folder of images 📁 -> 📝

#@markdown This will generate prompts for every image in a folder and either save results 
#@markdown to a desc.csv file in the same folder or rename the files to contain their prompts.
#@markdown The renamed files work well for [DreamBooth extension](https://github.com/d8ahazard/sd_dreambooth_extension)
#@markdown in the [Stable Diffusion Web UI](https://github.com/AUTOMATIC1111/stable-diffusion-webui).
#@markdown You can use the generated csv in the [Stable Diffusion Finetuning](https://colab.research.google.com/drive/1vrh_MUSaAMaC5tsLWDxkFILKJ790Z4Bl?usp=sharing)

import csv
import os
from IPython.display import clear_output, display
from PIL import Image
from tqdm import tqdm
from .clip_setup import setup, image_to_prompt

folder_path = "/content/my_images" #@param {type:"string"}
prompt_mode = 'best' #@param ["best","fast","classic","negative"]
output_mode = 'rename' #@param ["desc.csv","rename"]
max_filename_len = 128 #@param {type:"integer"}


def sanitize_for_filename(prompt: str, max_len: int) -> str:
    name = "".join(c for c in prompt if (c.isalnum() or c in ",._-! "))
    name = name.strip()[:(max_len-4)] # extra space for extension
    return name

ci.config.quiet = True

files = [f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png')] if os.path.exists(folder_path) else []
prompts = []
for idx, file in enumerate(tqdm(files, desc='Generating prompts')):
    if idx > 0 and idx % 100 == 0:
        clear_output(wait=True)

    image = Image.open(os.path.join(folder_path, file)).convert('RGB')
    prompt = image_to_prompt(image, prompt_mode)
    prompts.append(prompt)

    print(prompt)
    thumb = image.copy()
    thumb.thumbnail([256, 256])
    display(thumb)

    if output_mode == 'rename':
        name = sanitize_for_filename(prompt, max_filename_len)
        ext = os.path.splitext(file)[1]
        filename = name + ext
        idx = 1
        while os.path.exists(os.path.join(folder_path, filename)):
            print(f'File {filename} already exists, trying {idx+1}...')
            filename = f"{name}_{idx}{ext}"
            idx += 1
        os.rename(os.path.join(folder_path, file), os.path.join(folder_path, filename))

if len(prompts):
    if output_mode == 'desc.csv':
        csv_path = os.path.join(folder_path, 'desc.csv')
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            w.writerow(['image', 'prompt'])
            for file, prompt in zip(files, prompts):
                w.writerow([file, prompt])

        print(f"\n\n\n\nGenerated {len(prompts)} prompts and saved to {csv_path}, enjoy!")
    else:
        print(f"\n\n\n\nGenerated {len(prompts)} prompts and renamed your files, enjoy!")
else:
    print(f"Sorry, I couldn't find any images in {folder_path}")

def process_directory(input_dir, output_file="prompts.txt", mode='best'):
    """Process all images in a directory and save prompts to a file."""
    # Setup models
    setup()
    
    # Get all image files
    image_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    image_files = [
        f for f in os.listdir(input_dir) 
        if f.lower().endswith(image_extensions)
    ]
    
    results = {}
    
    # Process each image with progress bar
    for img_file in tqdm(image_files, desc="Processing images"):
        try:
            img_path = os.path.join(input_dir, img_file)
            image = Image.open(img_path).convert('RGB')
            prompt = image_to_prompt(image, mode=mode)
            results[img_file] = prompt
        except Exception as e:
            print(f"Error processing {img_file}: {str(e)}")
            results[img_file] = f"ERROR: {str(e)}"
    
    # Save results
    with open(output_file, 'w', encoding='utf-8') as f:
        for img_file, prompt in results.items():
            f.write(f"{img_file}\t{prompt}\n")
    
    return f"Processed {len(results)} images. Results saved to {output_file}"

def process_images(image_list, mode='best'):
    """Process a list of image paths and return prompts."""
    # Setup models
    setup()
    
    results = {}
    
    # Process each image with progress bar
    for img_path in tqdm(image_list, desc="Processing images"):
        try:
            image = Image.open(img_path).convert('RGB')
            prompt = image_to_prompt(image, mode=mode)
            results[img_path] = prompt
        except Exception as e:
            print(f"Error processing {img_path}: {str(e)}")
            results[img_path] = f"ERROR: {str(e)}"
    
    return results
