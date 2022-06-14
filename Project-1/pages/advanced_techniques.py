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

class FrameBlurImage(tk.Frame):
    CANVAS_SIZE = (200, 200)
    CANVAS_BK_COLOR = "#317001"
    FIELD_EDGE_NW = (10, 11)
    IMG_X, IMG_Y = 20, 20
    IMG_H, IMG_W = 0, 0

    def __init__(self, parent, fname):
        tk.Frame.__init__(self, parent)
        self.fname = fname
        self.canvas_main = tk.Canvas(master=self, background=self.CANVAS_BK_COLOR, width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self.canvas_main.grid(row=0, column=0, sticky="WENS")
        self.frm_options = ttk.Frame(master=self)
        self.frm_options.grid(row=1, column=0)

        self._init_manipulators()
        self.grid_columnconfigure(0, weight=1)
        for widget in self.frm_options.winfo_children():
            widget.grid_configure(padx=5, ipadx=5, sticky="W")

    def _init_manipulators(self):
        self.var_options = tk.StringVar(master=self, value="Normal")
        rd_option_1 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="Reset", value="Reset", command=self.option_changed)
        rd_option_1.grid(row=0, column=0)
        rd_option_2 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="Average Blur", value="Average Blur", command=self.option_changed)
        rd_option_2.grid(row=0, column=1)
        rd_option_3 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="Gaussian Blur", value="Gaussian Blur", command=self.option_changed)
        rd_option_3.grid(row=0, column=2)
        rd_option_4 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="Median Blur", value="Median Blur", command=self.option_changed)
        rd_option_4.grid(row=1, column=1)
        rd_option_5 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="Bilateral Blur", value="Bilateral Blur", command=self.option_changed)
        rd_option_5.grid(row=1, column=2)

    def load_image(self):
        self.img_cv = cv.imread(str(self.fname), cv.IMREAD_UNCHANGED)
        self.img_cv = cv.resize(src=self.img_cv, dsize=scale_dim(self.img_cv, keep_aspect_ratio=True, fixed_height=160), interpolation=cv.INTER_AREA)
        self.img_cv = cv.cvtColor(self.img_cv, cv.COLOR_BGR2RGB)
        self.img_cv_current = self.img_cv.copy()
        # self.IMG_H, self.IMG_W, channels = self.img_cv.shape
        self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv))

        self.canvas_main.create_image((self.IMG_X+self.img_holder.width()//2, self.IMG_Y+self.img_holder.height()//2), image=self.img_holder, tag="image", anchor="center")
        self.canvas_main.create_rectangle(*self.FIELD_EDGE_NW, self.img_holder.width()+30, self.img_holder.height()+30)

    def option_changed(self):
        option = self.var_options.get()
        img = self.canvas_main.find_withtag("image")
        self.img_cv_current = self.img_cv.copy()
        
        if option == "Reset":
            pass
        elif option == "Average Blur":
            self.img_cv_current = cv.blur(src=self.img_cv_current, ksize=(5, 5))
        elif option == "Gaussian Blur":
            self.img_cv_current = cv.GaussianBlur(src=self.img_cv_current, ksize=(5, 5), sigmaX=cv.BORDER_DEFAULT)
        elif option == "Median Blur":
            self.img_cv_current = cv.medianBlur(src=self.img_cv_current, ksize=5)
        elif option == "Bilateral Blur":
            self.img_cv_current = cv.bilateralFilter(src=self.img_cv_current, d=50, sigmaColor=100, sigmaSpace=75)
        else:
            return

        self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
        self.canvas_main.itemconfigure(img, image=self.img_holder)

class FrameMaskingImage(tk.Frame):
    CANVAS_SIZE = (200, 230)
    CANVAS_BK_COLOR = "#317001"
    FIELD_EDGE_NW = [10, 11]
    IMG_X, IMG_Y = 20, 20
    IMG_H, IMG_W = 0, 0

    def __init__(self, parent, fname):
        tk.Frame.__init__(self, parent)
        self.fname = fname
        self.canvas_main = tk.Canvas(master=self, background=self.CANVAS_BK_COLOR, width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self.canvas_main.grid(row=0, column=0, sticky="WENS")
        self.frm_options = ttk.Frame(master=self)
        self.frm_options.grid(row=1, column=0)

        self._init_manipulators()
        self.grid_columnconfigure(0, weight=1)
        for widget in self.frm_options.winfo_children():
            widget.grid_configure(padx=5, ipadx=5, sticky="W")

    def _init_manipulators(self):
        self.var_options = tk.StringVar(master=self, value="Normal")
        rd_option_1 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="Reset", value="Reset", command=self.option_changed)
        rd_option_1.grid(row=0, column=0)
        rd_option_2 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="AND", value="AND", command=self.option_changed)
        rd_option_2.grid(row=0, column=1)
        rd_option_3 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="OR", value="OR", command=self.option_changed)
        rd_option_3.grid(row=0, column=2)
        rd_option_4 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="XOR", value="XOR", command=self.option_changed)
        rd_option_4.grid(row=1, column=1)
        rd_option_5 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="NOT", value="NOT", command=self.option_changed)
        rd_option_5.grid(row=1, column=2)

    def load_image(self):
        self.img_cv = cv.imread(str(self.fname), cv.IMREAD_UNCHANGED)
        self.img_cv = cv.resize(src=self.img_cv, dsize=scale_dim(self.img_cv, keep_aspect_ratio=True, fixed_width=80), interpolation=cv.INTER_AREA)
        self.img_cv = cv.cvtColor(self.img_cv, cv.COLOR_BGR2RGB)
        self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv))
        self.canvas_main.create_image((self.IMG_X+self.img_holder.width()//2, self.IMG_Y+self.img_holder.height()//2), image=self.img_holder, tag="image", anchor="center")
        self.canvas_main.create_rectangle(*self.FIELD_EDGE_NW, self.img_holder.width()+30, self.img_holder.height()+30)
        
        self.img_mask = np.zeros(shape=self.img_cv.shape[:2], dtype="uint8")
        self.img_mask = cv.circle(img=self.img_mask, center=(self.img_mask.shape[0]//2, self.img_mask.shape[1]//2), radius=self.img_mask.shape[0]//4, color=255, thickness=-1)
        self.img_mask[65:80, :] = 255
        self.img_mask[:10, :] = 255
        self.img_mask_holder = ImageTk.PhotoImage(Image.fromarray(self.img_mask))
        self.canvas_main.create_image((self.IMG_X+self.img_mask_holder.width()//2, 10+self.img_mask_holder.height()*2), image=self.img_mask_holder, tag="mask", anchor="center")
        self.canvas_main.create_rectangle(self.FIELD_EDGE_NW[0], self.FIELD_EDGE_NW[1]+self.img_holder.height()+30, self.img_holder.width()+30, (self.img_holder.height()+30)*2)

        self.img_result = self.img_cv.copy()
        self.img_holder_result = ImageTk.PhotoImage(Image.fromarray(self.img_result))
        self.canvas_main.create_image(200, 125, image=self.img_holder_result, tag="result", anchor="center")
        self.canvas_main.create_rectangle(150, 75, 145+self.img_holder_result.width()+25, 75+self.img_holder_result.height()+20)

    def option_changed(self):
        option = self.var_options.get()
        img = self.canvas_main.find_withtag("result")
        self.img_result = self.img_cv.copy()
        
        if option == "Reset":
            pass
        elif option == "AND":
            self.img_result = cv.bitwise_and(src1=self.img_result, src2=self.img_result, mask=self.img_mask)
        elif option == "OR":
            self.img_result = cv.bitwise_or(src1=self.img_result, src2=self.img_result, mask=self.img_mask)
        elif option == "XOR":
            self.img_result = cv.bitwise_xor(src1=self.img_result, src2=self.img_result, mask=self.img_mask)
        elif option == "NOT":
            self.img_result = cv.bitwise_not(src=self.img_result, mask=self.img_mask)
        else:
            return

        self.img_holder_result = ImageTk.PhotoImage(Image.fromarray(self.img_result))
        self.canvas_main.itemconfigure(img, image=self.img_holder_result)
