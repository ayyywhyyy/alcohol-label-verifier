from PIL import Image, ImageEnhance


def improve_image_for_ocr(image: Image.Image) -> Image.Image:
    image = image.convert("RGB")

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)

    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.3)

    return image
