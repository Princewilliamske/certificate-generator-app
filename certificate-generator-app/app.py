from flask import Flask, render_template, request, send_file, url_for
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
import os

app = Flask(__name__)

# Directory to store generated certificates
CERTIFICATES_DIR = "generated_certificates"

# Ensure the directory exists
if not os.path.exists(CERTIFICATES_DIR):
    os.makedirs(CERTIFICATES_DIR)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get recipient name from form
            name = request.form["name"]

            # Paths and file details
            template_path = r"certificate-generator-app/template_certificate.png"  # Template image
            output_file = os.path.join(CERTIFICATES_DIR, f"{name}_certificate.pdf")  # Save certificate on the server

            # Generate and save the certificate
            generate_certificate_pdf(template_path, name, output_file)

            # Provide a link to download the certificate
            download_link = url_for("download_certificate", filename=f"{name}_certificate.pdf")

            return render_template("index.html", success=True, download_link=download_link)

        except Exception as e:
            # If an error occurs, return to the form with error message
            return render_template("index.html", error=str(e))

    return render_template("index.html")


@app.route("/download/<filename>")
def download_certificate(filename):
    """Route to download a saved certificate."""
    file_path = os.path.join(CERTIFICATES_DIR, filename)
    if not os.path.exists(file_path):
        return "File not found!", 404

    return send_file(
        file_path,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf",
    )


def generate_certificate_pdf(template_path, name, output_path):
    """Generate and save the certificate as a PDF on the server."""
    # Check if the template file exists
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found at {template_path}")

    # Load the "Good Vibes" font
    font_path = "certificate-generator-app/templates/goodvibes.ttf"  # Update with the actual path to the font file
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font not found at {font_path}")
    pdfmetrics.registerFont(TTFont("GoodVibes", font_path))

    # Load the certificate template
    template_image = Image.open(template_path)
    template_width, template_height = template_image.size

    # Resize the image proportionally to fit within A4 size
    a4_width, a4_height = A4
    aspect_ratio = min(a4_width / template_width, a4_height / template_height)
    resized_width = int(template_width * aspect_ratio)
    resized_height = int(template_height * aspect_ratio)
    template_image = template_image.resize((resized_width, resized_height),  Image.Resampling.LANCZOS)

    # Save the resized template image as a temporary background
    temp_background = "temp_background.png"
    template_image.save(temp_background)

    # Create a new PDF with A4 page size
    c = canvas.Canvas(output_path, pagesize=A4)
    x_offset = (a4_width - resized_width) / 2  # Center the image horizontally
    y_offset = (a4_height - resized_height) / 2  # Center the image vertically
    c.drawImage(temp_background, x_offset, y_offset, resized_width, resized_height)

    # Add the recipient's name using the "Good Vibes" font
    c.setFont("GoodVibes", 39.5)  # Adjust font size for A4
    name_x = a4_width / 2  # Center the name horizontally
    name_y = y_offset + resized_height / 1.8999  # Adjust vertical position within the image
    c.drawCentredString(name_x, name_y, name)

    # Save the PDF
    c.save()

    # Remove the temporary background image
    os.remove(temp_background)


if __name__ == "__main__":
    app.run(debug=True)
