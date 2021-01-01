from func_timeout import func_timeout, FunctionTimedOut
from PIL import Image
import configparser
import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="Path to the image")
ap.add_argument("-o", "--output", required=True, help="output to the image")
ap.add_argument("-e", "--error", required=True, help="output to the image")

args = vars(ap.parse_args())
ImagePath = args["input"]
Outputpath = args["output"]
Errorpath = args["error"]



# Start Config data...
config = configparser.ConfigParser()
config.sections()
config.read('example.ini')

# Get Timeout Second...
sec = int(config['DEFAULT']['sec'])

# Read File...
im = cv2.imread(ImagePath)

def Non_Morphing():
    logopath = config['DEFAULT']['logopath']

    o_size = os.path.getsize(ImagePath)

    if o_size > 2000000:
        img = Image.open(ImagePath)

        width, height = img.size
        img.resize((width // 2, height // 2))

        img.save(ImagePath)

    print('processing %s...' % ImagePath)

    # Reading Image...
    image = im

    # Currently India Is Region...

    cv2.imwrite(Outputpath, image)
    image = Image.open(Outputpath)
    logopath = logopath.replace("'", '')
    logopath = logopath.replace('"', '')
    logo = Image.open(logopath)

    wsize = int(min(image.size[0], image.size[1]) * 0.25)
    wpercent = (wsize / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    simage = logo.resize((wsize, hsize))
    mbox = image.getbbox()
    sbox = simage.getbbox()

    # right bottom corner
    box = (mbox[2] - sbox[2], mbox[3] - sbox[3])
    image.paste(simage, box)
    image.save(Outputpath)
    print("Ok")


try:
    func_timeout(sec, Non_Morphing, args=())
except FunctionTimedOut:
    print("Sorry! Time's Up, Please Run It Again.")
    try:
        # Save In Error File Because Its Timeout...
        cv2.imwrite(Errorpath, im)
        os.remove(Outputpath)
    except Exception as e:
        print(e)
        pass
