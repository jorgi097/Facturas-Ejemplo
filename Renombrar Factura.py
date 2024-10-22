from PyPDF2 import PdfReader
import re
import os
import time

# CLEAR SCREEN
os.system("cls")

# DEFINE GLOBAL VARIABLES
extension = ".pdf"
rename_done = {}

# DEFINE FUNCTIONS
def get_content(file): # GET PDF CONTENT
    reader = PdfReader(file)
    page = reader.pages[0]
    content = page.extract_text()
    content = content.lower()
    return content

def is_invoice(text): # GET FILE TYPE
    result = "uso cfdi" in text
    return result

def get_date(text): # GET DATE
    match_date = re.search(r'emisión:\d{5}\s*(\w+)-(\w+)-(\w+)', text)
    day = match_date.group(3)
    month = match_date.group(2)
    year = match_date.group(1)
    return year, month, day

def get_receptor( text): # GET RECEPTOR
    match_receptor = re.search(r'nombre receptor:\s*(\w+)', text)
    receptor = match_receptor.group(1)
    return receptor

def get_sender(text): # GET SENDER
    match_sender = re.search(r'nombre emisor:\s*(.*)', text)
    sender = match_sender.group(1)
    return sender

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


# AVOID REPITED NAMES
rename_unique()


def rename_invoice():
    invoice_dir = get_invoice()
    
    for invoice in invoice_dir:
        text = get_content(invoice)
        year, month, day = get_date(text)
        receptor = get_receptor(text) 
        sender = get_sender(text)
        is_recibida = receptor == "grecia"

        if(is_recibida):
            base_filename = f'Recibida {year}-{month}-{day} - {sender}'.upper()

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
                
                
rename_invoice()