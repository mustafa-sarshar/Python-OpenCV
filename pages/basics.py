from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2 as cv
import threading
from utils.methods import scale_dim

class FrameReadImage(tk.Frame):
    CANVAS_SIZE = (200, 200)
    CANVAS_BK_COLOR = "#317001"
    FIELD_EDGE = (10, 11, CANVAS_SIZE[0]-9, CANVAS_SIZE[1]-5)
    IMG_X, IMG_Y = 20, 20

    def __init__(self, parent, fname):
        tk.Frame.__init__(self, parent)
        self.fname = fname
        self.canvas_main = tk.Canvas(master=self, background=self.CANVAS_BK_COLOR, width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self.canvas_main.grid(row=0, column=0, sticky="WENS")

    def load_image(self):
        _img_cv = cv.imread(str(self.fname), cv.IMREAD_UNCHANGED)
        _img_cv = cv.resize(src=_img_cv, dsize=scale_dim(_img_cv, keep_aspect_ratio=True, fixed_height=160), interpolation=cv.INTER_AREA)
        self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(cv.cvtColor(_img_cv, cv.COLOR_BGR2RGB)))
        self.canvas_main.create_image((self.IMG_X, self.IMG_Y), image=self.imgae_holder, tag="imgae", anchor="nw")
        self.canvas_main.create_rectangle(*self.FIELD_EDGE)

class FrameReadVideo(tk.Frame):
    CANVAS_SIZE = (200, 200)
    CANVAS_BK_COLOR = "#317001"
    FIELD_EDGE = (10, 11, CANVAS_SIZE[0]-9, CANVAS_SIZE[1]-5)
    VIDEO_X, VIDEO_Y = 20, 20

    def __init__(self, parent, fname):
        tk.Frame.__init__(self, parent)
        self.fname = fname
        self.canvas_main = tk.Canvas(master=self, background=self.CANVAS_BK_COLOR, width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self.canvas_main.grid(row=0, column=0, sticky="WENS")
    
    def load_video(self):
        self.cap = cv.VideoCapture(str(self.fname))
        self.video_thread = threading.Thread(target=self.show_video, daemon=True)
        self.video_thread.start()

    def show_video(self):
        if self.cap:
            success = True
            self.canvas_main.create_rectangle(*self.FIELD_EDGE)
            while success:
                success, _video = self.cap.read()
                if success:                    
                    _video = cv.resize(src=_video, dsize=scale_dim(_video, keep_aspect_ratio=True, fixed_width=160), interpolation=cv.INTER_AREA)
                    self.video_holder = ImageTk.PhotoImage(Image.fromarray(cv.cvtColor(_video, cv.COLOR_BGR2RGB)))
                    self.canvas_main.create_image((self.VIDEO_X, self.VIDEO_Y), image=self.video_holder, tag="video", anchor="nw")
                    cv.waitKey(30)
        self.load_video() # Repeat showing the video

class FrameLoadImage(tk.Frame):
    CANVAS_SIZE = (200, 200)
    CANVAS_BK_COLOR = "#317001"
    FIELD_EDGE = (10, 11, CANVAS_SIZE[0]-9, CANVAS_SIZE[1]-5)
    IMG_X, IMG_Y = 20, 20

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.canvas_main = tk.Canvas(master=self, background=self.CANVAS_BK_COLOR, width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self.canvas_main.grid(row=0, column=0, sticky="WENS")
        self.btn_open = ttk.Button(master=self, text="Open", command=self.load_image)
        self.btn_open.grid(row=1, column=0, sticky="WE")
    
    def load_image(self):
        fname = filedialog.askopenfilename(
            defaultextension="*.jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")],
            initialdir=Path(Path.cwd(), "files")
        )
        if fname:
            self.show_image(fname=str(fname))
    
    def show_image(self, fname):
        _img_cv = cv.imread(str(fname), cv.IMREAD_UNCHANGED)
        _img_cv = cv.resize(src=_img_cv, dsize=scale_dim(_img_cv, keep_aspect_ratio=True, fixed_width=160), interpolation=cv.INTER_AREA)
        self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(cv.cvtColor(_img_cv, cv.COLOR_BGR2RGB)))
        self.canvas_main.create_image((self.IMG_X, self.IMG_Y), image=self.imgae_holder, tag="imgae", anchor="nw")
        self.canvas_main.create_rectangle(*self.FIELD_EDGE)