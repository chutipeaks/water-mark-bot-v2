import os
import io
import img2pdf
import fitz  # PyMuPDF
from PIL import Image
from PyPDF2 import PdfReader
from collections import OrderedDict
import logging
import traceback
import asyncio
from PIL import Image, UnidentifiedImageError

# Define target image sizes to remove (width, height)
TARGET_SIZES = [
    (1241, 89),  # First size to remove
    (476, 82)  # Second size to remove
]


async def process_page(pdf: PdfReader, page_index: int, image_path: str):
    """Process a single PDF page to filter out target-sized images."""
    try:
        # Check if page has XObject resources
        if '/Resources' not in pdf.pages[page_index] or '/XObject' not in pdf.pages[page_index]['/Resources']:
            logging.warning(f"No XObject resources found on page {page_index}")
            return None

        content = pdf.pages[page_index]['/Resources']['/XObject'].get_object()
        filtered_images = {}
        index = 0

        for obj in content:
            if content[obj]['/Subtype'] == '/Image':
                try:
                    size = (content[obj]['/Width'], content[obj]['/Height'])

                    # Skip images that match our target sizes (remove these)
                    if size in TARGET_SIZES:
                        logging.info(f"Removing target size image: {size}")
                        continue

                    # Keep all other images
                    filtered_images[index] = {
                        'object': obj,
                        'size': size,
                        'data': content[obj]._data
                    }
                    index += 1

                except Exception as e:
                    logging.warning(f"Failed to process image {obj}: {str(e)}")
                    continue

        return filtered_images

    except Exception as e:
        logging.error(f"Error processing page {page_index}: {str(e)}")
        return None


async def remove_uknown_image_annotations_main(input_file_path: str, output_directory: str):
    """Disabled version - just returns the original file"""
    logging.info("Image annotation removal is disabled")
    return input_file_path