from flask import Flask, render_template, request, send_file, session
import os
import json
import pytesseract
from PIL import Image
from rapidfuzz import process

from utils.prescription_parser import extract_prescription_details
from utils.pdf_generator import generate_pdf


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Tesseract OCR Path
import platform

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = Flask(__name__)

app.secret_key = "ai_prescription_analyzer_2026"

# Upload Folder
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

DATABASE_FILE = "database/medicines.json"


# ===========================
# HOME
# ===========================

@app.route("/")
def home():
    return render_template("index.html")


# ===========================
# ABOUT
# ===========================

@app.route("/about")
def about():
    return render_template("about.html")


# ===========================
# FEATURES
# ===========================

@app.route("/features")
def features():
    return render_template("features.html")


# ===========================
# CONTACT
# ===========================

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        print("\n========== NEW CONTACT MESSAGE ==========")
        print("Name    :", name)
        print("Email   :", email)
        print("Subject :", subject)
        print("Message :", message)
        print("=========================================\n")

        # Save message to file
        with open("messages.txt", "a", encoding="utf-8") as file:

            file.write(f"Name : {name}\n")
            file.write(f"Email : {email}\n")
            file.write(f"Subject : {subject}\n")
            file.write(f"Message : {message}\n")
            file.write("-" * 50 + "\n")

        # ==========================
        # SEND EMAIL
        # ==========================

        sender_email = "omkarghorband24@gmail.com"
        receiver_email = "omkarghorband24@gmail.com"
        app_password = "whyozorszohysqga"

        try:

            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            msg = MIMEMultipart()

            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = f"New Contact Form - {subject}"

            body = f"""
New Contact Form Message

Name : {name}

Email : {email}

Subject : {subject}

Message :

{message}
"""

            msg.attach(MIMEText(body, "plain"))

            print("Connecting to Gmail...")

            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)

            print("Connected!")

            server.starttls()
            print("TLS Started!")

            server.login(sender_email, app_password)
            print("Logged In!")

            server.send_message(msg)
            print("Mail Sent!")

            server.quit()

            print("✅ Email Sent Successfully!")

        except Exception as e:

            print("❌ Email Error :", e)

        return render_template(
            "contact.html",
            success="✅ Your message has been sent successfully!"
        )

    return render_template("contact.html")

@app.route("/upload", methods=["POST"])
def upload():

    print("========== UPLOAD FUNCTION CALLED ==========")

    image = request.files["image"]

    if image.filename == "":
        return "No Image Selected"

    path = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
    image.save(path)

    print("Image Saved Successfully!")

    # OCR
    text = pytesseract.image_to_string(Image.open(path))
    details = extract_prescription_details(text)

    # Load JSON Database
    with open(DATABASE_FILE, "r") as file:
        medicines = json.load(file)

    found_medicines = []

    ocr_lines = text.splitlines()
    medicine_names = [medicine["name"] for medicine in medicines]

    for line in ocr_lines:

        line = line.strip()

        if not line:
            continue

        match = process.extractOne(line, medicine_names)

        if match:

            matched_name = match[0]
            score = match[1]

            if score >= 70:

                for medicine in medicines:

                    if medicine["name"] == matched_name:

                        if medicine not in found_medicines:
                            found_medicines.append(medicine)

    print("========== OCR TEXT ==========")
    print(text)
    print("==============================")

    session["ocr_text"] = text
    session["details"] = details
    session["medicines"] = found_medicines

    return render_template(
        "result.html",
        image=image.filename,
        text=text,
        medicines=found_medicines,
        details=details
    )


# ===========================
# MANUAL SEARCH
# ===========================

@app.route("/search", methods=["POST"])
def search():

    medicine_name = request.form["medicine"]

    with open(DATABASE_FILE, "r") as file:
        medicines = json.load(file)

    medicine_names = [medicine["name"] for medicine in medicines]

    match = process.extractOne(medicine_name, medicine_names)

    if match and match[1] >= 70:

        for medicine in medicines:

            if medicine["name"] == match[0]:

                return render_template(
                    "result.html",
                    image="",
                    text="Manual Search",
                    medicines=[medicine],
                    details={
                        "dose": [],
                        "timing": [],
                        "duration": []
                    }
                )

    return render_template(
        "result.html",
        image="",
        text="Medicine Not Found",
        medicines=[],
        details={
            "dose": [],
            "timing": [],
            "duration": []
        }
    )


# ===========================
# PDF DOWNLOAD
# ===========================

@app.route("/download")
def download():

    filename = "Prescription_Report.pdf"

    text = session.get("ocr_text", "")
    medicines = session.get("medicines", [])

    details = session.get(
        "details",
        {
            "dose": [],
            "timing": [],
            "duration": []
        }
    )

    generate_pdf(
        filename,
        text,
        medicines,
        details
    )

    return send_file(filename, as_attachment=True)


# ===========================
# RUN APP
# ===========================

if __name__ == "__main__":
    app.run(debug=True)