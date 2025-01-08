from setuptools import setup, find_packages

setup(
    name="clip_colab",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Pillow>=9.0.0",
        "tqdm>=4.65.0",
        "gradio>=3.35.2",
        "open_clip_torch>=2.20.0",
        "clip-interrogator>=0.5.4",
        "IPython>=8.0.0"
    ],
    include_package_data=True,
) 