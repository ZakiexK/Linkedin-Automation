import pytesseract
from PIL import Image
import time
import ollama
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")  # fallback if not set

# Safe open with retry for Windows file locking issue
def safe_open_image(path, retries=5, delay=1):
    for i in range(retries):
        try:
            return Image.open(path)
        except PermissionError:
            print(f"File {path} is locked, retrying...")
            time.sleep(delay)
    raise

# Extract text from an image
def extract_text_from_image(image_path: str) -> str:
    img = safe_open_image(image_path)
    return pytesseract.image_to_string(img)

# Generate post with Ollama AI
def generate_post_from_image(image_path: str) -> str:
    extracted_text = extract_text_from_image(image_path)

    prompt = f"""
You are a professional LinkedIn post writer. Create a concise LinkedIn post (120–200 words) 
based on the following extracted text. Make it professional yet personal. Avoid jargon dumps.

Extracted text:
{extracted_text}
    """

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    post_text = response["message"]["content"]

    # Ensure LinkedIn limit
    if len(post_text) > 2999:
        post_text = post_text[:2999]

    return post_text
