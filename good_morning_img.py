from PIL import Image, ImageDraw, ImageFont
import requests

try:
    with open("input_image.jpg", "wb") as f:
        f.write(requests.get(url="https://picsum.photos/720/720/?blur=2").content)
    img = Image.open("input_image.jpg")
except FileNotFoundError:
    print("input_image.jpg not found. Creating a new image for demonstration.")
    img = Image.new('RGB', (400, 200), color = 'white')

width, height = img.size
# Create a drawing context
draw = ImageDraw.Draw(img)

# Define the text and font
def wrap_text(text, font, max_width):
    lines = []
    words = text.split()
    current_line = []

    for word in words:
        # Check the width of the current line with the new word added
        test_line = ' '.join(current_line + [word])
        width = ImageDraw.Draw(Image.new('RGB', (1, 1))).textlength(test_line, font=font) 

        if width <= max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    lines.append(' '.join(current_line)) # Add the last line
    return lines

font_path = "arial.ttf"  # Replace with the path to your desired font file (e.g., a .ttf file)
font_size = width * 7/100

try:
    font = ImageFont.truetype(font_path, font_size)
except IOError:
    print(f"Font file '{font_path}' not found. Using default font.")
    font = ImageFont.load_default(size=font_size)

# Getting fun good morning quotes
# q = requests.get(url="https://ron-swanson-quotes.herokuapp.com/v2/quotes").json()[0]
# q = requests.get(url="https://api.kanye.rest").json()["quote"]
q = requests.get(url="https://api.realinspire.live/v1/quotes/random").json()[0]["content"]
print(q)
wrapped_text = wrap_text(q, font, width * 0.8)
text = ""
for line in wrapped_text:
    text += f"{line}\n"
text += "\nGood Morning!!"

_, _, w, h = draw.textbbox((0, 0), text, font=font)
# Define the text color and position
text_color = (0, 0, 0)  # Red color (RGB)
text_position = ((width-w)/2, (height-h)/2)  # X, Y coordinates
# Add the text to the image
draw.text(text_position, text, fill=text_color, font=font, align="center", stroke_fill=(255, 255, 255), stroke_width=2)

# Save the modified image
img.save("output_image_with_text.jpg")

print("Text added to image successfully!")