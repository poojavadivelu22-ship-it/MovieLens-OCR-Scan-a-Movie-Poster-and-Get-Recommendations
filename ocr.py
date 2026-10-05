import easyocr


# Load EasyOCR model
reader = easyocr.Reader(["en"])


def extract_text_from_image(image):
    result = reader.readtext(image)

    extracted_text = []

    for detection in result:
        text = detection[1]
        extracted_text.append(text)

    return " ".join(extracted_text)