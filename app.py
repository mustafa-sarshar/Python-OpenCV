# In[] Libs
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from pages.basics import FrameReadImage, FrameReadVideo, FrameLoadImage
from pages.transformation import FrameManipulateImage, FrameTransformImage, FrameChangeColorSpaceImage, FrameSplitColorChannelsImage

# In[] Layout
class App(tk.Tk):
    PADDING_10 = (10, 10, 10, 10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._init_notebook()
        self._init_tabs()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _init_notebook(self):
        self.notebook_main = ttk.Notebook(master=self, padding=self.PADDING_10)
        frm_basics = ttk.Frame(master=self.notebook_main)
        frm_transformation = ttk.Frame(master=self.notebook_main)
        self.notebook_main.add(child=frm_basics, text="Basics")
        self.notebook_main.add(child=frm_transformation, text="Transformation")

        self.notebook_basics = ttk.Notebook(master=frm_basics, padding=self.PADDING_10)
        self.notebook_basics.grid(row=0, column=0, sticky="WENS")

        self.notebook_transformation = ttk.Notebook(master=frm_transformation, padding=self.PADDING_10)
        self.notebook_transformation.grid(row=0, column=0, sticky="WENS")

        self.notebook_main.grid(row=0, column=0, sticky="WENS")
        self.notebook_main.grid_columnconfigure(0, weight=1)

    def _init_tabs(self):
        # Read Imgae Tab
        fname = Path(Path.cwd(), "files", "cat_1.png")
        frm_read_image = FrameReadImage(parent=self.notebook_basics, fname=fname)
        self.notebook_basics.add(child=frm_read_image, text="Read Image")
        frm_read_image.load_image()

        # Read Video Tab
        fname = Path(Path.cwd(), "files", "cat_1.mp4")
        frm_read_video = FrameReadVideo(parent=self.notebook_basics, fname=fname)
        self.notebook_basics.add(child=frm_read_video, text="Read Video")
        frm_read_video.load_video()

        # Load Image Tab
        frm_load_image = FrameLoadImage(parent=self.notebook_basics)
        self.notebook_basics.add(child=frm_load_image, text="Load Image")

        # Manipulate Image Tab
        fname = Path(Path.cwd(), "files", "cat_4.jpg")
        frm_manipulate_image = FrameManipulateImage(parent=self.notebook_transformation, fname=fname)
        self.notebook_transformation.add(child=frm_manipulate_image, text="Manipulate")
        frm_manipulate_image.load_image()

        # Transform Image Tab
        fname = Path(Path.cwd(), "files", "cat_3.jpg")
        frm_transform_image = FrameTransformImage(parent=self.notebook_transformation, fname=fname)
        self.notebook_transformation.add(child=frm_transform_image, text="Transform")
        frm_transform_image.load_image()
        
        # Change Color Space Image Tab
        fname_left = Path(Path.cwd(), "files", "landscape_1.jpg")
        fname_right = Path(Path.cwd(), "files", "landscape_2.jpg")
        frm_color_spaces = FrameChangeColorSpaceImage(parent=self.notebook_transformation, fname_left=fname_left, fname_right=fname_right)
        self.notebook_transformation.add(child=frm_color_spaces, text="Color Spaces")
        frm_color_spaces.load_image()
        
        # Split Color Channels of Image Tab
        fname = Path(Path.cwd(), "files", "landscape_3.jpg")
        frm_color_channels = FrameSplitColorChannelsImage(parent=self.notebook_transformation, fname=fname)
        self.notebook_transformation.add(child=frm_color_channels, text="Color Channels")
        frm_color_channels.load_image()
        
        self.notebook_main.select(tab_id=1)
        self.notebook_transformation.select(tab_id=3)

# In[] App
if __name__ == "__main__":
    app = App()
    app.grid_columnconfigure(0, weight=1)
    app.mainloop()