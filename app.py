# In[] Libs
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from pages.basics import (
    FrameReadImage, FrameReadVideo, FrameLoadImage, FrameManipulateImage,
    FrameTransformImage,
)

# In[] Layout
class App(tk.Tk):
    PADDING_10 = (10, 10, 10, 10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._init_notebook()
        self._init_tabs()

    def _init_notebook(self):
        self.notebook_main = ttk.Notebook(master=self, padding=self.PADDING_10)
        self.notebook_main.grid(row=0, column=0, sticky="WENS")
        self.notebook_main.grid_columnconfigure(0, weight=1)

    def _init_tabs(self):
        # Read Imgae Tab
        fname = Path(Path.cwd(), "files", "cat_1.png")
        frm_read_image = FrameReadImage(parent=self.notebook_main, fname=fname)
        self.notebook_main.add(child=frm_read_image, text="Read Image")
        frm_read_image.load_image()

        # Read Video Tab
        fname = Path(Path.cwd(), "files", "cat_1.mp4")
        frm_read_video = FrameReadVideo(parent=self.notebook_main, fname=fname)
        self.notebook_main.add(child=frm_read_video, text="Read Video")
        frm_read_video.load_video()

        # Load Image Tab
        frm_load_image = FrameLoadImage(parent=self.notebook_main)
        self.notebook_main.add(child=frm_load_image, text="Load Image")

        self.notebook_main.select(tab_id=1)

        # Manipulate Image Tab
        fname = Path(Path.cwd(), "files", "cat_4.jpg")
        frm_manipulate_image = FrameManipulateImage(parent=self.notebook_main, fname=fname)
        self.notebook_main.add(child=frm_manipulate_image, text="Manipulate Image")
        frm_manipulate_image.load_image()

        self.notebook_main.select(tab_id=3)

        # Transform Image Tab
        fname = Path(Path.cwd(), "files", "cat_3.jpg")
        frm_transform_image = FrameTransformImage(parent=self.notebook_main, fname=fname)
        self.notebook_main.add(child=frm_transform_image, text="Transform Image")
        frm_transform_image.load_image()

        self.notebook_main.select(tab_id=4)

# In[] App
if __name__ == "__main__":
    app = App()
    app.grid_columnconfigure(0, weight=1)
    app.mainloop()