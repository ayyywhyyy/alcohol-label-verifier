import easyocr
import numpy as np
from PIL import Image
import streamlit as st


@st.cache_resource
def load_reader():
    return easyocr.Reader(["en"], gpu=False)


def extract_text_from_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    image_array = np.array(image)

    reader = load_reader()
    results = reader.readtext(image_array, detail=0)

    extracted_text = "\n".join(results)
    return extracted_text
