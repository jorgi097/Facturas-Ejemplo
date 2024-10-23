from PyPDF2 import PdfReader
import re
import os
import time
import tkinter as tk
from tkinter import filedialog

# DEFINE GLOBAL VARIABLES ----------------------------------------------------------------------
extension = ".pdf"

# DEFINE FUNCTIONS -----------------------------------------------------------------------------
def get_content(file): # GET PDF CONTENT
    reader = PdfReader(file)
    page = reader.pages[0]
    content = page.extract_text()
    content = content.lower()
    return content

def is_invoice(text): # GET FILE TYPE
    result = "uso cfdi" in text
    return result

def get_date(text): # GET (YEAR-MONTH-DATE)
    match_date = re.search(r'emisión:\d{5}\s*(\w+)-(\w+)-(\w+)', text)
    year = match_date.group(1)
    month = match_date.group(2)
    day = match_date.group(3)
    date = f"{year}-{month}-{day}"
    return date

def get_receptor_name(text): 
    match_receptor = re.search(r'nombre receptor:\s*(\w+)', text)
    receptor_name = match_receptor.group(1)
    return receptor_name

def get_receptor_rfc(text): 
    match_receptor_rfc = re.search(r'rfc receptor:\s*(\w+)', text)
    receptor_rfc = match_receptor_rfc.group(1)
    return receptor_rfc

def get_sender_name(text):
    match_sender_name = re.search(r'nombre emisor:\s*(.*)', text)
    sender_name = match_sender_name.group(1)
    return sender_name

def get_sender_rfc(text): 
    match_sender_rfc = re.search(r'rfc emisor:\s*(\w+)', text)
    sender_rfc = match_sender_rfc.group(1)
    return sender_rfc

def get_invoice(): # LIST FILES IN FOLDER
    dir = os.listdir()
    pdf_dir = [file for file in dir if file.endswith(extension)]
    invoice_dir = [file for file in pdf_dir if is_invoice(get_content(file))]
    return invoice_dir

def generate_unique_name(filename): # GENERATES UNIQUE NAME
    timestamp = int(time.time())
    base_name, extension = os.path.splitext(filename)
    unique_name = f"{base_name}-{timestamp}{extension}"
    return unique_name

def rename_unique(): # RENAME INVOICE WHIT UNIQUE NAME
    invoices = get_invoice()
    for invoice in invoices:
        unique_name = generate_unique_name(invoice)
        os.rename(invoice, unique_name)

def rename_invoice(rfc): # MAIN FUNCTION
    invoice_dir = get_invoice()
    rename_done = {}
    
    for invoice in invoice_dir:
        text = get_content(invoice)
        date = get_date(text)
        receptor_rfc = get_receptor_rfc(text)
        sender_rfc = get_sender_rfc(text)
        receptor_name = get_receptor_name(text) 
        sender_name = get_sender_name(text)
        is_receptor = receptor_rfc == rfc.lower()
        is_sender = sender_rfc == rfc.lower()

        if is_receptor and not is_sender:
            base_filename = f'Recibida {date} - {sender_name}'.upper()
        elif is_sender and not is_receptor: 
            base_filename = f'Emitiida {date} - {receptor_name}'.upper()
            
            # IF FIRST FILE
            if base_filename not in rename_done:
                os.rename(invoice, base_filename + extension)
                rename_done.update({base_filename:[0]})

            # IF NOT FIRST FILE
            elif base_filename in rename_done:
                next_num = rename_done[base_filename][-1] + 1
                next_name = f'{base_filename} - ({next_num}){extension}'
                os.rename(invoice, next_name)
                rename_done[base_filename].append(next_num)


# MAIN EXECUTION ----------------------------------------------------------------------------
os.system("cls") # CLEAR SCREEN

def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    if folder_path:
        label_path.config(text=f"Ruta seleccionada: {folder_path}")

def save_rfc():
    global rfc
    rfc = input_rfc.get()
    if rfc:
        label_rfc.config(text=f"RFC: {rfc}")


# MAIN TKINTER
root = tk.Tk()
root.title("Seleccionar Carpeta")
root.geometry('600x400')

# INPUT PATH
dir_select_btn = tk.Button(root, text="Seleccionar Carpeta", command=select_folder)
dir_select_btn.pack(pady=20)

label_path = tk.Label(root, text="Ruta seleccionada: ")
label_path.pack()

# INPUT RFC
label_rfc = tk.Label(root, text="Ingrese el RFC de quien recibe:")
label_rfc.pack(pady=10)

input_rfc = tk.Entry(root, width=30)
input_rfc.pack()

save_rfc_btn = tk.Button(root, text="Seleccionar RFC", command=save_rfc)
save_rfc_btn.pack(pady=20)

root.mainloop()


# rename_unique() # AVOID REPEATED NAMES
# rename_invoice(rfc)pg