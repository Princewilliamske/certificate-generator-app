# **📜 Certificate Generator**
## A simple web application that generates, previews, and downloads personalized certificates in PDF format using Flask and ReportLab.


## 🚀 Features

✅ Generate certificates with custom recipient names

✅ Preview the generated certificate before downloading

✅ Download certificates in high-quality PDF format

✅ Uses a predefined certificate template (template_certificate.png)

## 🛠️ Technologies Used

	Technology		Usage
	Flask			Web framework (backend)
	HTML, CSS		Frontend design
	ReportLab		PDF generation
	Pillow (PIL)		Image processing
 
## 📂 Project Structure

		certificate-generator/
		│── templates/
		│   ├── index.html          	# Main frontend page
		│── generated_certificates/ 	# Folder for storing generated PDFs
		│── app.py                  	# Flask application logic
		│── template_certificate.png 	# Certificate background template
		│── goodvibes.ttf            	# Custom font for certificate
		│── requirements.txt         	# Dependencies list
		│── README.md                	# Project documentation
  
## 🔧 Installation & Setup

1️⃣ Clone the Repository

	git clone https://github.com/your-username/certificate-generator.git
	cd certificate-generator
 
2️⃣ Install Dependencies

Make sure you have Python installed, then run:

	pip install -r requirements.txt
 
3️⃣ Run the Application

	python app.py
	The application will start on http://127.0.0.1:5000/

## 🖼️ How It Works

1️⃣ Open the app in a browser

2️⃣ Enter the recipient’s name in the input field

3️⃣ Click "Generate Certificate"

4️⃣ Preview the generated certificate

5️⃣ Click "Download Certificate" to save it as a PDF

## 📜 Dependencies
Ensure you have the following installed before running the app:

Flask → pip install flask

ReportLab → pip install reportlab

Pillow (PIL) → pip install pillow

## 🏆 Example Certificate
The generated certificates will have a high-quality background image and the recipient’s name in a stylish font.

## ⚡ License
This project is open-source and free to use.

## 📧 Contact
For any questions or contributions, feel free to reach out via GitHub issues.
