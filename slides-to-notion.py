import os
import time

import pillow_heif
import pytesseract
import argparse
from PIL import Image
from notion_client import Client
from dotenv import load_dotenv
from pillow_heif import register_heif_opener

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
        if image_path.lower().endswith('.heic'):
            heif_file = pillow_heif.read_heif(image_path)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
            )
        else:
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
                },
                {
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                }
            ]
        )
        print(f"Added note to slide: {slide_number}")
    except Exception as e:
        print(f"Error during adding note: {e}")


def scan_images_in_folder(folder_path, slide_number=1):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.heic')):
            image_path = os.path.join(folder_path, filename)
            extracted_text = extract_text_from_image(image_path)
            if extracted_text:
                add_text_to_notion(extracted_text, slide_number)
                slide_number += 1
    return slide_number


def watch_folder(folder_path):
    processed_files = set(os.listdir(folder_path))
    slide_number = 1
    while True:
        current_files = set(os.listdir(folder_path))
        new_files = current_files - processed_files
        if new_files:
            for filename in new_files:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif', '.heic')):
                    image_path = os.path.join(folder_path, filename)
                    extracted_text = extract_text_from_image(image_path)
                    if extracted_text:
                        add_text_to_notion(extracted_text, slide_number)
                        slide_number += 1
            processed_files = current_files
        time.sleep(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan slides and add text to notion")
    parser.add_argument("--path", required=True, help="Path to directory to watch")
    parser.add_argument("--watch", action="store_true", help="Watch for changes in directory")

    args = parser.parse_args()
    folder_path = args.path

    register_heif_opener()

    if args.watch:
        watch_folder(folder_path)
    else:
        scan_images_in_folder(folder_path)
