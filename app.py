#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path

import gradio as gr

title = """<h1 align="center">OtoLLM Image Selection</h1>"""
description = """<h3 align="center">This system is used to select otoscopy images in good quality for training OtoLLM.<h3>"""
instruction = """
<h4>How to use this demo?</h4>
1. Choose your name in the bottom <b><span style="color:Red;">"Name"</span></b> box, then click <b><span style="color:Red;">"Confirm Name"</span></b>.<br>
2. You will see an image appears on the left. You should click <b><span style="color:Red;">"Good"</span></b> or <b><span style="color:Red;">"Bad"</span></b> button to rate the quality of this image.<br>

This demo only includes a few images to illustrate the selection process. The complete dataset is not included in this demo.<br>
We have open sourced the code of this system on GitHub at <a href="https://github.com/otollm/image-selection">this link</a>.
"""
current_file_path = Path(__file__).resolve()
IMAGE_DIR = current_file_path.parent / "samples"
IMAGES = sorted(os.listdir(IMAGE_DIR))
USERS = ["Doctor-A", "Doctor-B", "Doctor-C"]


def get_next_img(img=None) -> tuple[str, str]:
    """Get the next image.

    Returns:
        tuple[str, str]: path to the next image and notes in HTML format
    """
    print(img)
    if not img:
        return os.path.join(IMAGE_DIR, IMAGES[0]), ""
    if img["orig_name"] == IMAGES[-1]:
        return img["path"], '<h4 align="center">🎉No more images</h4>'
    index = IMAGES.index(img["orig_name"])
    next_index = int(index) + 1
    return os.path.join(IMAGE_DIR, IMAGES[next_index]), ""


def flag_func(*args) -> tuple[str, str]:
    """Flag the rating.

    Returns:
        tuple[str, str]: path to the next image and notes in HTML format
    """
    print(args)
    args = list(args)
    if not args[1]:  # no image
        img = get_next_img()[0]
    elif isinstance(args[1], dict):
        img = args[1]["path"]
    else:
        img = args[1]

    if not args[0]:  # no username
        return img, '<h4 align="center"><b>❌Faild!</b><br>Please select the doctor <b><span style="color:Red;">"Name"</span></b> first</h4>'
    callback.flag(args)
    next_img, img_notes = get_next_img(args[1])
    if img_notes:
        return next_img, img_notes
    return next_img, '<h4 align="center"><span style="color:Green;"><b>✅Successful!<b></span></h4>'


# Build the GUI
with gr.Blocks(title="ImageSelection") as demo:
    gr.Markdown(title)
    gr.Markdown(description)
    with gr.Row(variant="compact"):
        img = gr.Image(height=500, width=500, label="Image", interactive=False, show_download_button=False, show_share_button=False)
        gr.Markdown(instruction)

    results = gr.HTML(value="", label="Results")

    with gr.Row(variant="compact"):
        bad_btn = gr.Button("Bad", variant="secondary")
        good_btn = gr.Button("Good", variant="primary")

    with gr.Row(variant="compact"):
        username = gr.Dropdown(choices=USERS, interactive=True, label="Name")
        name_btn = gr.Button("Confirm Name", variant="primary")

    need_flag = [username, img, good_btn, bad_btn]
    callback = gr.CSVLogger()
    callback.setup(need_flag, flagging_dir="flagged")

    name_btn.click(get_next_img, img, [img, results], preprocess=False)
    good_btn.click(flag_func, [username, img, good_btn], [img, results], preprocess=False)
    bad_btn.click(flag_func, [username, img, bad_btn], [img, results], preprocess=False)

# Launch the GUI
demo.queue()
demo.launch()
