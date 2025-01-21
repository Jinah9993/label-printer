import pandas as pd
from reportlab.pdfgen import canvas
from tkinter import Tk, filedialog, Label, Button, Canvas as TkCanvas, Frame
from tkinter.messagebox import showinfo
from pdf2image import convert_from_bytes
from PIL import Image, ImageTk
import io
import csv
import os


def adjust_text(text, max_width, pdf, font="Helvetica-Bold", initial_font_size=24):
    font_size = initial_font_size
    pdf.setFont(font, font_size)
    while pdf.stringWidth(text, font, font_size) > max_width and font_size > 10:
        font_size -= 1
        pdf.setFont(font, font_size)

    if font_size > 10:
        return [text], font_size  

    
    words = text.split(" ")
    lines = []
    current_line = words[0]
    for word in words[1:]:
        if pdf.stringWidth(current_line + " " + word, font, font_size) < max_width:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines, font_size


def create_preview(csv_file):
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        showinfo("Error", f"Error reading CSV file: {e}")
        return None

    
    df.columns = df.columns.str.strip()

    # required columns
    required_columns = ['SKU', 'Group', 'Album', 'Item', 'Member']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        showinfo("Error", f"The following required columns are missing in the CSV: {', '.join(missing_columns)}")
        return None

    
    pdf_buffer = io.BytesIO()
    pdf = canvas.Canvas(pdf_buffer, pagesize=(288, 432)) 
    pdf.setTitle("SKU Labels")

    max_width = 250  

    for i, row in enumerate(df.iterrows()):
        sku = row[1]['SKU']
        group = row[1]['Group']
        album = row[1]['Album']
        item = row[1]['Item']
        member = row[1]['Member']

        # separate the alphabetic and numeric parts of the SKU
        alphabetic_part = ''.join([char for char in sku if char.isalpha()])
        numeric_part = ''.join([char for char in sku if char.isdigit()])

        # font settings
        sku_font_size = 35
        sku_number_font_size = 45
        font_size = 24

        # label position
        if i % 2 == 0:  # top label
            pdf.saveState()
            pdf.translate(144, 440)
            pdf.setFont("Helvetica-Bold", sku_font_size) 
            pdf.drawCentredString(0, -40, alphabetic_part)  # sku - alphabet
            pdf.setFont("Helvetica-Bold", sku_number_font_size) 
            pdf.drawCentredString(0, -100, numeric_part)  # sku - number

            # group and album
            group_album_text = f"{group} {album}"
            lines, adjusted_font_size = adjust_text(group_album_text, max_width, pdf, font="Helvetica-Bold", initial_font_size=font_size)
            pdf.setFont("Helvetica-Bold", adjusted_font_size)
            y_position = -160
            for line in lines:
                pdf.drawCentredString(0, y_position, line)
                y_position -= adjusted_font_size + 4

            # item and member
            item_member_text = f"{item} {member}"
            lines, adjusted_font_size = adjust_text(item_member_text, max_width, pdf, font="Helvetica-Bold", initial_font_size=font_size)
            pdf.setFont("Helvetica-Bold", adjusted_font_size)
            for line in lines:
                pdf.drawCentredString(0, y_position, line)
                y_position -= adjusted_font_size + 4

            pdf.restoreState()
        else:  # bottom label
            pdf.saveState()
            pdf.translate(144, 220)
            pdf.setFont("Helvetica-Bold", sku_font_size)
            pdf.drawCentredString(0, -40, alphabetic_part) # sku - alphabet
            pdf.setFont("Helvetica-Bold", sku_number_font_size)
            pdf.drawCentredString(0, -100, numeric_part) # sku - number

            # group and album
            group_album_text = f"{group} {album}"
            lines, adjusted_font_size = adjust_text(group_album_text, max_width, pdf, font="Helvetica-Bold", initial_font_size=font_size)
            pdf.setFont("Helvetica-Bold", adjusted_font_size)
            y_position = -160
            for line in lines:
                pdf.drawCentredString(0, y_position, line)
                y_position -= adjusted_font_size + 4

            # item and member
            item_member_text = f"{item} {member}"
            lines, adjusted_font_size = adjust_text(item_member_text, max_width, pdf, font="Helvetica-Bold", initial_font_size=font_size)
            pdf.setFont("Helvetica-Bold", adjusted_font_size)
            for line in lines:
                pdf.drawCentredString(0, y_position, line)
                y_position -= adjusted_font_size + 4

            pdf.restoreState()
            pdf.showPage()  # new page after two labels

        # divider line
        if i % 2 == 0:
            pdf.setStrokeColorRGB(0, 0, 0) 
            pdf.setLineWidth(0.5)
            pdf.line(0, 216, 288, 216)  # horizontal line

    pdf.save()
    pdf_buffer.seek(0)
    return pdf_buffer


def show_preview(pdf_buffer):
    try:
        # pdf buffer to image
        images = convert_from_bytes(pdf_buffer.getvalue())
        first_page = images[0]  # display the first page
        first_page.thumbnail((400, 600))  

        # Tkinter-compatible image
        photo = ImageTk.PhotoImage(first_page)

        preview_frame = Frame(root, width=400, height=600, bg="white", highlightbackground="black", highlightthickness=1)
        preview_frame.grid(row=0, column=1, padx=20, pady=10, rowspan=10)

        # display
        preview_canvas = TkCanvas(preview_frame, width=400, height=600, bg="white")
        preview_canvas.image = photo 
        preview_canvas.create_image(0, 0, anchor="nw", image=photo)
        preview_canvas.pack()

    except Exception as e:
        showinfo("Error", f"Error displaying PDF preview: {e}")


def auto_preview():
    global uploaded_csv  
    uploaded_csv = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if not uploaded_csv:
        showinfo("Error", "No CSV file selected.")
        return

    pdf_buffer = create_preview(uploaded_csv)
    if pdf_buffer:
        show_preview(pdf_buffer)


def save_pdf():
    if not uploaded_csv:
        showinfo("Error", "No CSV file uploaded.")
        return

    output_file = filedialog.asksaveasfilename(
        title="Save PDF As",
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
    )
    if not output_file:
        showinfo("Error", "No save location specified.")
        return

    pdf_buffer = create_preview(uploaded_csv)
    if pdf_buffer:
        with open(output_file, "wb") as f:
            f.write(pdf_buffer.getvalue())
        showinfo("Success", f"PDF saved as {output_file}")


def download_sample_csv():
    sample_data = [
        ["LONGID012345", "SuperLongGroupNameThatExceedsLimit", "Extended Album Name Beyond Width", "Extremely Long Item Name", "VeryVerboseMemberName"],
        ["SHORT001", "Short", "Short Album", "Item", "Member"],
        ["REGID123456", "RegularGroup", "RegularAlbum", "RegularItem", "RegularMember"],
        ["EDGECA789012", "EdgeCaseGroup", "EdgeAlbum", "EdgeItem", "EdgeMember"],
        ["MIXID654321", "MixGroup", "LongAlbumName", "ShortItem", "MixedLengthMember"],
    ]
    headers = ["SKU", "Group", "Album", "Item", "Member"]

    try:
        downloads = os.path.join(os.path.expanduser("~"), 'Downloads')
        output_file = os.path.join(downloads, "sample.csv")
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            writer.writerows(sample_data)
        showinfo("Success", f"Sample CSV saved to Downloads as sample.csv")
    except Exception as e:
        showinfo("Error", f"Failed to save sample CSV: {e}")


root = Tk()
root.title("SKU Label Generator")
root.geometry("780x630")
root.configure(bg="#f9f9f9")

uploaded_csv = None  


welcome_label = Label(root, text="SKU Label Generator", font=("Helvetica", 20, "bold"), fg="#333", bg="#f9f9f9")
welcome_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")


button_frame = Frame(root, bg="#f9f9f9")
button_frame.grid(row=1, column=0, padx=20, pady=10, sticky="w")

upload_button = Button(button_frame, text="Upload CSV and Preview", command=auto_preview, font=("Helvetica", 14), bg="#4CAF50", fg="white", relief="flat", padx=10, pady=5)
upload_button.grid(row=0, column=0, padx=5, pady=5)

save_button = Button(button_frame, text="Save Labels", command=save_pdf, font=("Helvetica", 14), bg="#2196F3", fg="white", relief="flat", padx=10, pady=5)
save_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

sample_button = Button(button_frame, text="Download Sample CSV", command=download_sample_csv, font=("Helvetica", 14), bg="#FF9800", fg="white", relief="flat", padx=10, pady=5)
sample_button.grid(row=2, column=0, padx=5, pady=5, sticky="w")

root.mainloop()
