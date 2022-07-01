from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2 as cv
from cv2 import threshold
from utils.methods import scale_dim
import matplotlib.pyplot as plt

class FrameHistogramImage(tk.Frame):
    CANVAS_SIZE = (200, 200)
    CANVAS_BK_COLOR = "#317001"
    FIELD_EDGE = (10, 11, CANVAS_SIZE[0]-9, CANVAS_SIZE[1]-5)
    IMG_X, IMG_Y = 20, 20

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.canvas_main = tk.Canvas(master=self, background=self.CANVAS_BK_COLOR, width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self.canvas_main.grid(row=0, column=0, sticky="WENS")
        self.btn_open = ttk.Button(master=self, text="Open an image", command=self.load_image)
        self.btn_open.grid(row=1, column=0, sticky="WE")
        self.btn_histogram = ttk.Button(master=self, text="Histogram of Color Channels", command=self.cal_hist)
        self.btn_histogram.grid(row=2, column=0, sticky="WE")
        
        self.grid_columnconfigure(0, weight=1)        
        self.grid_rowconfigure(0, weight=1)
        self.canvas_main.create_rectangle(*self.FIELD_EDGE, tag="border")

    def load_image(self):
        fname = filedialog.askopenfilename(
            defaultextension="*.jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")],
            initialdir=Path(Path.cwd(), "files")
        )
        if fname:
            self.show_image(fname=str(fname))

    def show_image(self, fname):
        self.img_cv = cv.imread(str(fname), cv.IMREAD_UNCHANGED)
        self.img_cv = cv.resize(src=self.img_cv, dsize=scale_dim(self.img_cv, keep_aspect_ratio=True, fixed_width=160), interpolation=cv.INTER_AREA)
        self.img_holder = ImageTk.PhotoImage(Image.fromarray(cv.cvtColor(self.img_cv, cv.COLOR_BGR2RGB)))
        self.canvas_main.create_image((self.IMG_X, self.IMG_Y), image=self.img_holder, tag="imgae", anchor="nw")
        self.canvas_main.delete(self.canvas_main.find_withtag("border"))
        self.canvas_main.create_rectangle(*self.FIELD_EDGE)

    def cal_hist(self):
        plt.figure()        
        colors = ("b", "g", "r")
        for i, col in enumerate(colors):
            hist = cv.calcHist(images=[self.img_cv], channels=[i], mask=None, histSize=[256], ranges=[0, 256])
            plt.plot(hist, color=col)
            # plt.xlim([0, 256])
        plt.title("Histogram of Color Channels")
        plt.xlabel("Bins")
        plt.ylabel("No. of pixels")
        plt.legend(colors)
        plt.show()

class FrameThresholdingImage(tk.Frame):
    CANVAS_SIZE = (250, 200)
    CANVAS_BK_COLOR = "#317001"
    FIELD_EDGE = (10, 11, CANVAS_SIZE[0], CANVAS_SIZE[1]-5)
    IMG_X, IMG_Y = 15, 20

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.canvas_main = tk.Canvas(master=self, background=self.CANVAS_BK_COLOR, width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self.canvas_main.grid(row=0, column=0, sticky="WENS")
        self.btn_open = ttk.Button(master=self, text="Open an image", command=self.load_image)
        self.btn_open.grid(row=1, column=0, sticky="WE")
        self.btn_thresh = ttk.Button(master=self, text="Thresholding", command=lambda: self.apply_thresholding())
        self.btn_thresh.grid(row=2, column=0, sticky="WE")
        self.btn_thresh_inv = ttk.Button(master=self, text="Inverse Thresholding", command=lambda: self.apply_thresholding(inverse=True))
        self.btn_thresh_inv.grid(row=3, column=0, sticky="WE")
        self.btn_thresh = ttk.Button(master=self, text="Adaptive Thresholding", command=lambda: self.apply_thresholding_adaptive())
        self.btn_thresh.grid(row=4, column=0, sticky="WE")
        self.btn_thresh_inv = ttk.Button(master=self, text="Adaptive Inverse Thresholding", command=lambda: self.apply_thresholding_adaptive(inverse=True))
        self.btn_thresh_inv.grid(row=5, column=0, sticky="WE")
        
        self.grid_columnconfigure(0, weight=1)        
        self.grid_rowconfigure(0, weight=1)
        self.canvas_main.create_rectangle(*self.FIELD_EDGE, tag="border")

    def load_image(self):
        fname = filedialog.askopenfilename(
            defaultextension="*.jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")],
            initialdir=Path(Path.cwd(), "files")
        )
        if fname:
            self.show_image(fname=str(fname))

    def show_image(self, fname):
        self.img_cv = cv.imread(str(fname), cv.IMREAD_UNCHANGED)
        self.img_cv = cv.resize(src=self.img_cv, dsize=scale_dim(self.img_cv, scale_factor=1, keep_aspect_ratio=True, fixed_width=230, fixed_height=170), interpolation=cv.INTER_AREA)
        self.img_holder = ImageTk.PhotoImage(Image.fromarray(cv.cvtColor(self.img_cv, cv.COLOR_BGR2RGB)))
        self.canvas_main.create_image((self.IMG_X, self.IMG_Y), image=self.img_holder, tag="imgae", anchor="nw")
        self.canvas_main.delete(self.canvas_main.find_withtag("border"))
        self.canvas_main.create_rectangle(*self.FIELD_EDGE)

    def apply_thresholding(self, inverse=False):
        threshold_type = cv.THRESH_BINARY, "BINARY"
        if inverse:
            threshold_type = cv.THRESH_BINARY_INV, "BINARY INVERSE"
        
        _img = cv.cvtColor(self.img_cv, cv.COLOR_RGB2GRAY)
        retval, img_thresholded = cv.threshold(src=_img, thresh=150, maxval=255, type=threshold_type[0])
        cv.imshow(winname=f"Thresholding via {threshold_type[1]}", mat=img_thresholded)
    
    def apply_thresholding_adaptive(self, inverse=False):
        threshold_type = cv.THRESH_BINARY, "BINARY"
        if inverse:
            threshold_type = cv.THRESH_BINARY_INV, "BINARY INVERSE"
        
        _img = cv.cvtColor(self.img_cv, cv.COLOR_RGB2GRAY)
        img_thresholded = cv.adaptiveThreshold(
            src=_img, maxValue=255, adaptiveMethod=cv.ADAPTIVE_THRESH_MEAN_C, thresholdType=threshold_type[0], blockSize=5, C=3)
        cv.imshow(winname=f"Adaptive Thresholding via {threshold_type[1]}", mat=img_thresholded)