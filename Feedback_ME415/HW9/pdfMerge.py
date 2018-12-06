import os
import PyPDF2

def load_pdf(filename):
        f = open(filename, 'rb')
        return PyPDF2.PdfFileReader(f)

def add_to_writer(pdf, writer, start, end):
        for i in range(int(start)-1, int(end)):
                writer.addPage(pdf.getPage(i))

def displayPDF(in_list):
        dispTitle = ' Welcome to the PDF Merger '
        titlewidth = len(dispTitle)
        leftcol = 5
        maxwidth = titlewidth + leftcol
        for i in in_list:
                if len(i) + leftcol > maxwidth:
                        maxwidth = len(i) + leftcol
        print(dispTitle.center(maxwidth, '='))
        for i in range(len(in_list)):
                print(f'[{i}]'.center(leftcol) + in_list[i].ljust(maxwidth - leftcol))

pdf_files = []
for file_name in os.listdir('.'):
        if file_name.endswith('.pdf'):
                if file_name.startswith('._'):
                        pass
                else:
                        pdf_files.append(file_name)

displayPDF(pdf_files)

filename1 = input('Input File Name : ')
if filename1 == '':
        filename1 = 'combine.pdf'
elif filename1.isdigit():
        filename1 = pdf_files[int(filename1)]
        print(filename1)
else:
        pass
filename2 = input('Input File Name : ')

if filename2 == '':
        filename2 = 'combine.pdf'
elif filename2.isdigit():
        filename2 = pdf_files[int(filename2)]
        print(filename2)
else:
        pass

pdf1 = load_pdf(filename1)
pdf2 = load_pdf(filename2)

pdf1_pages = pdf1.getNumPages()
pdf2_pages = pdf2.getNumPages()

print(f'{filename1} has {pdf1_pages} pages.')
start1 = (input('Start on page : '))
if start1 == '':
        start1 = 1
end1 = (input('End on page : '))
if end1 == '':
        end1 = pdf1_pages

print(f'{filename2} has {pdf2_pages} pages.')
start2 = (input('Start on page : '))
if start2 == '':
        start2 = 1
end2 = (input('End on page : '))
if end2 == '':
        end2 = pdf2_pages

output_filename = input('Save new file as : ')
if output_filename == '':
        output_filename = 'combine'

output_file = open(f'{output_filename}.pdf','wb')
writer = PyPDF2.PdfFileWriter()



add_to_writer(pdf1, writer, start1, end1)
add_to_writer(pdf2, writer, start2, end2)

writer.write(output_file)
output_file.close()


