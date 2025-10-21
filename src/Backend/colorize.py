import colorsys

import randomcolor
from PIL import Image


def get_random_color():
    return randomcolor.RandomColor().generate()


def convert_hex_to_rgb(hex_code: str) -> tuple:
    h = hex_code.lstrip("#")
    t: list = []
    for i in (0, 2, 4):
        t.append(int(h[i : i + 2], 16))
    return tuple(t)


def get_contrast_color(rgb, max_contrast=192):
    """
    Get contrast color in monochrome.

    :param rgb: tuple or list of (r, g, b), each 0–255
    :param max_contrast: maximum contrast, 128–255
    :return: (r, g, b) tuple of contrast color
    """
    r, g, b = rgb
    min_contrast = 128

    # Calculate luma (brightness)
    y = round(0.299 * r + 0.587 * g + 0.114 * b)

    # Opposite brightness
    oy = 255 - y
    dy = oy - y

    if abs(dy) > max_contrast:
        dy = (1 if dy > 0 else -1) * max_contrast
        oy = y + dy
    elif abs(dy) < min_contrast:
        dy = (1 if dy > 0 else -1) * min_contrast
        oy = y + dy

    # Return monochrome color
    return oy, oy, oy, 100


def get_complementary_hsl(rgb):
    """
    Calculates a complementary color using HSL color space.
    Assumes RGB values are between 0 and 255.
    Returns RGB values between 0 and 255.
    """

    r, g, b = rgb

    # Convert RGB → HLS
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)

    # Pick complementary hue (opposite on color wheel)
    h = (h + 0.5) % 1.0

    # Ensure lightness is opposite (if bg is dark, make text light)
    l = 0.85 if l < 0.5 else 0.15

    # Keep saturation decent
    s = max(0.5, s)

    # Convert back to RGB
    r2, g2, b2 = colorsys.hls_to_rgb(h, l, s)
    r2, g2, b2 = int(r2 * 255), int(g2 * 255), int(b2 * 255)
    return r2, g2, b2, 100


def get_best_text_color(img: Image.Image) -> tuple[int, int, int, int]:
    """
    Analyzes an image, finds the dominant color,
    and returns a good contrasting text color in hex.
    """
    pixels = list(img.getdata())
    r = sum([p[0] for p in pixels]) / len(pixels)
    g = sum([p[1] for p in pixels]) / len(pixels)
    b = sum([p[2] for p in pixels]) / len(pixels)

    return get_complementary_hsl((r, g, b))


def get_darker_shade(rgb_color: tuple[int, int, int]) -> tuple[int, int, int, int]:
    r, g, b = rgb_color
    r, g, b = r / 255, g / 255, b / 255
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    darker_l = max(0, l * 50 / 100)  # Ensure it doesn't go below 0
    darker_r, darker_g, darker_b = colorsys.hls_to_rgb(h, darker_l, s)

    return int(darker_r * 255), int(darker_g * 255), int(darker_b * 255), 100
