from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

# Certificate generation route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        output_path = "generated_certificate.pdf"

        # Generate the certificate
        generate_certificate(name, output_path)

        return send_file(
            output_path, as_attachment=True, download_name="certificate.pdf"
        )
    return render_template("index.html")


def generate_certificate(name, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Customize certificate layout
    c.setFont("Helvetica-Bold", 36)
    c.drawString(200, 450, f"Certificate of Achievement")
    
    c.setFont("Helvetica", 24)
    c.drawString(200, 400, f"Awarded to {name}")
    
    c.setFont("Helvetica-Oblique", 14)
    c.drawString(200, 350, "For outstanding performance.")
    c.drawString(200, 300, "Congratulations!")
    
    c.save()


if __name__ == "__main__":
    app.run(debug=True)
