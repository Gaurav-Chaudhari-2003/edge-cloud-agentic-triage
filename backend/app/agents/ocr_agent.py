import os
from app.agents.base import AgentState

try:
    from PIL import Image
    import pytesseract
except ImportError:
    # This allows the app to run if OCR dependencies are not installed,
    # but it will fail gracefully if an image is actually processed.
    print("WARNING: Pillow or pytesseract not installed. OCR functionality will be unavailable.")
    Image = None
    pytesseract = None

class OCRAgent:
    """
    Extracts text from an image using Tesseract OCR. This agent only runs
    if the input_type is 'image'. The extracted text then replaces the
    image path in state.content for downstream processing.
    """

    def run(self, state: AgentState) -> AgentState:
        # This agent only runs for image inputs.
        if state.input_type != "image":
            return state

        state.current_agent = "ocr"
        state.execution_path.append("ocr")

        if not Image or not pytesseract:
            state.validation_errors.append("OCR dependencies (Pillow, Tesseract) are not installed on the server.")
            return state

        image_path = state.content
        if not os.path.exists(image_path):
            state.validation_errors.append(f"OCRAgent: Image path does not exist: {image_path}")
            return state

        try:
            # Use pytesseract to do OCR on the image
            extracted_text = pytesseract.image_to_string(Image.open(image_path))
            
            if not extracted_text or not extracted_text.strip():
                state.validation_errors.append("OCR failed to extract any text from the image.")
            else:
                # The extracted text now becomes the main content for the rest of the pipeline
                state.content = extracted_text
                print(f"--- OCR Agent: Extracted Text ---")
                print(extracted_text)
                print(f"---------------------------------")

        except Exception as e:
            error_message = f"OCR processing failed with an unexpected error: {e}"
            state.validation_errors.append(error_message)
            print(f"ERROR: {error_message}")

        return state
