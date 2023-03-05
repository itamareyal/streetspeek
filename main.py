
from global_defs import *
from global_func import *

# ---------------------------------------------------------
#   CAFEINFO - execution script
# ---------------------------------------------------------

# Program version
version = 1.0
sg.theme_add_new('sp_theme', SP_THEME)
sg.theme('sp_theme')

current_image = IMG_DEFAULT
current_folder = os.getcwd()
initial_filelist = get_img_file_list(current_folder)

# GUI layout
# layout = [  # header
#             [sg.Push(), sg.Text('', font=FONT_HEADER), sg.Push()],

#             # image
#             [sg.Push(), sg.Image(current_image, s=IMG_SIZE, key='-IMG-'), sg.Push(),],

#             # buttons
#             [sg.Input(key='-FILE-', visible=False, enable_events=True), sg.FileBrowse(button_text= 'Load image', font=FONT_PARAM),
#             sg.Button('Analyze', key='-ANALYZE-', font=FONT_PARAM),
#             sg.Button('Exit', key='-EXIT-', font=FONT_PARAM)],

#             # console
#             [sg.Output(size=(CONSOLE_WIDTH,5), key='-OUTPUT-', font=FONT_LOG)],
#             ]


# --------------------------------- Define Layout ---------------------------------

# First the window layout...2 columns

left_col = [[sg.Image(key='-LOGO-', data=convert_to_bytes(LOGO_FILE, resize=(300,300)))],
            [sg.Text('Folder'), sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse(initial_folder=current_folder)],
            [sg.Listbox(values=initial_filelist, enable_events=True, size=(40,20),key='-FILE LIST-')],
            [sg.Text('Resize to',visible=False), sg.In(key='-W-', size=(5,1),visible=False), sg.In(key='-H-', size=(5,1),visible=False)]]

# For now will only show the name of the file that was chosen
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
        # print('analyzing image...')
        time.sleep(3)
        compute_flag = True
        print('image analyzed')
        window['-IMAGE-'].update(data=convert_to_bytes(DET_IMG, resize=IN_IMG_SIZE))
        print('Results for זוריק')
        print(f'WEBSITE: {DET_WEB}')
        print(f'FACEBOOK: {DET_FACEBOOK}')
        print(f'-------------------------------')
        print('Results for זורך')
        print('No results found for זורך')

# --------------------------------- Close & Exit ---------------------------------
window.close()

# # Main event loop
# while True:
#     event, values = window.read()
#     # window closing
#     if event == sg.WIN_CLOSED or event == '-EXIT-':
#         break

#     # excel file selected
#     if event == '-FILE-':
#         if verify_input_file(values['-FILE-']):
#             current_image = values['-FILE-']
#             window['-IMG-'].update(source=current_image)
#             print(f"new image loaded")


# window.close()