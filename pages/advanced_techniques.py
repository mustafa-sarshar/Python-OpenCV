import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2 as cv
from utils.methods import scale_dim
import numpy as np

class FrameSplitColorChannelsImage(tk.Frame):
    CANVAS_SIZE = (200, 200)
    CANVAS_BK_COLOR = "#317001"
    FIELD_EDGE_NW = (10, 11)
    IMG_X, IMG_Y = 20, 20

    def __init__(self, parent, fname):
        tk.Frame.__init__(self, parent)
        self.fname = fname
        self.canvas_main = tk.Canvas(master=self, background=self.CANVAS_BK_COLOR, width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self.canvas_main.grid(row=0, column=0, sticky="WENS")
        self.frm_options = ttk.Frame(master=self)
        self.frm_options.grid(row=1, column=0, sticky="WE")

        self._init_transformers()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure([0, 1], weight=1)
        self.frm_options.grid_columnconfigure((0, 1, 2), weight=1)
        for widget in self.frm_options.winfo_children():
            widget.grid_configure(padx=5, ipadx=5)

    def _init_transformers(self):
        btn_task_1 = ttk.Button(master=self.frm_options, text="Blue Channel", command=lambda: self.task_changed(task="Blue Channel"))
        btn_task_1.grid(row=0, column=0, sticky="WE")
        btn_task_2 = ttk.Button(master=self.frm_options, text="Green Channel", command=lambda: self.task_changed(task="Green Channel"))
        btn_task_2.grid(row=0, column=1, sticky="WE")
        btn_task_3 = ttk.Button(master=self.frm_options, text="Red Channel", command=lambda: self.task_changed(task="Red Channel"))
        btn_task_3.grid(row=0, column=2, sticky="WE")

    def load_image(self):
        self.img_cv = cv.imread(str(self.fname), cv.IMREAD_UNCHANGED)
        self.img_cv = cv.resize(src=self.img_cv, dsize=scale_dim(self.img_cv, keep_aspect_ratio=True, fixed_height=160), interpolation=cv.INTER_AREA)
        self.img_cv = cv.cvtColor(self.img_cv, cv.COLOR_BGR2RGB)
        self.img_cv_current = self.img_cv.copy()
        self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv))
        img_w, img_h = self.img_holder.width(), self.img_holder.height()

        self.canvas_main.create_image((self.IMG_X+img_w//2, self.IMG_Y+img_h//2), image=self.img_holder, tag="image", anchor="center")
        self.canvas_main.create_rectangle(*self.FIELD_EDGE_NW, self.img_holder.width()+30, self.img_holder.height()+30)
        
        blank = np.zeros(shape=self.img_cv.shape[:2], dtype="uint8")
        b, g, r = cv.split(self.img_cv)
        self.img_blue_channel = cv.merge([b, blank, blank])
        self.img_green_channel = cv.merge([blank, g, blank])
        self.img_red_channel = cv.merge([blank, blank, r])

    def task_changed(self, task):
        img = self.canvas_main.find_withtag("image")

        if task == "Blue Channel":
            cv.imshow(winname="Blue Channel", mat=self.img_blue_channel)
        elif task == "Green Channel":
            cv.imshow(winname="Green Channel", mat=self.img_green_channel)
        elif task == "Red Channel":
            cv.imshow(winname="Red Channel", mat=self.img_red_channel)

