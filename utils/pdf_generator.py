from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(filename, text, medicines, details):

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>AI Prescription Analyzer Report</b>", styles["Heading1"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>OCR Text</b>", styles["Heading2"]))
    story.append(Paragraph(text.replace("\n", "<br/>"), styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Medicines</b>", styles["Heading2"]))

    for medicine in medicines:

        story.append(Paragraph(f"<b>Name :</b> {medicine['name']}", styles["Normal"]))
        story.append(Paragraph(f"<b>Uses :</b> {medicine['uses']}", styles["Normal"]))
        story.append(Paragraph(f"<b>Price :</b> {medicine['price']}", styles["Normal"]))
        story.append(Paragraph(f"<b>Side Effects :</b> {medicine['side_effects']}", styles["Normal"]))
        story.append(Paragraph(f"<b>Alternative :</b> {medicine['alternative']}", styles["Normal"]))
        story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Dose</b>", styles["Heading2"]))
    story.append(Paragraph(", ".join(details["dose"]), styles["Normal"]))

    story.append(Paragraph("<b>Timing</b>", styles["Heading2"]))
    story.append(Paragraph(", ".join(details["timing"]), styles["Normal"]))

    story.append(Paragraph("<b>Duration</b>", styles["Heading2"]))
    story.append(Paragraph(", ".join(details["duration"]), styles["Normal"]))

    pdf.build(story)