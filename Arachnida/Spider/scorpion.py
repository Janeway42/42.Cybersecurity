import argparse
import re
import os
from PIL import Image
from PIL.ExifTags import TAGS

allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

class FriendlyArgParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"\n😕 Oops! Forgot something?\n")
        exit(2)

def parse_image_metadata(image_name):
    if not is_valid_image(image_name):
        print("File " + image_name + " is not a valid image format\n")
        return

    # extract and print metadata
    try:
        img = Image.open(image_name)
        print(f"File: {os.path.basename(image_name)}\n")

        print("Basic data: ")
        print(f" - Format: {img.format}")
        print(f" - Size: {img.size}")
        print(f" - Width: {img.width}")
        print(f" - Height: {img.height}")
        print(f" - Mode: {img.mode}")
        print(f' - Frames in image: {getattr(img, "n_frames", 1)}')

        # extract EXIF data (can not be extracted withowt third parties libraries in python)
        exif_data = img.getexif()
        print("\nEXIF data:")
        for tag_id in exif_data:
            # get the tag name, instead of human unreadable tag id
            tag = TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)
            # decode bytes 
            if isinstance(data, bytes):
                data = data.decode()
            print(f" - {tag:25}: {data}")
        print("------------------------------------------\n")

    except Exception as e:
        print(f"Could not access metadata for '{image_name}': {e}\n")


# if valid url it returns the link else it returns false
def is_valid_image(image):
    return image.lower().endswith(allowed_extensions)

# Start metadata parsing 
if __name__ == "__main__":
    parser = FriendlyArgParser(
            description="Script that prints image metadata"
        )
    parser.add_argument("first_file")
    parser.add_argument("additional_files", nargs="*")
    args = parser.parse_args()

    images = [args.first_file] + args.additional_files
    
    if not images:
        print("No files received. No files analyzed.\n")
    else:
        for image in images:
            parse_image_metadata(image)


# if PIllow not available run "pip3 install Pillow" before running the program 
# run example: python3 scorpion.py data/42_schools_worldwide-1024x623.png data/logo_partners_ADIDAS.jpg