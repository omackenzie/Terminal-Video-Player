import cv2
import os
import ctypes

os.system("color")

while True:
    video_path = input("Enter the path of the video: ")

    if os.path.exists(video_path):
        video = cv2.VideoCapture(video_path)
        break
    else:
        print("Invalid path!")

while True:
    try:
        height = int(input("Enter the height you want the video to be inside the terminal (from 1-256): "))
        if height < 1:
            print("The height can't be smaller than 1!")
        elif height > 256:
            print("The max height is 256!")
        else:
            break
    except:
        print("The height needs to be an integer!")

###Changing font stuff (not written by me)
LF_FACESIZE = 32
STD_OUTPUT_HANDLE = -11

class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class CONSOLE_FONT_INFOEX(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("nFont", ctypes.c_ulong),
                ("dwFontSize", COORD),
                ("FontFamily", ctypes.c_uint),
                ("FontWeight", ctypes.c_uint),
                ("FaceName", ctypes.c_wchar * LF_FACESIZE)]

font = CONSOLE_FONT_INFOEX()
font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
font.nFont = 12
font.dwFontSize.X = int(256/height)
font.dwFontSize.Y = int(256/height)*2
font.FontFamily = 54
font.FontWeight = 400
font.FaceName = "Consolas"

handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
ctypes.windll.kernel32.SetCurrentConsoleFontEx(
        handle, ctypes.c_long(False), ctypes.pointer(font))

###

current_frame = 0

while True:
    ret,img = video.read()
    scale_percent = height/img.shape[0]
    width = int(img.shape[1] * scale_percent)*2
    dim = (width, height)

    if ret:
        os.system("cls")

        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
        
        ansi_values = []
    
        for y in range(height):
            for x in range(width):
                r,g,b = int(resized[y,x,2]/51), int(resized[y,x,1]/51), int(resized[y,x,0]/51)
                ansi_values.append(16+36*r+6*g+b)

        for y in range(height):
            for i in range(width*y, width*(y+1)):
                print(f"\x1b[38;5;{ansi_values[i]}m█", end="")
            print("")

        current_frame += 1
    else:
        break
        
input()
