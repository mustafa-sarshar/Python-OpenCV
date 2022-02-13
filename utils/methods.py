def scale_dim(img, scale_factor=0.5, keep_aspect_ratio=False, fixed_height=170, fixed_width=230):
    """
    This method works for video, image and live video as well.
    """
    width = int(img.shape[1] * scale_factor)
    height = int(img.shape[0] * scale_factor)

    if fixed_width >= fixed_height:    
        if keep_aspect_ratio and fixed_height:
            height_percent = (fixed_height / float(height))
            width = int((float(width) * float(height_percent)))
            height = fixed_height
    else:
        if keep_aspect_ratio and fixed_width:
            width_percent = (fixed_width / float(width))
            height = int((float(height) * float(width_percent)))
            width = fixed_width

    return (width, height)