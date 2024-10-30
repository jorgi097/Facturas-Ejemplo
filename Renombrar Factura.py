from PyPDF2 import PdfReader
import re
import os
import time
import tkinter as tk
from tkinter import filedialog

# DEFINE GLOBAL VARIABLES ----------------------------------------------------------------------
extension = ".pdf"

# DEFINE FUNCTIONS -----------------------------------------------------------------------------

def validate_rfc(rfc):
    is_valid_rfc = re.search(r"^[a-zñ&]{3,4}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])[a-z0-9]{2}[0-9a]$", rfc)
    return is_valid_rfc

def get_invoice(path): # LIST FILES IN FOLDER
    dir = os.listdir(path)
    pdf_dir = [file for file in dir if file.endswith(extension)]
    invoice_dir = []
    for file in pdf_dir:
        try:
            if is_invoice(get_content(path, file)):
                invoice_dir.append(file)
        except TypeError:
            print(f"El archivo {file} no se pudo leer correctamente")
    return invoice_dir

def get_date(text): # GET (YEAR-MONTH-DATE)
    match_date = re.search(r'emisión:\s*\d{5}\s*(\w+)-(\w+)-(\w+)', text)
    year = match_date.group(1)
    month = match_date.group(2)
    day = match_date.group(3)
    date = f"{year}-{month}-{day}"
    return date

def get_receptor_name(text): 
    match_receptor = re.search(r'nombre receptor:\s*([^\n]+)', text)
    receptor_name = match_receptor.group(1)
    return receptor_name

def get_receptor_rfc(text): 
    match_receptor_rfc = re.search(r'rfc receptor:\s*(\w+)', text)
    receptor_rfc = match_receptor_rfc.group(1)
    return receptor_rfc

def get_sender_name(text):
    match_sender_name = re.search(r'nombre emisor:\s*([^\n]+)', text)
    sender_name = match_sender_name.group(1)
    return sender_name

def get_sender_rfc(text): 
    match_sender_rfc = re.search(r'rfc emisor:\s*(\w+)', text)
    sender_rfc = match_sender_rfc.group(1)
    return sender_rfc

def is_invoice(text): # GET FILE TYPE
    result = "uso cfdi" in text
    return result

def get_content(path, file): # GET PDF CONTENT
    try:
        reader = PdfReader(path + file)
        page = reader.pages[0]
        content = page.extract_text()
        content = content.lower()
        return content
    except:
        pass
        
def generate_unique_name(filename): # GENERATES UNIQUE NAME
    timestamp = int(time.time())
    base_name, extension = os.path.splitext(filename)
    unique_name = f"{base_name}-{timestamp}{extension}"
    return unique_name

def rename_unique(path): # RENAME INVOICE WHIT UNIQUE NAME
    invoices = get_invoice(path)
    for invoice in invoices:
        unique_name = generate_unique_name(invoice)
        os.rename(path + invoice, path + unique_name)

def rename_invoice(rfc, path): # MAIN FUNCTION
    invoice_dir = get_invoice(path)
    rename_done = {}
    
    for invoice in invoice_dir:
        text = get_content(path, invoice)
        date = get_date(text)
        receptor_rfc = get_receptor_rfc(text)
        sender_rfc = get_sender_rfc(text)
        receptor_name = get_receptor_name(text) 
        sender_name = get_sender_name(text)
        is_receptor = receptor_rfc == rfc.lower()
        is_sender = sender_rfc == rfc.lower()

        if is_receptor:
            base_filename = f'Recibida {date} - {sender_name}'.upper()
        elif is_sender: 
            base_filename = f'Emitida {date} - {receptor_name}'.upper()
            
        # IF FIRST FILE
        if base_filename not in rename_done:
            os.rename(path + invoice, path + base_filename + extension)
            rename_done.update({base_filename:[0]})

        # IF NOT FIRST FILE
        elif base_filename in rename_done:
            next_num = rename_done[base_filename][-1] + 1
            next_name = f'{base_filename} - ({next_num}){extension}'
            os.rename(path + invoice, path + next_name)
            rename_done[base_filename].append(next_num)


# MAIN EXECUTION ----------------------------------------------------------------------------
os.system("cls") # CLEAR SCREEN

def select_folder():
    global selected_path
    selected_path = filedialog.askdirectory()
    selected_path = selected_path + "\\"
    if selected_path:
        label_path.config(text=f"Ruta seleccionada: {selected_path}")

def save_rfc():
    global rfc
    rfc = input_rfc.get()
    rfc = rfc.lower().strip()
    is_valid_rfc = validate_rfc(rfc)
    if is_valid_rfc:
        label_rfc.config(text=f"RFC: {rfc.upper()}")
    else:
        label_rfc.config(text=f"{rfc.upper()} no es un RFC valido")
        
        
def rename_files():
    if 'rfc' in globals() and 'selected_path' in globals():
        if rfc and selected_path:
            rename_unique(selected_path), rename_invoice(rfc, selected_path)
        else:
            rename_error.config(text="Seleccione una carpeta e ingrese un RFC valido")
    else:
        rename_error.config(text="Seleccione una carpeta e ingrese un RFC valido")


# MAIN TKINTER
root = tk.Tk()
root.title("Seleccionar Carpeta")
root.geometry('600x400')

# INPUT PATH
label_path = tk.Label(root, text="Ruta seleccionada: ")
label_path.pack()

dir_select_btn = tk.Button(root, text="Seleccionar Carpeta", command=select_folder)
dir_select_btn.pack(pady=10)

# INPUT RFC
label_rfc = tk.Label(root, text="Ingrese el RFC de quien recibe:")
label_rfc.pack(pady=10)

input_rfc = tk.Entry(root, width=20)
input_rfc.pack()

save_rfc_btn = tk.Button(root, text="Seleccionar RFC", command=save_rfc)
save_rfc_btn.pack(pady=10)

# RENAME
rename_btn = tk.Button(root, text="Renombrar", command=rename_files)
rename_btn.pack(pady=20)

rename_error = tk.Label(root)
rename_error.pack()

root.mainloop()

