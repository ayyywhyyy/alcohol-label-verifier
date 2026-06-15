import pytesseract
from PIL import Image


def extract_text_from_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text