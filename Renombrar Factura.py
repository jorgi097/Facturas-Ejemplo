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

def rename_invoice(invoice_type, name): # MAIN FUNCTION
    type = invoice_type.lower()
    invoice_dir = get_invoice()
    rename_done = {}
    
    if type == "receive":
        for invoice in invoice_dir:
            text = get_content(invoice)
            date = get_date(text)
            rfcs = get_receptor_rfc(text)
            print(rfcs)
            rfcss = get_sender_rfc(text)
            print(rfcss)
            
            receptor = get_receptor_name(text) 
            sender = get_sender_name(text)
            is_right_person = receptor == name.lower()

            if(is_right_person):
                base_filename = f'Recibida {date} - {sender}'.upper()

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
    elif type == "send":
        print("OK")   


# MAIN EXECUTION ----------------------------------------------------------------------------
os.system("cls") # CLEAR SCREEN







options_list = ["Recibidas", "Emitidas"] 
    
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        label_path.config(text=f"Ruta seleccionada: {folder_path}")

def save_name():
    name = entry_name.get()
    if name:
        label_name.config(text=f"Nombre: {name}")
        
def option_selected(event):
    selected_option = option_var.get()
    label_selected.config(text=f"Opción seleccionada: {selected_option}")

root = tk.Tk()
root.title("Seleccionar Carpeta")
root.geometry('800x600')

# Crear y posicionar un botón para seleccionar la carpeta
dir_select_btn = tk.Button(root, text="Seleccionar Carpeta", command=select_folder)
dir_select_btn.pack(pady=20)

# Etiqueta para mostrar la ruta seleccionada
label_path = tk.Label(root, text="Ruta seleccionada: ")
label_path.pack()

# Etiqueta y entrada para ingresar el nombre a guardar
label_name = tk.Label(root, text="Ingrese el RFC de quien recibe:")
label_name.pack(pady=10)

input_name = tk.Entry(root, width=30)
input_name.pack()

# Botón para guardar el nombre ingresado
name_save_btn = tk.Button(root, text="Guardar Nombre", command=save_name)
name_save_btn.pack(pady=10)

# Variable para almacenar la opción seleccionada
invoice_type = tk.StringVar(root)
invoice_type.set(options_list[0])  # Opción por defecto

# Crear el OptionMenu
option_menu = tk.OptionMenu(root, option_var, *options_list, command=option_selected)
option_menu.pack(pady=20)

# Etiqueta para mostrar la opción seleccionada
label_selected = tk.Label(root, text="Opción seleccionada: ")
label_selected.pack()

tk.OptionMenu(root, )


root.mainloop()




# rename_unique() # AVOID REPEATED NAMES
# rename_invoice("receive", name)