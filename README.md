# Image Text to Notion Script

## Installation

1. Install Tesseract OCR:
   - On macOS: `brew install tesseract`
   - On Windows: Download and install from [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the same directory as the script with the following content:
   ```
   NOTION_API_KEY=your_notion_api_key
   NOTION_PAGE_ID=your_notion_page_id
   TESSERACT_PATH=/path/to/tesseract
   ```

## Usage

### One-Time Folder Scan

To scan all images in a folder and upload the text to Notion:

```bash
python script.py --path="<path_to_folder>"
```

Replace `<path_to_folder>` with the path to the folder containing the images.

### Continuous Folder Monitoring

To continuously monitor a folder for new images and upload the text to Notion:

```bash
python script.py --path="<path_to_folder>" --watch
```

Replace `<path_to_folder>` with the path to the folder to be monitored.

## Environment Variables

- **NOTION_API_KEY**: Your Notion integration API key. You can create an integration and get an API key from [Notion's API documentation](https://developers.notion.com/docs/getting-started).
- **NOTION_PAGE_ID**: The ID of the Notion page or database where the notes should be added.
- **TESSERACT_PATH**: The path to the Tesseract OCR executable. This is required for text extraction from images.


