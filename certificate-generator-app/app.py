from flask import Flask, render_template, request, send_file
from PIL import Image
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

# Certificate generation route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        template_path = r"certificate-generator-app\Korina Villanueva.png"  # Template image
        output_path = "generated_certs.pdf"  # Output PDF

        # Generate the certificate as a PDF
        generate_certificate_pdf(template_path, name, output_path)

        return send_file(
            output_path, as_attachment=True, download_name="certificate.pdf"
        )
    return render_template("index.html")


def generate_certificate_pdf(template_path, name, output_path):
    # Check if the template file exists
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found at {template_path}")

    # Load the certificate template
    template_image = Image.open(template_path)
    width, height = template_image.size

    # Save the template image as a background for the PDF
    temp_background = "temp_background.png"
    template_image.save(temp_background)

    # Create a new PDF with the template as the background
    c = canvas.Canvas(output_path, pagesize=(width, height))
    c.drawImage(temp_background, 0, 0, width, height)

    # Add the recipient's name
    c.setFont("Helvetica-Bold", 50)  # Adjust font style and size as needed
    name_x, name_y = 500, 520  # Coordinates for the name
    c.drawString(name_x, name_y, name)

    # Save the PDF
    c.save()

    # Remove the temporary background image
    os.remove(temp_background)


if __name__ == "__main__":
    app.run(debug=True)
