import fpdf
from datetime import date
import cv2


def generate_pdf(image_save_path, skin_image_path, image_class, confidence, lang='en'):

    pdf = fpdf.FPDF()
    pdf_title = "Pdf report"
    pdf.set_title(pdf_title)

    m = 16
    pdf.add_page()
    pdf.set_margins(m,m)
    # bottom margin
    pdf.set_auto_page_break(True, margin=1)

    # default page A4
    page_width = 210
    page_height = 297

    # darkblue
    pdf.set_line_width(1.5)
    pdf.set_draw_color(52, 114, 207)
    pdf.line(m, 17, page_width - m, 17)

    # lightblue
    footer_line_width = 40
    pdf.set_line_width(footer_line_width)
    pdf.set_draw_color(124, 170, 238)
    footer_y = page_height - footer_line_width//2
    pdf.line(0, footer_y, page_width, footer_y)

    # Title
    pdf.set_font("Times", size=12)
    pdf.set_font_size(24)
    pdf.set_text_color(0, 0, 0)
    pdf.set_x(m)
    pdf.set_y(23)
    pdf.cell(page_width-2*m, 15, "Report", ln=1, align='C')

    # Image
    image = cv2.imread(skin_image_path)
    image_height, image_width, channel = image.shape
    image_ratio = image_width/image_height
    new_image_height = 40
    new_image_width = new_image_height * image_ratio
    pdf.image(skin_image_path, page_width/2 - new_image_width/2, 40, new_image_width, new_image_height)

    # Predictions
    pdf.set_font_size(14)
    pdf.set_y(40+new_image_height)

    result_text = "Result: {}".format(image_class)
    confidence_text = "Confidence: {}%".format(confidence)
    description_text = "Short description of predicted skin condition."

    pdf.multi_cell(100, 15, result_text)
    pdf.multi_cell(100, 15, confidence_text)
    pdf.multi_cell(100, 15, description_text)

    # Date
    pdf.set_font_size(12)
    pdf.set_x(m)
    pdf.set_y(footer_y - 35)
    today = date.today().strftime("%Y. %m. %d.")
    pdf.cell(100,15, today, ln=1)
    

    # Disclaimer
    pdf.set_y(footer_y - 15)
    disclaimer_text = "This tool does not provide medical advice, it is intended for informational purposes only. It is not a substitute for professional medical advice, diagnosis or treatment. Always seek the guidance of your doctor or other qualified health professional with any questions you may have regarding your health or a medical condition."
    pdf.set_font_size(10)
    pdf.multi_cell(page_width-2*m, 5, disclaimer_text)

    # Save pdf
    pdf.output(name=image_save_path)

if __name__ == "__main__":
    generate_pdf("skin_condition_report.pdf", "skin.png", 2, 60, lang='en')
