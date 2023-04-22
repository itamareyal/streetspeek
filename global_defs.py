from datetime import date, datetime
import PySimpleGUI as sg
import os
import time
# ---------------------------------------------------------
#   GLOBAL_DEFS - global scope variables
# ---------------------------------------------------------

GUI_HEADER = 'streetspeek'

# err codes
ERR_ROW_NOT_APPENDED = -1
ERR_FILE_NOT_EXIST = 1
ERR_FILE_SHEET_MISSING = 2

MORE_AREGS =8
DELTA_X = 1
DEF_DELTA_X = DELTA_X **2
MAX_REGS = 256

ELSE = "אחר"

# gui fonts
FONT_HEADER = 'Any 24'
FONT_PARAM = 'Any 18'
FONT_LOG = 'Any 14'
# gui element width
IMG_SIZE = (500,500)
IMG_DEFAULT = sg.EMOJI_BASE64_HAPPY_THUMBS_UP
PARAM_WIDTH = 60
CONSOLE_WIDTH = 100

MAX_COMPUTE_CNT = 1000

BUFFER = '----------------------------------------'

DET_IMG = os.path.join('db', 'det.jpeg')
DET_WEB = 'https://www.cafezorik.co.il/'
DET_FACEBOOK = 'https://www.facebook.com/cafezorik/'

LOGO_FILE = os.path.join('db','SP_logo_grey.png')

IN_IMG_SIZE = (500,500)
ALLOWED_IMG_FORMATS = ['png','jpeg']

SP_THEME = {'BACKGROUND': '#E7DFD8',
                'TEXT': '#000000',
                'INPUT': '#A3A3A3',
                'TEXT_INPUT': 'white',
                'SCROLL': '#A3A3A3',
                'BUTTON': ('white', '#A3A3A3'),
                'PROGRESS': ('#01826B', '#6BE5F5'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

# prop class definition
class Prop:
    def __init__(self, name, system, subsystem, description) -> None:
        self.name = name
        self.system = system
        self.subsystem = subsystem
        self.description = description
