import os
import sys
import pytesseract
from PIL import Image
from notion_client import Client
from dotenv import load_dotenv

# load envs
load_dotenv()

# setup tesseract path
pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH")

# notion stuff
notion = Client(auth=os.getenv("NOTION_API_KEY"))
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")


# helpers
def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='pol')
        return text
    except Exception as e:
        print(f"Error during reading file: {image_path}: {e}")
        return ""


def add_text_to_notion(text, slide_number):
    try:
        notion.blocks.children.append(
            block_id=NOTION_PAGE_ID,
            children=[
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": text
                                }
                            }
                        ]
                    }
                }
            ]
        )
        print(f"Added note to slide: {slide_number}")
    except Exception as e:
        print(f"Error during adding note: {e}")


def scan_images_in_folder(folder_path):
    slide_number = 1
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            image_path = os.path.join(folder_path, filename)
            extracted_text = extract_text_from_image(image_path)
            if extracted_text:
                add_text_to_notion(extracted_text, slide_number)
                slide_number += 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: slides-to-notion.py <path to image dir>")
        sys.exit(1)

    folder_path = sys.argv[1]
    scan_images_in_folder(folder_path)
