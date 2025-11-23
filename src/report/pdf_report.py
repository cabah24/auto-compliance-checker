"""
Generador de PDF simple usando ReportLab.
"""
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime




def generate_simple_pdf(results: dict, out_file: str = 'report.pdf'):
    c = canvas.Canvas(out_file, pagesize=A4)
    width, height = A4
    c.setFont('Helvetica-Bold', 14)
    c.drawString(40, height - 40, 'Auto-Compliance Windows - Informe')
    c.setFont('Helvetica', 10)
    c.drawString(40, height - 60, f'Generado: {datetime.utcnow().isoformat()}Z')


    y = height - 100
    for section, checks in results.items():
        c.setFont('Helvetica-Bold', 12)
        c.drawString(40, y, section)
        y -= 20
        c.setFont('Helvetica', 9)
        for chk in checks:
            text = f"- {chk.get('check')} [{chk.get('status')}] - {chk.get('severity')}"
            c.drawString(50, y, text[:90])
            y -= 14
            if y < 80:
                c.showPage()
                y = height - 40
                c.save()