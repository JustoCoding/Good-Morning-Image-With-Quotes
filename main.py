from src import Image_editor as ie
from src import colorize as colorize
from pathlib import Path
import requests

# Setting our Color Pallete
color_hex = colorize.get_random_color()[0]
color = colorize.convert_hex_to_rgb(color_hex)
text_color = colorize.get_complementary_hsl(color[:3])
darker_color = colorize.get_darker_shade((color[0], color[1], color[2]))

# Creating an image with a color and saving it to a file path
img = ie.create_image(size=(1440, 1440), color=color, sfile=Path("data/images/Test-Image1.png"))

# Loading a prefered font with a specified size. Could load a default font by keeping file_name = None
font = ie.load_font(file_name=Path("data/Fonts/DancingScript.ttf"), size=img.width * 9/100)

# Gaining a random quote from the api
q = requests.get(url="https://api.realinspire.live/v1/quotes/random").json()[0]

# Drawing a checkers_pattern on top of the image
img = ie.draw_checkers_pattern(img=img, color=darker_color, spacing=img.width * 5/100)

# Writing quote on left
img = ie.add_text(img=img, text=q["content"], text_box_width=img.width * 70/100, text_color=text_color, font=font,
                    align="left", spacing=20, stroke_fill=None, h_tbalign="left", v_tbalign="center",
                    h_indent=img.width * 7/100, v_indent=-(img.height * (7/100)), nline_text=[f"        - {q["author"]}"])

# Adding Good Morning Greeting at the bottom
img = ie.add_text(img=img, text="Good Morning!!!", text_box_width=img.width * 70/100, text_color=darker_color, font=font,
                    align="center", spacing=20, stroke_fill=None, h_tbalign="center", v_tbalign="bottom", v_indent=img.height * 7/100)

# Saving the newly created image to a file path
img.save(Path("data/images/Test-Image2.png"))
