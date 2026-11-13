import pymupdf


def extract_text_from_pdf(file_path):
    try:
        with pymupdf.open(file_path) as document:
            text = "".join(page.get_text() for page in document)
    except (pymupdf.FileDataError, RuntimeError) as error:
        raise ValueError("The uploaded file is not a readable PDF.") from error

    if not text.strip():
        raise ValueError(
            "No selectable text was found in this PDF. "
            "Please upload a text-based resume PDF."
        )

    return text