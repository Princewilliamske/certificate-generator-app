from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)

# Certificate generation route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        template_path = "Korina Villanueva.png"  # Template image
        output_path = "generated_certificate.pdf"

        # Generate the certificate with the name
        generate_certificate(template_path, name, output_path)

        return send_file(
            output_path, as_attachment=True, download_name="certificate.pdf"
        )
    return render_template("index.html")


def generate_certificate(template_path, name, output_path):
    # Load the certificate template
    image = Image.open(template_path)
    draw = ImageDraw.Draw(image)

    # Define font and text position
    font_path = "goodvibes.ttf"  # Path to a TTF font file
    font_size = 50
    font = ImageFont.truetype(font_path, font_size)

    text = name
    text_position = (500, 520)  # Adjust to fit the specific space
    text_color = (0, 0, 0)  # Black color for text

    # Insert the recipient's name into the template
    draw.text(text_position, text, fill=text_color, font=font)

    # Save the modified certificate
    image.save(output_path)


if __name__ == "__main__":
    app.run(debug=True)
