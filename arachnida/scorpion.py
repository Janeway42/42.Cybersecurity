import argparse
import re
import os
from PIL import Image
from PIL.ExifTags import TAGS
from PIL import TiffImagePlugin

allowed_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
exif_tag = None
exif_val = None

class FriendlyArgParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"\nOops! Might wanna check the arguments before runing the program again!\n")
        exit(2)

def parse_image_metadata(image_name, exif_tag, new_exif_val):
    if not is_valid_image(image_name):
        print("File " + image_name + " is not a valid image format\n")
        return

    # extract and print metadata
    try:
        img = Image.open(image_name)

        # extract EXIF data (can not be extracted withowt third parties libraries in python)
        exif_data = img.getexif()

        if exif_tag is not None:
            # TAGS.items() returns a list of {key: value} EXIF tag IDs. Example: {1: 'ImageWidth', 2: 'Artist', ...}
            requested_tag = [key for key, val in TAGS.items() if val == exif_tag]
            if requested_tag:
                tag_id = requested_tag[0]
                exif_data[tag_id] = new_exif_val

                # save the updated EXIF data
                try:
                    img.save(image_name, exif=exif_data.tobytes())
                    print(f"\nTag '{exif_tag}' succesfully updated to: {exif_tag}\n")
                except Exception as e:
                    print(f"\nFailed to update tag '{exif_tag}': {e}\n!!! Only 'Artist' and 'ImageDescription' can be updated presently !!!")
            else:
                print(f"\nCould not modify EXIF tag: '{exif_tag}'\n")
        else: 
            print(f"\nFile: {os.path.basename(image_name)}\n")

            print("Basic data: ")
            print(f" - Format: {img.format}")
            print(f" - Size: {img.size}")
            print(f" - Width: {img.width}")
            print(f" - Height: {img.height}")
            print(f" - Mode: {img.mode}")
            print(f' - Frames in image: {getattr(img, "n_frames", 1)}')

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
        print(f"\nCould not access metadata for '{image_name}': {e}\n")


# if valid url it returns the link else it returns false
def is_valid_image(image):
    return image.lower().endswith(allowed_extensions)

# Start metadata parsing 
if __name__ == "__main__":
    parser = FriendlyArgParser(
            description="Script that prints image metadata"
        )

    parser.add_argument("items", nargs="+", help="images to read metadata from")
    parser.add_argument("-tag", required=False, help="The EXIF tag to be modified")
    parser.add_argument("-val", required=False, help="The new value for the EXIF tag")
    args = parser.parse_args()

    if args.tag:
        exif_tag = args.tag
    if args.val:
        exif_val = args.val

    try: 
        if len(args.items) > 1 and (args.tag or args.val): 
            print("\nModify the artist of an image one image at a time!\n")
        elif (args.val and not args.tag) or (args.tag and not args.val):
            print("\nPlease specify both the tag and the value you wish to modify!!!\n")
        else:
            for image in args.items:
                parse_image_metadata(image, exif_tag, exif_val)
    except Exception as e:
        print(f"\nCould not run scorpion: {e}\n")


# if PIllow not available run "pip3 install Pillow" before running the program 
# run example: python3 scorpion.py data/42_schools_worldwide-1024x623.png data/logo_partners_ADIDAS.jpg
# modify 'Artist' or 'ImageDescription' EXIF metadata run: python3 scorpion.py data/42_schools_worldwide-1024x623.png -tag Artist -val "New Name"