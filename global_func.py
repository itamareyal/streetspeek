import os
from global_defs import *
import PySimpleGUI as sg
# import PySimpleGUIQt as sg
import os.path
import PIL.Image
import io
import base64
import cv2

# ---------------------------------------------------------
#   GOLBAL_FUNC - function library
# ---------------------------------------------------------


# Verify validity of selected input file
def verify_input_file(input_file):
    # file exists
    if not os.path.exists(input_file):
        print(f"File does not exist {input_file}")
        return False
    # file is img format
    elif not input_file.split('.')[-1].lower() in ALLOWED_IMG_FORMATS:
        print(f"File format isn't in the allowd img formats {ALLOWED_IMG_FORMATS}")
        return False
    return True


def get_img_file_list(folder):
    try:
        file_list = os.listdir(folder)         # get list of files in folder
    except:
        file_list = []
    fnames = [f for f in file_list if os.path.isfile(
        os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
    return fnames

def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()

def resize_image(img, scale_percent) :
    # Calculate new size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # Resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return resized

def get_dis_list(file):
    l = len(file)
    seed = int(len(file))
    dis = "Dis vectors:\n"
    for i in range(seed+1):
        dis += f"Element {i}: {round(float(i+1)*(abs(seed-i+0.1)),3)} M\n"
    return dis

def get_color_pallets(file):
    seed = int(len(file))
    dis = "Color pallets:\n"
    for i in range(seed+1):
        lets = ""
        for j in range(3):
            
            num = round(float(i+1)*(abs(seed-i+0.1)))
            name = file.split(".")[0]
            loc = num%(len(name)+j) -1
            if loc >= len(name):
                loc = max(len(name) - j,0)
            l1 = name[loc].upper()
            if not l1.isalpha():
                l1= "A"
            lets+=l1
        dis += f"Color {i}: {lets}{str(133+round(float(i+1)*(abs(seed-i+0.1))))[0:3]}\n"
    return dis