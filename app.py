# In[] Libs
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from pages.basics import FrameReadImage, FrameReadVideo, FrameLoadImage
from pages.transformation import FrameManipulateImage, FrameTransformImage, FrameChangeColorSpaceImage
from pages.advanced_techniques import FrameSplitColorChannelsImage, FrameBlurImage, FrameMaskingImage
from pages.analyse_image import FrameHistogramImage, FrameThresholdingImage
from utils import set_dpi_awareness

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
        frm_advanced_techniques = ttk.Frame(master=self.notebook_main)
        frm_analyse_image = ttk.Frame(master=self.notebook_main)
        self.notebook_main.add(child=frm_basics, text="Basics")
        self.notebook_main.add(child=frm_transformation, text="Transformation")
        self.notebook_main.add(child=frm_advanced_techniques, text="Advanced Techniques")
        self.notebook_main.add(child=frm_analyse_image, text="Analyse Image")

        self.notebook_basics = ttk.Notebook(master=frm_basics, padding=self.PADDING_10)
        self.notebook_basics.grid(row=0, column=0, sticky="WENS")

        self.notebook_transformation = ttk.Notebook(master=frm_transformation, padding=self.PADDING_10)
        self.notebook_transformation.grid(row=0, column=0, sticky="WENS")
        
        self.notebook_advanced_techniques = ttk.Notebook(master=frm_advanced_techniques, padding=self.PADDING_10)
        self.notebook_advanced_techniques.grid(row=0, column=0, sticky="WENS")
        
        self.notebook_analyse_image = ttk.Notebook(master=frm_analyse_image, padding=self.PADDING_10)
        self.notebook_analyse_image.grid(row=0, column=0, sticky="WENS")

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
        # frm_read_video.load_video()

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
        frm_color_channels = FrameSplitColorChannelsImage(parent=self.notebook_advanced_techniques, fname=fname)
        self.notebook_advanced_techniques.add(child=frm_color_channels, text="Color Channels")
        frm_color_channels.load_image()
        
        # Blur Image Tab
        fname = Path(Path.cwd(), "files", "landscape_1.jpg")
        frm_blur_image = FrameBlurImage(parent=self.notebook_advanced_techniques, fname=fname)
        self.notebook_advanced_techniques.add(child=frm_blur_image, text="Blur Image")
        frm_blur_image.load_image()
        
        # Masking Image Tab
        fname = Path(Path.cwd(), "files", "cat_1.png")
        frm_masking_image = FrameMaskingImage(parent=self.notebook_advanced_techniques, fname=fname)
        self.notebook_advanced_techniques.add(child=frm_masking_image, text="Masking Image")
        frm_masking_image.load_image()
        
        # Histogram Image Tab
        frm_histogram_image = FrameHistogramImage(parent=self.notebook_analyse_image)
        self.notebook_analyse_image.add(child=frm_histogram_image, text="Histogram Image")
        
        # Histogram Image Tab
        frm_thresholding_image = FrameThresholdingImage(parent=self.notebook_analyse_image)
        self.notebook_analyse_image.add(child=frm_thresholding_image, text="Thresholding Image")
        
        self.notebook_main.select(tab_id=3)
        self.notebook_advanced_techniques.select(tab_id=2)
        
        

# In[] App
if __name__ == "__main__":
    set_dpi_awareness()
    app = App()
    app.grid_columnconfigure(0, weight=1)
    app.mainloop()