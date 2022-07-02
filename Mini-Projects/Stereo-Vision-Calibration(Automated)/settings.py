import cv2 as cv

CAMERA_FRAME_SIZE = (320, 240)      # in pixels (width, height)
CHESSBOARD_SIZE = (7, 7)
CHESSBOARD_SQUARES_SIZE = 22  # mm

# termination criteria
TERMINATION_CRITERIA = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Source: https://shimat.github.io/opencvsharp_docs/html/040d5c3f-bd31-f5ff-76c8-106304d8135c.htm
CV2_BORDER_MODES = dict(
    constant=cv.BORDER_CONSTANT,        # 0     Border is filled with the fixed value, passed as last parameter of the function. `iiiiii|abcdefgh|iiiiiii` with some specified `i`
    replicate=cv.BORDER_REPLICATE,      # 1     The pixels from the top and bottom rows, the left-most and right-most columns are replicated to fill the border. `aaaaaa|abcdefgh|hhhhhhh`
    reflect=cv.BORDER_REFLECT,          # 2     `fedcba|abcdefgh|hgfedcb`
    wrap=cv.BORDER_WRAP,                # 3     `cdefgh|abcdefgh|abcdefg`
    reflect_101=cv.BORDER_REFLECT_101,  # 4     `gfedcb|abcdefgh|gfedcba`
    transparent=cv.BORDER_TRANSPARENT,  # 5     `uvwxyz|absdefgh|ijklmno`
    default=cv.BORDER_DEFAULT,          # 4     same as BORDER_REFLECT_101
    isolated=cv.BORDER_ISOLATED,        # 16    do not look outside of ROI
)

# Source: https://iq.opengenus.org/different-interpolation-methods-in-opencv/
CV2_INTERPOLATION_METHODS = dict(
    nearest=cv.INTER_NEAREST,           # 0
    linear=cv.INTER_LINEAR,             # 1
    cubic=cv.INTER_CUBIC,               # 2
    area=cv.INTER_AREA,                 # 3
    lanczos4=cv.INTER_LANCZOS4,         # 4
    linear_exact=cv.INTER_LINEAR_EXACT, # 5
    nearest_exact=cv.INTER_NEAREST_EXACT, # 6
    max=cv.INTER_MAX,                   # 7
    fill_outliers=cv.WARP_FILL_OUTLIERS, # 8
    inverse_map=cv.WARP_INVERSE_MAP,    # 16
)

class CameraSettings:
    camera_frame_size = (320, 240)  # pixel
    camera_focal_length = 10        # mm