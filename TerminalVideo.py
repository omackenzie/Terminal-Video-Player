import cv2
import os
import curses
import time

while True:
    video_path = input("Enter the path of the video: ")

    if os.path.exists(video_path):
        video = cv2.VideoCapture(video_path)
        break
    else:
        print("Invalid path!")

while True:
    try:
        height = int(input("Enter the height you want the video to be inside the terminal (from 31-256): "))
        if height < 31:
            print("The height can't be smaller than 31!")
        elif height > 256:
            print("The max height is 256!")
        else:
            break
    except:
        print("The height needs to be an integer!")

while True:
    amount_of_frames = input("Enter the amount of frames you want to play (type ALL if you want to play the entire video): ")
    if amount_of_frames.isdigit():
        amount_of_frames = int(amount_of_frames)
        break
    elif amount_of_frames.lower() == "all":
        amount_of_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        break
    else:
        print("The amount of frames needs to be an integer!")

if amount_of_frames > int(video.get(cv2.CAP_PROP_FRAME_COUNT)):
    amount_of_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

if os.name == "nt":
    import ctypes
    import ctypes.wintypes
    
    #Change font size
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
    font.dwFontSize.X = int(256/height)*2
    font.dwFontSize.Y = int(256/height)*2
    font.FontFamily = 54
    font.FontWeight = 400
    font.FaceName = "Consolas"

    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(
            handle, ctypes.c_long(False), ctypes.pointer(font))

    #Change window size so that the characters can fit
    os.system(f"mode con cols={height*4} lines={height*2}")

def main(stdscr):
    curses.initscr()
    curses.curs_set(0)  
    max_y, max_x = stdscr.getmaxyx()
    pad = curses.newpad(height*2, height*4)

    curses.use_default_colors()
    for i in range(1, 255):
        curses.init_pair(i, i, -1);

    ret,img = video.read()
    scale_percent = height/img.shape[0]
    width = int(img.shape[1] * scale_percent)*2
    dim = (width, height)
        
    def render_frames():
        current_frame = 0
        frames = []

        while current_frame != amount_of_frames:
            ret,img = video.read()
            if ret:
                pad.addstr(0,0,f"Calculated {current_frame} frames")
                pad.refresh(0,0, 0,0, max_y-1,max_x-1)
                resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

                frames.append([])
                for y in range(height):
                    for x in range(width):
                        r,g,b = int(resized[y,x,2]/51), int(resized[y,x,1]/51), int(resized[y,x,0]/51)
                        frames[current_frame].append(16+36*r+6*g+b)
                current_frame += 1
            else:
                break

        return frames
    def play():
        for current_frame in range(amount_of_frames):
            start = time.time()
            draw_screen(pad, width, frames[current_frame])
            pad.refresh(0,0, 0,0, max_y-1,max_x-1)
            time.sleep(max(1/video.get(cv2.CAP_PROP_FPS) - (time.time() - start), 0))

    frames = render_frames()
    current_frame = 0
    play()

def draw_screen(pad, width, frame):
    for y in range(height):
        pad.move(y,0)
        for i in range(width*y, width*(y+1)):
            pad.addstr("█", curses.color_pair(frame[i]))

curses.wrapper(main)
