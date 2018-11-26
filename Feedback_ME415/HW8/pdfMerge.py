import os
import PyPDF2

def load_pdf(filename):
        f = open(filename, 'rb')
        return PyPDF2.PdfFileReader(f)

def add_to_writer(pdf, writer, start, end):
        for i in range(start-1, end):
                writer.addPage(pdf.getPage(i))

for file_name in os.listdir('.'):
        if file_name.endswith('.pdf'):
                if file_name.beginswith('._'):
                        pass
                else
                        print(file_name)

print('Welcome to the PDF Merger')

filename1 = input('Input File Name : ')
if filename1 == '':
        filename1 = 'combine'
filename2 = input('Input File Name : ')
if filename2 == '':
        filename2 = 'combine'

pdf1 = load_pdf(filename1)
pdf2 = load_pdf(filename2)

pdf1_pages = pdf1.getNumPages()
pdf2_pages = pdf2.getNumPages()

print(f'{filename1} has {pdf1_pages} pages.')
start1 = int(input('Start on page : '))
if start1 == ''
        start1 = 1
end1 = int(input('End on page : '))
if end1 == ''
        end1 = pdf1_pages

print(f'{filename2} has {pdf2_pages} pages.')
start2 = int(input('Start on page : '))
if start2 == ''
        start2 = 1
end2 = int(input('End on page : '))
if end2 == ''
        end2 = pdf1_pages

output_filename = input('Save new file as : ')
if output_filename == '':
        output_filename = 'combine'

output_file = open(f'{output_filename}.pdf','wb')
writer = PyPDF2.PdfFileWriter()



add_to_writer(pdf1, writer, start1, end1)
add_to_writer(pdf2, writer, start2, end2)

writer.write(output_file)
output_file.close()


