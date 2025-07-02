import streamlit as st
import os
from PIL import Image, ImageDraw, ImageFont
import json

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
    # Dataset selector, image uploader, and annotation uploader in a single row
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        dataset_name = st.selectbox("Select Dataset", ["COCO", "Pascal VOC", "Custom"], key="dataset")
    with col2:
        image_file = st.file_uploader("Sample Image", type=["jpg", "png"], key="img")
    with col3:
        annotation_file = st.file_uploader("Annotation (JSON)", type=["json"], key="ann")

    show_button = image_file is not None
    if show_button:
        if st.button("View Sample"):
            img = Image.open(image_file).convert("RGB")
            if annotation_file is not None:
                annotation_data = json.load(annotation_file)
                image_id = get_image_id(annotation_data, image_file.name)
                if image_id is not None:
                    boxes_and_cats = get_boxes_and_categories_for_image(annotation_data, image_id)
                    cat_id_to_name = get_category_id_to_name(annotation_data)
                    draw = ImageDraw.Draw(img)
                    # Try to use a default font
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
                    st.image(img, caption="Sample Image with Boxes and Labels", use_container_width=False, width=600)
                else:
                    st.warning("Image not found in annotation file.")
            else:
                st.image(img, caption="Sample Image", use_container_width=False, width=600)
    elif image_file is None:
        st.info("Upload a sample image to begin.")

elif section == "Detector":
    st.header("Detector Section (Coming Soon)")
    st.write("This section will allow you to run detection models.")

elif section == "Evaluator":
    st.header("Evaluator Section (Coming Soon)")
    st.write("This section will allow you to evaluate detection results.")
