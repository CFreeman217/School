import os
from pyPDF2 import PdfFileReader, PdfFileMerger

pdf_files = list()

for file_name in os.listdir('.'):
    if file_name.endswith('.pdf'):
        pdf_files.extend(file_name)

merger = PdfFileMerger()

for f in pdf_files:
    merger.append(PdfFileReader(f),'rb')

merger.write('combine.pdf')