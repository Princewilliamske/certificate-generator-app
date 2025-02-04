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
    preview_link = None  # Variable to store preview link

    if request.method == "POST":
        try:
            # Get recipient name from form
            name = request.form["name"]

            # Paths and file details
            template_path = os.path.abspath(os.path.join(os.getcwd(), "template_certificate.png"))
            output_file = os.path.join(CERTIFICATES_DIR, f"{name}_certificate.pdf")  # Save certificate on the server

            # Generate and save the certificate
            generate_certificate_pdf(template_path, name, output_file)

            # Provide links for preview and download
            preview_link = url_for("view_certificate", filename=f"{name}_certificate.pdf")
            download_link = url_for("download_certificate", filename=f"{name}_certificate.pdf")

            return render_template("index.html", success=True, preview_link=preview_link, download_link=download_link)

        except Exception as e:
            # If an error occurs, return to the form with an error message
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


@app.route("/view/<filename>")
def view_certificate(filename):
    """Route to view a saved certificate."""
    file_path = os.path.join(CERTIFICATES_DIR, filename)
    if not os.path.exists(file_path):
        return "File not found!", 404

    return send_file(file_path, mimetype="application/pdf")


def generate_certificate_pdf(template_path, name, output_path):
    """Generate and save the certificate as a PDF on the server."""
    # Check if the template file exists
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found at {template_path}")

    # Load the "Good Vibes" font
    font_path = "templates/goodvibes.ttf"  # Update with the actual path to the font file
    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font not found at {font_path}")
    pdfmetrics.registerFont(TTFont("GoodVibes", font_path))

    # Load and ensure image is in high quality
    template_image = Image.open(template_path).convert("RGB")  
    template_width, template_height = template_image.size

    # Maintain high DPI for clarity
    dpi = 300
    a4_width, a4_height = A4
    aspect_ratio = min(a4_width / template_width, a4_height / template_height)
    resized_width = int(template_width * aspect_ratio * 1.2)  # Adjust for better clarity
    resized_height = int(template_height * aspect_ratio * 1.2)

    # Resize without quality loss
    template_image = template_image.resize((resized_width, resized_height), Image.Resampling.LANCZOS)

    # Save the resized image with high DPI
    temp_background = "temp_background.png"
    template_image.save(temp_background, dpi=(dpi, dpi))

    # Create high-quality PDF
    c = canvas.Canvas(output_path, pagesize=A4)
    c.setAuthor("Certificate Generator")
    c.setTitle("Award Certificate")

    # Center the image
    x_offset = (a4_width - resized_width) / 2
    y_offset = (a4_height - resized_height) / 2
    c.drawImage(temp_background, x_offset, y_offset, resized_width, resized_height, mask=None)

    # Add recipient's name
    c.setFont("GoodVibes", 39.5)
    name_x = a4_width / 2
    name_y = y_offset + resized_height / 1.8999
    c.drawCentredString(name_x, name_y, name)

    # Save and clean up
    c.save()
    os.remove(temp_background)
    
if __name__ == "__main__":
    app.run(debug=True)
