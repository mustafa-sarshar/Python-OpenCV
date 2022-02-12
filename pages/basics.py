from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2 as cv
import threading
from ffpyplayer.player import MediaPlayer
from pyparsing import col
from sklearn.feature_extraction import image
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
        
        self.grid_columnconfigure(0, weight=1)

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
        self.canvas_main.grid(row=0, columnspan=2, sticky="WENS")
        self.var_video_info = tk.StringVar(master=self, value="")
        self.lbl_video_info = ttk.Label(master=self, textvariable=self.var_video_info, background="")
        self.lbl_video_info.place(x=0, y=0, anchor="center")
        self.var_stop_video = tk.BooleanVar(master=self, value=False)
        self.chkbox_stop_video = ttk.Checkbutton(master=self, text="Stop Video", variable=self.var_stop_video, command=self.btn_stop_video_changed)
        self.chkbox_stop_video.grid(row=1, column=0, sticky="WE")
        self.var_mute_video = tk.BooleanVar(master=self, value=False)
        self.chkbox_mute_video = ttk.Checkbutton(master=self, text="Mute Audio", variable=self.var_mute_video, state="disabled")
        self.chkbox_mute_video.grid(row=1, column=1, sticky="WE")
        
        self.grid_columnconfigure(0, weight=1)

    def btn_stop_video_changed(self):
        stop_video = self.var_stop_video.get()
        self.var_mute_video.set(stop_video)

    def load_video(self):
        self.cap = cv.VideoCapture(str(self.fname))
        # self.player = MediaPlayer(str(self.fname))
        self.video_thread = threading.Thread(target=self.show_video, daemon=True)
        self.video_thread.start()

    def show_video(self):
        if self.cap:
            success = True
            self.canvas_main.create_rectangle(*self.FIELD_EDGE)
            while success:
                if not self.var_stop_video.get():
                    success, video = self.cap.read()
                    _video_info = f"Frame: {self.cap.get(1):.0f} / {self.cap.get(7):.0f}"
                    self.var_video_info.set(_video_info)
                    self.lbl_video_info.place(x=self.CANVAS_SIZE[0]//2-len(_video_info)//2, y=self.CANVAS_SIZE[1]//2+40)
                    # audio_frame, val = self.player.get_frame()
                    # if not self.var_mute_video.get():
                        # self.player.set_mute(0)
                        # if audio_frame:
                        #     img, t = audio_frame
                        #     print(val, t, img.get_pixel_format(), img.get_buffer_size())
                    # else:
                    #     self.player.set_mute(1)
                    if success:# and audio_frame:
                        video = cv.resize(src=video, dsize=scale_dim(video, keep_aspect_ratio=True, fixed_width=160), interpolation=cv.INTER_AREA)
                        self.video_holder = ImageTk.PhotoImage(Image.fromarray(cv.cvtColor(video, cv.COLOR_BGR2RGB)))
                        self.canvas_main.create_image((self.VIDEO_X, self.VIDEO_Y), image=self.video_holder, tag="video", anchor="nw")
                        cv.waitKey(30)
                else:
                    # self.player.set_mute(1)
                    cv.waitKey(-1)
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
        
        self.grid_columnconfigure(0, weight=1)

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

class FrameManipulateImage(tk.Frame):
    CANVAS_SIZE = (200, 200)
    CANVAS_BK_COLOR = "#317001"
    FIELD_EDGE_NW = (10, 11)
    IMG_X, IMG_Y = 20, 20

    def __init__(self, parent, fname):
        tk.Frame.__init__(self, parent)
        print(self, parent)
        self.fname = fname
        self.canvas_main = tk.Canvas(master=self, background=self.CANVAS_BK_COLOR, width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self.canvas_main.grid(row=0, column=0, sticky="WENS")
        self.frm_options = ttk.Frame(master=self)
        self.frm_options.grid(row=1, column=0)
        
        self._init_manipulators()
        
        self.grid_columnconfigure(0, weight=1)

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

    def load_image(self):
        self.img_cv = cv.imread(str(self.fname), cv.IMREAD_UNCHANGED)
        self.img_cv = cv.resize(src=self.img_cv, dsize=scale_dim(self.img_cv, keep_aspect_ratio=True, fixed_height=160), interpolation=cv.INTER_AREA)
        self.img_cv_current = self.img_cv.copy()
        self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(cv.cvtColor(self.img_cv, cv.COLOR_BGR2RGB)))

        self.canvas_main.create_image((self.IMG_X+self.imgae_holder.width()//2, self.IMG_Y+self.imgae_holder.height()//2), image=self.imgae_holder, tag="image", anchor="center")
        self.canvas_main.create_rectangle(*self.FIELD_EDGE_NW, self.imgae_holder.width()+30, self.imgae_holder.height()+30)

    def option_changed(self):
        option = self.var_options.get()
        img = self.canvas_main.find_withtag("image")

        if option == "Reset":
            self.img_cv_current = self.img_cv.copy()
            self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(cv.cvtColor(self.img_cv, cv.COLOR_BGR2RGB)))
            self.canvas_main.itemconfigure(img, image=self.imgae_holder)
        elif option == "Gray":
            self.img_cv_current = self.img_cv.copy()
            self.img_cv_current = cv.cvtColor(self.img_cv_current, cv.COLOR_BGR2GRAY)
            self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.imgae_holder)
        elif option == "Blur":
            self.img_cv_current = cv.GaussianBlur(self.img_cv_current, ksize=(7, 7), sigmaX=cv.BORDER_DEFAULT)
            self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.imgae_holder)
        elif option == "Edges":
            self.img_cv_current = cv.Canny(self.img_cv_current, threshold1=10, threshold2=175)
            self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.imgae_holder)
        elif option == "Dilate":
            self.img_cv_current = cv.dilate(self.img_cv_current, kernel=(7, 7), iterations=3)
            self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.imgae_holder)
        elif option == "Erode":
            self.img_cv_current = cv.erode(self.img_cv_current, kernel=(7, 7), iterations=3)
            self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.imgae_holder)

class FrameTransformImage(tk.Frame):
    CANVAS_SIZE = (200, 200)
    CANVAS_BK_COLOR = "#317001"
    FIELD_EDGE_NW = (10, 11)
    IMG_X, IMG_Y = 20, 20

    def __init__(self, parent, fname):
        tk.Frame.__init__(self, parent)
        print(self, parent)
        self.fname = fname
        self.canvas_main = tk.Canvas(master=self, background=self.CANVAS_BK_COLOR, width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self.canvas_main.grid(row=0, column=0, sticky="WENS")
        self.frm_options = ttk.Frame(master=self)
        self.frm_options.grid(row=1, column=0)

        self._init_transformers()

        self.grid_columnconfigure(0, weight=1)

    def _init_transformers(self):
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

    def load_image(self):
        self.img_cv = cv.imread(str(self.fname), cv.IMREAD_UNCHANGED)
        self.img_cv = cv.resize(src=self.img_cv, dsize=scale_dim(self.img_cv, keep_aspect_ratio=True, fixed_height=160), interpolation=cv.INTER_AREA)
        self.img_cv_current = self.img_cv.copy()
        self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(cv.cvtColor(self.img_cv, cv.COLOR_BGR2RGB)))

        self.canvas_main.create_image((self.IMG_X+self.imgae_holder.width()//2, self.IMG_Y+self.imgae_holder.height()//2), image=self.imgae_holder, tag="image", anchor="center")
        self.canvas_main.create_rectangle(*self.FIELD_EDGE_NW, self.imgae_holder.width()+30, self.imgae_holder.height()+30)

    def option_changed(self):
        option = self.var_options.get()
        img = self.canvas_main.find_withtag("image")

        if option == "Reset":
            self.img_cv_current = self.img_cv.copy()
            self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(cv.cvtColor(self.img_cv, cv.COLOR_BGR2RGB)))
            self.canvas_main.itemconfigure(img, image=self.imgae_holder)
        elif option == "Gray":
            self.img_cv_current = self.img_cv.copy()
            self.img_cv_current = cv.cvtColor(self.img_cv_current, cv.COLOR_BGR2GRAY)
            self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.imgae_holder)
        elif option == "Blur":
            self.img_cv_current = cv.GaussianBlur(self.img_cv_current, ksize=(7, 7), sigmaX=cv.BORDER_DEFAULT)
            self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.imgae_holder)
        elif option == "Edges":
            self.img_cv_current = cv.Canny(self.img_cv_current, threshold1=10, threshold2=175)
            self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.imgae_holder)
        elif option == "Dilate":
            self.img_cv_current = cv.dilate(self.img_cv_current, kernel=(7, 7), iterations=3)
            self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.imgae_holder)
        elif option == "Erode":
            self.img_cv_current = cv.erode(self.img_cv_current, kernel=(7, 7), iterations=3)
            self.imgae_holder = ImageTk.PhotoImage(Image.fromarray(self.img_cv_current))
            self.canvas_main.itemconfigure(img, image=self.imgae_holder)
