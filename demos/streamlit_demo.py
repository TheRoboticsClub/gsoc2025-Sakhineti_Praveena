import streamlit as st
import os
from PIL import Image, ImageDraw, ImageFont
import json
import zipfile
import tempfile
import shutil
import base64
import io

def get_image_id(annotation_data, uploaded_filename):
    for img in annotation_data.get('images', []):
        if img['file_name'] == uploaded_filename:
            return img['id']
    return None

def get_boxes_and_categories_for_image(annotation_data, image_id):
    # Return list of (bbox, category_id) for the image
    return [(ann['bbox'], ann['category_id']) for ann in annotation_data.get('annotations', []) if ann['image_id'] == image_id]

def get_category_id_to_name(annotation_data):
    # Map category_id to category name
    return {cat['id']: cat['name'] for cat in annotation_data.get('categories', [])}

st.set_page_config(page_title="Object Detection Metrics", layout="wide")

st.title("Object Detection & Segmentation Metrics")

# Sidebar with three sections
st.sidebar.title("Detection Metrics")
section = st.sidebar.radio("Go to", ["Viewer", "Detector", "Evaluator"])

# Main content for Viewer
if section == "Viewer":
    st.header("Dataset Viewer")
    # Add dataset type selector and zip file uploader in the same row
    col1, col2 = st.columns([1, 2])
    with col1:
        dataset_type = st.selectbox("Dataset Type", ["COCO", "PascalVOC", "Custom"], key="dataset_type")
    with col2:
        zip_file = st.file_uploader("Upload Dataset Zip", type=["zip"], key="zip")
    if zip_file is not None:
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "dataset.zip")
            with open(zip_path, "wb") as f:
                f.write(zip_file.read())
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)

            # Recursively search for annotation file and image folder
            ann_path = None
            img_dir = None
            for root, dirs, files in os.walk(tmpdir):
                for file in files:
                    if file == "instances_val2017.json" and os.path.basename(root) == "annotations":
                        ann_path = os.path.join(root, file)
                for d in dirs:
                    if d == "val2017" and os.path.basename(root) == "images":
                        img_dir = os.path.join(root, d)
            if not ann_path:
                st.error("Could not find 'annotations/instances_val2017.json' in the zip file.")
            elif not img_dir:
                st.error("Could not find 'images/val2017' in the zip file.")
            else:
                # Load annotation data
                with open(ann_path, 'r') as f:
                    annotation_data = json.load(f)
                # List first 10 images
                image_files = sorted([f for f in os.listdir(img_dir) if f.lower().endswith((".jpg", ".png"))])[:10]
                if not image_files:
                    st.error("No images found in 'images/val2017'.")
                else:
                    cols = st.columns(len(image_files))
                    if 'selected_image' not in st.session_state:
                        st.session_state['selected_image'] = image_files[0]
                    for idx, (col, img_name) in enumerate(zip(cols, image_files)):
                        img_path = os.path.join(img_dir, img_name)
                        thumb = Image.open(img_path).convert("RGB").resize((100, 100))
                        border_color = '#FF0000' if st.session_state['selected_image'] == img_name else '#CCCCCC'
                        with col:
                            st.image(thumb, width=100)
                            if st.button(img_name, key=f"select_{img_name}"):
                                st.session_state['selected_image'] = img_name
                    # Check for query param selection
                    query_params = st.query_params
                    if 'selected' in query_params:
                        st.session_state['selected_image'] = query_params['selected'][0]
                        st.query_params.clear()  # Clear after use
                    selected_image = st.session_state['selected_image']
                    img_path = os.path.join(img_dir, selected_image)
                    img = Image.open(img_path).convert("RGB")
                    image_id = get_image_id(annotation_data, selected_image)
                    if image_id is not None:
                        boxes_and_cats = get_boxes_and_categories_for_image(annotation_data, image_id)
                        cat_id_to_name = get_category_id_to_name(annotation_data)
                        draw = ImageDraw.Draw(img)
                        try:
                            font = ImageFont.truetype("arial.ttf", 16)
                        except:
                            font = ImageFont.load_default()
                        for box, cat_id in boxes_and_cats:
                            x, y, w, h = box
                            draw.rectangle([x, y, x + w, y + h], outline="red", width=3)
                            label = cat_id_to_name.get(cat_id, str(cat_id))
                            text_pos = (x, y - 15 if y - 15 > 0 else y + 5)
                            draw.text(text_pos, label, fill="red", font=font)
                        st.image(img, caption="Image with Boxes and Labels", use_container_width=False, width=600)
                    else:
                        st.warning("Image not found in annotation file.")
    else:
        st.info("Upload a dataset zip file to begin.")

elif section == "Detector":
    st.header("Detector Section (Coming Soon)")
    st.write("This section will allow you to run detection models.")

elif section == "Evaluator":
    st.header("Evaluator Section (Coming Soon)")
    st.write("This section will allow you to evaluate detection results.")
