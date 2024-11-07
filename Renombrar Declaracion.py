from PyPDF2 import PdfReader
import re
import os

months = {
    "enero": "01",
    "febrero": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "agosto": "08",
    "septiembre": "09",
    "octubre": "10",
    "noviembre": "11",
    "diciembre": "12"
}

# LIST FILES IN FOLDER
dir = os.listdir()
dir = [file.lower() for file in dir]
pdfdir = [file for file in dir if file.endswith(".pdf")]


for file in pdfdir:
    # GET CONTENT
    reader = PdfReader(file)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    text = text.lower()

    # GET TYPE
    is_acuse = "acuse de recibo" in text
    is_declaracion = "Declaración Provisional o Definitiva de Impuestos Federales".lower() in text and "acuse de recibo" not in text

    # GET MONTH
    match_month = re.search(r'período de la declaración:\s*(\w+)', text)
    month = match_month.group(1)
    
    # GET YEAR
    match_year = re.search(r'ejercicio:\s*(\w+)', text)
    year = match_year.group(1)
    
    def replace_months(text, months_dict = months):
        for month, number in months_dict.items():
            text = text.replace(month, number)
        return text
    
    if is_acuse:
        try:
            os.rename(file, f'acuse {year}-{replace_months(month)}'.upper() + '.pdf')
        except PermissionError:
            print(f"El archivo {file} esta siendo utilizado por otro progrma.")
            print(f"Cierre el programa y corra este script de nuevo.")
    
    if is_declaracion:
        try:
            os.rename(file, f'declaracion {year}-{replace_months(month)}'.upper() + '.pdf')
        except PermissionError:
            print(f"El archivo {file} esta siendo utilizado por otro progrma.")
            print(f"Cierre el programa y corra este script de nuevo.")