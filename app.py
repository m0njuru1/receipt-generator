from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
from datetime import datetime
import os

app = Flask(__name__)

def create_pdf(course, batch, name, amount, method, date):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "MONEY RECEIPT")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Date: {date}")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(400, height - 50, "SCORE GAIN PTE")
    c.setFont("Helvetica", 9)
    c.drawString(400, height - 65, "Address: 4th Floor, Dutch Bangla Bank Building,")
    c.drawString(400, height - 75, "Bata Signal, New Elephant Rd, Dhaka 1205")
    c.drawString(400, height - 85, "Email: info@scoregain-pte.com")
    c.drawString(400, height - 95, "Phone: 01309008508")

    y = height - 140
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Course:")
    c.setFont("Helvetica", 12)
    c.drawString(120, y, course)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y, "Batch No:")
    c.setFont("Helvetica", 12)
    c.drawString(420, y, batch)

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Received With Thanks From:")
    c.setFont("Helvetica", 12)
    c.drawString(240, y, name)

    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Received Amount:")
    c.setFont("Helvetica", 12)
    c.drawString(180, y, f"{amount}/-")

    y -= 50
    c.setFillColorRGB(0.9, 0.8, 0.7)
    c.rect(0, y, width, 30, fill=True, stroke=False)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y + 8, f"Payment Method: {method}")
    c.drawRightString(width - 50, y + 8, f"Total: {amount}/-")

    c.drawRightString(width - 150, 80, "Authorized Signature")
    c.setFont("Helvetica-Bold", 26)
    c.setFillColorRGB(1, 0, 0)
    c.drawString(220, 300, "PAID")

    c.save()
    buffer.seek(0)
    return buffer

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        course = request.form['course']
        batch = request.form['batch']
        name = request.form['name']
        amount = request.form['amount']
        method = request.form['method']
        date = request.form['date'] or datetime.today().strftime('%d/%m/%Y')
        pdf = create_pdf(course, batch, name, amount, method, date)
        return send_file(pdf, as_attachment=True, download_name=f"receipt_{name.replace(' ', '_')}.pdf")
    return render_template('form.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
