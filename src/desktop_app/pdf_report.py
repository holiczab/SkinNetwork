import fpdf
from datetime import date
import cv2


def generate_pdf(image_save_path, skin_image_path, image_class, confidence, lang='en'):

    pdf = fpdf.FPDF()
    pdf.add_font('OpenSans', '', 'OpenSans-Regular.ttf', uni=True)
    pdf_title = "Pdf report"
    pdf.set_title(pdf_title)
    lang_index = {'en':0, 'hu':1}[lang]

    disease_category_dict = {
        0: ["melanocytic nevi (nv)", "Melanocytic nevus"],
        1: ["melanoma (mel)","Melanóma"],
        2: ["benign keratosis-like lesions (bkl)","Jóindulatú eredetű keratózis jellegű elváltozás"],
        3: ["basal cell carcinoma (bcc)","Bazális sejtkarcinóma"],
        4: ["actinic keratoses (akiec)","Aktinikus keratózis"],
        5: ["vascular lesions (vasc)","Érkárosodás"],
        6: ["dermatofibroma (df)", "Dermatofibroma"]
    }

    m = 16
    pdf.add_page()
    pdf.set_margins(m,m)
    # bottom margin
    pdf.set_auto_page_break(True, margin=1)

    # default page A4
    page_width = 210
    page_height = 297
    real_page_width = page_width - 2*m

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
    pdf.set_font("OpenSans", size=12)
    pdf.set_font_size(24)
    pdf.set_text_color(0, 0, 0)
    pdf.set_x(m)
    pdf.set_y(23)
    pdf.cell(page_width-2*m, 15, "Report", ln=1, align='C')

    # Image
    image = cv2.imread(skin_image_path)
    image_height, image_width, channel = image.shape
    image_ratio = image_width/image_height
    new_image_height = 100
    new_image_width = new_image_height * image_ratio
    pdf.image(skin_image_path, page_width/2 - new_image_width/2, 40, new_image_width, new_image_height)

    # Predictions
    pdf.set_font_size(12)
    pdf.set_y(50 + new_image_height)

    result_text_lang = ["Result", "Eredmény"][lang_index]
    confidence_text_lang = ["Confidence", "Bizonyosság"][lang_index]

    image_class_text = disease_category_dict[image_class][lang_index]
    result_text = result_text_lang + ": {}".format(image_class_text)
    confidence_text = confidence_text_lang + ": {}%".format(confidence)

    pdf.multi_cell(real_page_width, 15, result_text)
    pdf.multi_cell(real_page_width, 15, confidence_text)

    ## Descriptions
    # description_text = "Short description of predicted skin condition."
    # pdf.multi_cell(100, 15, description_text)

    # Date
    pdf.set_font_size(12)
    pdf.set_x(m)
    pdf.set_y(footer_y - 35)
    today = date.today().strftime("%Y. %m. %d.")
    pdf.cell(100,15, today, ln=1)
    

    # Disclaimer
    pdf.set_y(footer_y - 15)
    disclaimer_text = ["This tool does not provide medical advice, it is intended for informational purposes only. It is not a substitute for professional medical advice, diagnosis or treatment. Always seek the guidance of your doctor or other qualified health professional with any questions you may have regarding your health or a medical condition.",
    "Ez az eszköz nem nyújt orvosi tanácsot, csak tájékoztató jellegű. Nem helyettesíti a professzionális orvosi tanácsot, diagnózist vagy kezelést. Mindig kérje orvosa vagy más képzett egészségügyi szakember útmutatását, ha bármilyen kérdése van az egészségével vagy egészségügyi állapotával kapcsolatban."]
    pdf.set_font_size(10)
    pdf.multi_cell(real_page_width, 5, disclaimer_text[lang_index])

    # Save pdf
    pdf.output(name=image_save_path)

if __name__ == "__main__":
    generate_pdf("skin_condition_report.pdf", "skin.png", 2, 60, lang='hu')
