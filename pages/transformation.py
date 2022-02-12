import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2 as cv
from utils.methods import scale_dim
import numpy as np

class FrameManipulateImage(tk.Frame):
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
        rd_option_2 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="Gray", value="Gray", command=self.option_changed)
        rd_option_2.grid(row=0, column=1)
        rd_option_3 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="Blur", value="Blur", command=self.option_changed)
        rd_option_3.grid(row=0, column=2)
        rd_option_4 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="Edges", value="Edges", command=self.option_changed)
        rd_option_4.grid(row=1, column=0)
        rd_option_5 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="Dilate", value="Dilate", command=self.option_changed)
        rd_option_5.grid(row=1, column=1)
        rd_option_6 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="Erode", value="Erode", command=self.option_changed)
        rd_option_6.grid(row=1, column=2)
        rd_option_7 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="Contour", value="Contour", command=self.option_changed)
        rd_option_7.grid(row=2, column=0)

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

        if option == "Reset":
            self.img_cv_current = self.img_cv.copy()
            self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv))
            self.canvas_main.itemconfigure(img, image=self.img_holder)
        elif option == "Gray":
            self.img_cv_current = self.img_cv.copy()
            self.img_cv_current = cv.cvtColor(self.img_cv_current, cv.COLOR_BGR2GRAY)
            self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.img_holder)
        elif option == "Blur":
            self.img_cv_current = cv.GaussianBlur(self.img_cv_current, ksize=(7, 7), sigmaX=cv.BORDER_DEFAULT)
            self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.img_holder)
        elif option == "Edges":
            self.img_cv_current = cv.Canny(self.img_cv_current, threshold1=10, threshold2=175)
            self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.img_holder)
        elif option == "Dilate":
            self.img_cv_current = cv.dilate(self.img_cv_current, kernel=(7, 7), iterations=3)
            self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.img_holder)
        elif option == "Erode":
            self.img_cv_current = cv.erode(self.img_cv_current, kernel=(7, 7), iterations=3)
            self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.img_holder)
        elif option == "Contour":
            img_blank = np.zeros(shape=self.img_cv.shape, dtype="uint8")
            self.img_cv_current = self.img_cv.copy()
            self.img_cv_current = cv.cvtColor(self.img_cv_current, cv.COLOR_BGR2GRAY)
            self.img_cv_current = cv.GaussianBlur(self.img_cv_current, ksize=(3, 3), sigmaX=cv.BORDER_DEFAULT)
            self.img_cv_current = cv.Canny(self.img_cv_current, threshold1=125, threshold2=175)
            contours, _hierarchies = cv.findContours(self.img_cv_current, mode=cv.RETR_LIST, method=cv.CHAIN_APPROX_SIMPLE)
            cv.drawContours(image=img_blank, contours=contours, contourIdx=-1, color=(0, 0, 255), thickness=3)
            self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.img_holder)

class FrameTransformImage(tk.Frame):
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
        self.frm_options.grid_columnconfigure((0, 1, 2), weight=1)
        for widget in self.frm_options.winfo_children():
            widget.grid_configure(padx=5, ipadx=5)

    def _init_transformers(self):
        btn_task_1 = ttk.Button(master=self.frm_options, text="Reset", command=lambda: self.task_changed(task="Reset"))
        btn_task_1.grid(row=0, column=0, sticky="WE")
        
        btn_task_21 = ttk.Button(master=self.frm_options, text="Rotate clockwise", command=lambda: self.task_changed(task="Rotate clockwise"))
        btn_task_21.grid(row=0, column=1, sticky="WE")
        btn_task_22 = ttk.Button(master=self.frm_options, text="Rotate counter-clockwise", command=lambda: self.task_changed(task="Rotate counter-clockwise"))
        btn_task_22.grid(row=1, column=1, sticky="WE")

        btn_task_31 = ttk.Button(master=self.frm_options, text="Flip horizontally", command=lambda: self.task_changed(task="Flip horizontally"))
        btn_task_31.grid(row=0, column=2, sticky="WE")
        btn_task_32 = ttk.Button(master=self.frm_options, text="Flip vertically", command=lambda: self.task_changed(task="Flip vertically"))
        btn_task_32.grid(row=1, column=2, sticky="WE")

    def load_image(self):
        self.img_cv = cv.imread(str(self.fname), cv.IMREAD_UNCHANGED)
        self.img_cv = cv.resize(src=self.img_cv, dsize=scale_dim(self.img_cv, keep_aspect_ratio=True, fixed_height=160), interpolation=cv.INTER_AREA)
        self.img_cv = cv.cvtColor(self.img_cv, cv.COLOR_BGR2RGB)
        self.img_cv_current = self.img_cv.copy()
        self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv))
        img_w, img_h = self.img_holder.width(), self.img_holder.height()

        self.canvas_main.create_image((self.IMG_X+img_w//2, self.IMG_Y+img_h//2), image=self.img_holder, tag="image", anchor="center")
        self.canvas_main.create_rectangle(*self.FIELD_EDGE_NW, self.img_holder.width()+30, self.img_holder.height()+30)

    def task_changed(self, task):
        img = self.canvas_main.find_withtag("image")

        if task == "Reset":
            self.img_cv_current = self.img_cv.copy()
            self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv))
            self.canvas_main.itemconfigure(img, image=self.img_holder)
        elif task == "Rotate clockwise":
            self.img_cv_current = cv.rotate(self.img_cv_current, rotateCode=cv.ROTATE_90_CLOCKWISE)
            self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.img_holder)
        elif task == "Rotate counter-clockwise":
            self.img_cv_current = cv.rotate(self.img_cv_current, rotateCode=cv.ROTATE_90_COUNTERCLOCKWISE)
            self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.img_holder)
        elif task == "Flip horizontally":
            self.img_cv_current = cv.flip(self.img_cv_current, flipCode=1)
            self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.img_holder)
        elif task == "Flip vertically":
            self.img_cv_current = cv.flip(self.img_cv_current, flipCode=0)
            self.img_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.img_holder)

class FrameChangeColorSpaceImage(tk.Frame):
    CANVAS_SIZE = (200, 200)
    CANVAS_BK_COLOR = "#317001"
    IMG_X, IMG_Y = 20, 20
    IMG_H, IMG_W = 0, 0

    def __init__(self, parent, fname_left, fname_right):
        tk.Frame.__init__(self, parent)
        self.fnames = [fname_left, fname_right]
        self.canvas_main = tk.Canvas(master=self, background=self.CANVAS_BK_COLOR, width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self.canvas_main.grid(row=0, column=0, sticky="WENS")
        self.canvas_main = tk.Canvas(master=self, background=self.CANVAS_BK_COLOR, width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self.canvas_main.grid(row=0, column=0, sticky="WENS")
        self.frm_options = ttk.Frame(master=self)
        self.frm_options.grid(row=1, column=0)
        
        self._init_manipulators()        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        for widget in self.frm_options.winfo_children():
            widget.grid_configure(padx=5, ipadx=5, sticky="W")

    def _init_manipulators(self):
        self.var_options = tk.StringVar(master=self, value="Normal")
        rd_option_1 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="RGB", value="RGB", command=self.option_changed)
        rd_option_1.grid(row=0, column=0)
        rd_option_2 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="Gray", value="Gray", command=self.option_changed)
        rd_option_2.grid(row=0, column=1)
        rd_option_3 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="HSV", value="HSV", command=self.option_changed)
        rd_option_3.grid(row=0, column=2)
        rd_option_4 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="LAB", value="LAB", command=self.option_changed)
        rd_option_4.grid(row=1, column=0)
        rd_option_5 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="BGR", value="BGR", command=self.option_changed)
        rd_option_5.grid(row=1, column=1)
        rd_option_6 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="HLS", value="HLS", command=self.option_changed)
        rd_option_6.grid(row=1, column=2)
        rd_option_7 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="LUV", value="LUV", command=self.option_changed)
        rd_option_7.grid(row=2, column=0)
        rd_option_8 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="YUV", value="YUV", command=self.option_changed)
        rd_option_8.grid(row=2, column=1)
        rd_option_9 = ttk.Radiobutton(master=self.frm_options, variable=self.var_options, text="XYZ", value="XYZ", command=self.option_changed)
        rd_option_9.grid(row=2, column=2)

    def load_image(self):
        # Left Image
        self.img_cv_left = cv.imread(str(self.fnames[0]), cv.IMREAD_UNCHANGED)
        self.img_cv_left = cv.resize(src=self.img_cv_left, dsize=scale_dim(self.img_cv_left, keep_aspect_ratio=True, fixed_height=90), interpolation=cv.INTER_AREA)
        self.img_cv_left = cv.cvtColor(self.img_cv_left, cv.COLOR_BGR2RGB)
        self.img_cv_current_left = self.img_cv_left.copy()
        self.img_holder_left = ImageTk.PhotoImage(Image.fromarray(self.img_cv_left))

        self.canvas_main.create_image((self.IMG_X+self.img_holder_left.width()//2, self.IMG_Y+self.img_holder_left.height()//2), image=self.img_holder_left, tag="image_left", anchor="center")
        self.canvas_main.create_rectangle(10, 11, self.img_holder_left.width()+30, self.img_holder_left.height()+30)

        # Right Image    
        self.img_cv_right = cv.imread(str(self.fnames[1]), cv.IMREAD_UNCHANGED)
        self.img_cv_right = cv.resize(src=self.img_cv_right, dsize=scale_dim(self.img_cv_right, keep_aspect_ratio=True, fixed_height=90), interpolation=cv.INTER_AREA)
        self.img_cv_right = cv.cvtColor(self.img_cv_right, cv.COLOR_BGR2RGB)
        self.img_cv_current_right = self.img_cv_right.copy()
        self.img_holder_right = ImageTk.PhotoImage(Image.fromarray(self.img_cv_right))

        self.canvas_main.create_image((self.IMG_X+self.img_holder_left.width()+38+self.img_holder_right.width()//2, self.IMG_Y+self.img_holder_left.height()//2), image=self.img_holder_right, tag="image_right", anchor="center")
        self.canvas_main.create_rectangle(40+self.img_holder_left.width(), 11, 40+self.img_holder_left.width()+self.img_holder_right.width()+30, self.img_holder_right.height()+30)

    def option_changed(self):
        option = self.var_options.get()
        img_left = self.canvas_main.find_withtag("image_left")
        img_right = self.canvas_main.find_withtag("image_right")
        color_space = cv.COLOR_BGR2RGB

        if option == "RGB":
            pass
        elif option == "Gray":  
            color_space = cv.COLOR_RGB2GRAY 
        elif option == "HSV":
            color_space = cv.COLOR_RGB2HSV
        elif option == "LAB":
            color_space = cv.COLOR_RGB2LAB
        elif option == "BGR":
            color_space = cv.COLOR_RGB2BGR
        elif option == "HLS":
            color_space = cv.COLOR_RGB2HLS
        elif option == "LUV":
            color_space = cv.COLOR_RGB2LUV        
        elif option == "YUV":
            color_space = cv.COLOR_RGB2YUV
        elif option == "XYZ":
            color_space = cv.COLOR_RGB2XYZ
        else:
            return

        self.img_cv_current_left = self.img_cv_left.copy()
        self.img_cv_current_right = self.img_cv_right.copy()
        if option != "RGB":
            self.img_cv_current_left = cv.cvtColor(self.img_cv_current_left, color_space)
            self.img_cv_current_right = cv.cvtColor(self.img_cv_current_right, color_space)
        self.img_holder_left = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current_left))
        self.canvas_main.itemconfigure(img_left, image=self.img_holder_left)
        self.img_holder_right = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current_right))
        self.canvas_main.itemconfigure(img_right, image=self.img_holder_right)

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

