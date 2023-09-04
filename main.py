
from global_defs import *
from global_func import *

import pytesseract
import PIL.Image


# ---------------------------------------------------------
#   StreetsPeek - execution script
# ---------------------------------------------------------

# Program version
version = 1.0
sg.theme_add_new('sp_theme', SP_THEME)
sg.theme('sp_theme')

current_image = IMG_DEFAULT
current_folder = os.getcwd()
initial_filelist = get_img_file_list(current_folder)

# --------------------------------- Define Layout ---------------------------------

left_col = [[sg.Image(key='-LOGO-', data=convert_to_bytes(LOGO_FILE, resize=(300,300)))],
            [sg.Text('Folder'), sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse(initial_folder=current_folder)],
            [sg.Listbox(values=initial_filelist, enable_events=True, size=(40,20),key='-FILE LIST-')],
            [sg.Text('Resize to',visible=False), sg.In(key='-W-', size=(5,1),visible=False), sg.In(key='-H-', size=(5,1),visible=False)]]

images_col = [
              [sg.Text(size=(40,1), key='-TOUT-')],
              [sg.Image(key='-IMAGE-')]]

# ----- Full layout -----
layout = [[sg.Column(left_col, element_justification='c'), sg.VSeperator(),sg.Column(images_col, element_justification='c')],
            # buttons
            [sg.Button('Analyze', key='-ANALYZE-', font=FONT_PARAM), sg.Button('Exit', key='-EXIT-', font=FONT_PARAM)],
            # console
            [sg.Output(size=(CONSOLE_WIDTH,10), key='-OUTPUT-', font=FONT_LOG)],
            ]

# Window header
window = sg.Window(f'streetspeek version {version}', layout, element_justification='l')

compute_flag= False
compute_ready = False
compute_cnt = 0

# Pytesseract
tes_config = r"--psm 11 --oem 3"

# ----- Run the Event Loop -----
# --------------------------------- Event Loop ---------------------------------
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == '-EXIT-':
        break
    if event == '-FOLDER-':                         # Folder name was filled in, make a list of files in the folder
        folder = values['-FOLDER-']
        try:
            file_list = os.listdir(folder)         # get list of files in folder
        except:
            file_list = []
        fnames = [f for f in file_list if os.path.isfile(
            os.path.join(folder, f)) and f.lower().endswith((".png", ".jpg", "jpeg", ".tiff", ".bmp"))]
        window['-FILE LIST-'].update(fnames)
    elif event == '-FILE LIST-':    # A file was chosen from the listbox
        try:
            filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
            window['-TOUT-'].update(filename)
            if values['-W-'] and values['-H-']:
                new_size = int(values['-W-']), int(values['-H-'])
            else:
                new_size = None
            window['-IMAGE-'].update(data=convert_to_bytes(filename, resize=IN_IMG_SIZE))
            print(f'image loaded {filename}')
        except Exception as E:
            print(f'** Error {E} **')
            pass        # something weird happened making the full filename

    elif event == '-ANALYZE-':
        img = cv2.imread(filename)
        height, width, _ = img.shape
        boxes = pytesseract.image_to_boxes(img, config=tes_config)
        for box in boxes.splitlines():
            box = box.split(" ")
            img = cv2.rectangle(img, (int(box[1]), height- int(box[2])), (int(box[3]), height- int(box[4])), (0,255,0), 2 )
        cv2.imwrite(filename=f"{filename}_boxed.jpeg", img=img)
        img_boxed = f"{filename}_boxed.jpeg"
        tes_text = pytesseract.image_to_string(PIL.Image.open(filename), config=tes_config)
        
        # print detected text
        print(tes_text)
        print(BUFFER)

        print(get_dis_list(filename))
        print(get_color_pallets(filename))
        
        # Show Image with boxws
        window['-IMAGE-'].update(data=convert_to_bytes(img_boxed, resize=IN_IMG_SIZE))

# --------------------------------- Close & Exit ---------------------------------
window.close()
