# Import All Dependency Libraries...
import glob
import json
import time
from func_timeout import func_timeout, FunctionTimedOut
import requests
from PIL import Image
import argparse
import cv2
import os
import configparser

# Argument Of Input, Output And Error...



# Read File...



# Save File Function...
def file_save(path, image, logopath):
    cv2.imwrite(path, image)
    image = Image.open(path)
    logopath = logopath.replace("'", '')
    logopath = logopath.replace('"', '')
    logo = Image.open(logopath)

    wsize = int(min(image.size[0], image.size[1]) * 0.25)
    wpercent = (wsize / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    simage = logo.resize((wsize, hsize))
    mbox = image.getbbox()
    sbox = simage.getbbox()

    box = (mbox[2] - sbox[2], mbox[3] - sbox[3])
    image.paste(simage, box)
    image.save(Outputpath)
    print("Ok")
for file in glob.glob("C:\\Users/DELL/Downloads/New folder/New_/*.jpg"):
    ImagePath = file
    import random

    im = cv2.imread(ImagePath)

    n = random.randint(0, 5000)
    Outputpath = r"C:\\Users/DELL/PycharmProjects/Exam/Output/"
    Errorpath = r"C:\\Users/DELL/PycharmProjects/Exam/error/"

    Outputpath = Outputpath + str(n) + ".jpg"
    Errorpath = Errorpath + str(n) + ".jpg"
# Start Config data...
    config = configparser.ConfigParser()
    config.sections()
    config.read('example.ini')

    # Get Timeout Second...
    sec = int(config['DEFAULT']['sec'])


    # Main File...
    def Morphing():
        # Read Config Data...
        logopath = config['DEFAULT']['logopath']
        apiurl = config['DEFAULT']['apiurl']
        apiurl = apiurl.replace("'", '')
        apiurl = apiurl.replace('"', '')
        apikey = config['DEFAULT']['apikey']
        apikey = apikey.replace("'", '')
        apikey = apikey.replace('"', '')

        # Api Calling...
        def vision_api(impath):
            regions = ['in']
            with open(impath, 'rb') as fp:
                response = requests.post(apiurl,
                                         data=dict(regions=regions),
                                         files=dict(upload=fp),
                                         headers={'Authorization': 'Token ' + apikey})
            api_json_data = response.json()
            return api_json_data

        # Json Format Of Api Calling...
        json_data = vision_api(ImagePath)

        # Get Size Of Current File...
        file_size = os.path.getsize(ImagePath)

        # Check If It Is Above 2MB Its Reduce To Half....
        if file_size > 2000000:
            img = Image.open(ImagePath)
            width, height = img.size
            img.resize((width // 2, height // 2))
            img.save(ImagePath)

        try:
            # This Function Is For Parameter Checking...
            def testing():
                try:
                    pairlist = json.loads(config['DEFAULT']['parameter'])
                    pairlist = [str(i) for i in pairlist]
                    for i in pairlist:
                        pair_name = i.lower()
                        for i in json_data['results']:
                            dict_data = i['candidates']
                            json1 = dict_data[0]
                            json2 = json1['plate']
                            if pair_name in json2:
                                return 10
                except Exception:
                    return 0

            # Checking If Get 10 Its Mean Some Parameters In Image....
            crossv = testing()
        except Exception:
            pass
        print('processing %s...' % ImagePath)

        # Reading Image...
        image = im

        # Currently India Is Region...
        try:
            list1 = []
            morph_cord= json_data

            if len(morph_cord['results']) != 0:
            # Appending Coordination In List...
                for i in morph_cord['results']:
                    dict_data = i['box']
                    for x in dict_data:
                        ed = dict_data[x]
                        list1.append(ed)

                # Topleft Is For Left up And Bottomleft is right bottom...
                def morph(topLeft, bottomRight):
                    x = topLeft[0]
                    y = topLeft[1]
                    w, h = bottomRight[0], bottomRight[1]

                    start_point = (x, y)
                    end_point = (w, h)
                    color = (255, 255, 255)
                    thickness = -1

                    image = im

                    # Blurring Image.
                    if crossv == 10:
                        pass

                    else:
                        image = cv2.rectangle(image, start_point, end_point, color, thickness)

                    file_save(Outputpath, image, logopath)
                try:
                    l2 = []
                    for i in range(len(list1)+1):

                        if len(l2) == 4:
                            topLeft = (l2[0], l2[1])
                            bottomRight = (l2[2], l2[3])
                            morph(topLeft, bottomRight)
                            l2.clear()


                        l2.append(list1[i])

                except Exception:
                    print()
            else:
                print(a)
        except Exception:
            try:
                # Crop Image In Below Coordination...
                img = Image.open(ImagePath)
                dummydata = img.copy()
                area = (0, 800, 1100, 930)
                cropped_img = dummydata.crop(area)
                cropped_img.save(Outputpath)
                time.sleep(1)

                # Recheck If Number Plate Exit Or Not...
                st = vision_api(Outputpath)
                time.sleep(1)
                os.remove(Outputpath)
                time.sleep(1)

                # Process Of Blur If Number Plate Exits...
                if len(st['results']) != 0:
                    x, y, w, h = 400, 750, 950, 880
                    start_point = (x, y)
                    end_point = (w, h)
                    color = (255, 255, 255)
                    thickness = -1
                    image = cv2.rectangle(image, start_point, end_point, color, thickness)

                    # Calling File Save Function...
                    file_save(Outputpath, image, logopath)

                else:
                    # Calling File Save Function...
                    file_save(Outputpath, image, logopath)

            except Exception:

                # If File Is Invalid Its Save In Error Folder...
                cv2.imwrite(Errorpath, image)
                print("Not Ok")
                pass


    try:

        # Calling Timeout Function...
        func_timeout(sec, Morphing, args=())
    except FunctionTimedOut:
        print("Sorry! Time's Up, Please Run It Again.")
        try:
            # Save In Error File Because Its Timeout...
            cv2.imwrite(Errorpath, im)
            os.remove(Outputpath)
        except Exception as e:
            print(e)
            pass
