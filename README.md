---
title: Image Selection
emoji: 📝
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 4.41.0
pinned: true
license: mit
app_file: app.py
---

# Image Selection System

This repository holds the source code of the image selection system for the manuscript of **_A Deep Learning Approach Harnessing Large Language Models for Otoscopic Image Understanding_**.

## Dependencies

- python == 3.11
- gradio == 4.41.0

## How to Deploy

1. Create a virtual environment and install the dependencies:

    ```bash
    conda create -n image_selection python=3.11
    conda activate image_selection
    pip install -r requirements.txt
    ```

2. Run the application:

    ```bash
    conda activate image_selection
    python app.py
    ```

3. Open the browser and go to the address: [http://127.0.0.1:7860](http://127.0.0.1:7860)

This demo only includes a few images to illustrate the selection process. The complete dataset is not included in this demo.
