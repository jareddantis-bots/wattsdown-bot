from PIL import Image
from typing import Tuple
import pytesseract


def ocr_cropped(image_obj: Image, bounding_box: Tuple[int, int, int, int]) -> str:
    # Crop image to show affected areas
    cropped_image = image_obj.crop(bounding_box)
    # display(cropped_image)
    
    # Convert image to text
    text = pytesseract.image_to_string(cropped_image, config='--psm 6')
    return text.replace('\n', ' ')


def read_meralco_bulletin(image_obj: Image):
    # Get image dimensions
    width, _ = image_obj.size

    # Define crop for image regions
    box_affected_areas = (520, 390, width, 910)
    box_outage_date = (85, 220, 480, 350)
    box_outage_area = (490, 110, width, 325)
    box_outage_time = (85, 385, 480, 480)

    # Return recognized text from each area
    return  ((f'{ocr_cropped(image_obj, box_outage_date)}'),
            (f'{ocr_cropped(image_obj, box_outage_time)}'),
            (f'{ocr_cropped(image_obj, box_outage_area)}'),
            (f'{ocr_cropped(image_obj, box_affected_areas)}'))
