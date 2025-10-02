from PIL import Image, ImageDraw, ImageFont
from pathlib import PosixPath, Path
import math

def create_image(color: tuple[int, int, int, int], size: tuple[int, int] = (720, 720),
                 sfile: PosixPath | Path | None = None) -> Image.Image:
    """
    Creates and return image. If specified, saves the image to the specified PosixPath | Path.

    Args:
        color (tuple): RGB color code with transparency variable at postion 4
        size (tuple): Width, Height of the Image
        sfile (PosixPath | Path | None): File to which you want to save your image to OR None to skip saving the image to a file

    Returns:
        Image.Image: Newly created Image
    """
    img = Image.new('RGBA', size, color)

    if type(sfile) is PosixPath or type(sfile) is Path:
        img.save(sfile)

    elif sfile is not None:
        raise TypeError(f"Can't use {type(sfile)} as name to save the image file. Use a PosixPath | Path type instead")
    
    return img

def load_image(img_path: PosixPath | Path) -> Image.Image:
    if type(img_path) is PosixPath or type(img_path) is Path: 
        return Image.open(img_path)
    else:
        raise TypeError("Please use Path or PosixPath as variable type for `img_path`")



def wrap_text(text: str, font: ImageFont.ImageFont | ImageFont.FreeTypeFont, max_width: float | int) -> list:
    """
    Wraps text around according to the width of the image.
    """
    lines = []
    words = text.split()
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        width = ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(test_line, font=font) 

        if width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    lines.append(' '.join(current_line)) # Add the last line
    return lines
    
def add_text(text: str, text_color: tuple[int, int, int, int], text_box_width: float | int,
             font: ImageFont.ImageFont | ImageFont.FreeTypeFont, nline_text: list | None = None, img: Image.Image | None = None, 
             img_path: PosixPath | Path | None = None, h_tbalign: str = "center", v_tbalign: str = "center",
             stroke_fill: tuple[int, int, int, int] | None = (255, 255, 255, 100), stroke_width: float = 2,
             align: str = "center", spacing: float = 4, h_indent: float = 0, v_indent: float = 0,
             sfile: PosixPath | Path | None = None) -> Image.Image:
    """
    Add text to the specified image and returns the new image with text.

    Args:
        text (str): Message you want to write over image
        text_color (tuple(int, int, int)): RBG color format for text color with transparency variable at postion 4
        font (ImageFont | FreeTypeFont): Font you want to use for the text
        img (Image | None): Image you want to use to overlay text onto
        img_path (Path | PosixPath | None): Image file path if img is not loaded
        stroke_fill (tuple(int, int, int)): RGB color format for text stroke color with transparency variable at postion 4
        stroke_width (float): Specify the width for stroke
        align (str): Align the text. Refer to PIL documentation for options: https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.text
        sfile (PosixPath | Path): File path to save the image to. If None, image will not be saved
    
    Returns:
        Image.Image: Newly edited image with text overlay
    """
    if img_path != None:
        img = Image.open(img_path)
        width, height = img.size
        draw = ImageDraw.Draw(img)
    else:
        try:
            if img != None:
                width, height = img.size
                draw = ImageDraw.Draw(img)
            else:
                raise TypeError("Please use PIL image types for variable `img`")
        except Exception as e:
            raise e
        
    wrapped_text = ""
    for line in wrap_text(text, font=font, max_width=text_box_width):
        wrapped_text += f"{line}\n"
    
    if nline_text is not None:
        for line in nline_text:
            wrapped_text += f"{line}\n"

    if h_tbalign == "center":
        _, _, w, _ = draw.textbbox((0, 0), wrapped_text, font=font)
        x_cord = ((width + h_indent) - w)/2
    elif h_tbalign == "left":
        x_cord = width - (width - h_indent)
    elif h_tbalign == "right":
        _, _, w, _ = draw.textbbox((0, 0), wrapped_text, font=font)
        x_cord = width - (w + h_indent)
    else:
        raise ValueError("Please enter a valid option - 'right', 'left' or 'center' for variable h_tbalign")

    if v_tbalign == "center":
        _, _, _, h = draw.textbbox((0, 0), wrapped_text, font=font)
        y_cord = ((height + v_indent) - h) / 2
    elif v_tbalign == "top":
        y_cord = height - (height - v_indent)
    elif v_tbalign == "bottom":
        _, _, _, h = draw.textbbox((0, 0), wrapped_text, font=font)
        y_cord = height - (h + v_indent)
    else:
        raise ValueError("Please enter a valid option - 'top', 'bottom' or 'center' for variable v_tbalign")

    if stroke_fill == None:
        stroke_width = 0
    
    draw.multiline_text((x_cord, y_cord), wrapped_text, fill=text_color, font=font, align=align, 
                        stroke_fill=stroke_fill, stroke_width=stroke_width, spacing=spacing)

    if type(sfile) is PosixPath or type(sfile) is Path:
        img.save(sfile)
    
    elif sfile is not None:
        raise TypeError(f"Can't use {type(sfile)} as name to save the image file. Use a PosixPath | Path type instead")

    return img

def load_font(file_name: PosixPath | Path | None = None, size: float | None = None) -> ImageFont.ImageFont | ImageFont.FreeTypeFont:
    """
    """
    
    if type(file_name) is PosixPath or type(file_name) is Path:
        if size != None:
            f = ImageFont.truetype(file_name, size)
        elif size == None:
            f = ImageFont.truetype(file_name)
        else:
            raise TypeError("Use float in variable `size` or None to set it to default value")

    elif file_name == None:
        f = ImageFont.load_default(size=size)

    else:
        raise TypeError("Use PosixPath or Path type for `file_name`")

    return f

def draw_checkers_pattern(color: tuple[int, int, int, int], spacing: float, img: Image.Image | None = None,
                         img_path: Path | PosixPath | None = None, sfile: Path | PosixPath | None = None):
    if img is None:
        if type(img_path) is Path or type(img_path) is PosixPath:
            img = Image.open(img_path)
        else:
            raise ValueError("Please use Image.Image type variable for img OR asign Path or Posix of image to img_path")
    draw = ImageDraw.Draw(img)
    width, height = img.size
    num_hlines = math.ceil(height / spacing)
    num_vlines = math.ceil(width / spacing)
    x_list = []
    y_list = []
    for num in range(1, num_hlines):
        x_list.append(spacing * num)
    for num in range(1, num_vlines):
        y_list.append(spacing * num)
    
    for x in x_list:
        draw.line([(0, x), (img.width, x)], fill=color)
    for y in y_list:
        draw.line([(y, 0), (y, img.height)], fill=color)

    if sfile is not None:
        if type(sfile) is PosixPath or type(sfile) is Path:
            img.save(sfile)
        else:
            raise ValueError("Please use Path or PosixPath type value for sfile to save the image to the given Path")

    return img
