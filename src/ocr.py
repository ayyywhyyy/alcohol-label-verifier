import pytesseract
from PIL import Image


def extract_text_from_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")

    try:
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text
    except pytesseract.pytesseract.TesseractNotFoundError:
        return (
            "OCR ERROR: Tesseract is not installed or not available in the deployment environment. "
            "Please make sure packages.txt contains tesseract-ocr and redeploy the app."
        )
    except Exception as e:
        return f"OCR ERROR: {str(e)}"