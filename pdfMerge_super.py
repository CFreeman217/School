import os, datetime
import PyPDF2

def add_to_writer(pdf, writer, start, end):
    for i in range(start-1, end):
        writer.addPage(pdf.getPage(i))

def get_filename(prefix, suffix, base_path):
    '''
    Gets a unique file name in the base path.

    Appends date and time information to file name and adds a number
    if the file name is stil not unique.
    prefix = Homework assignment name
    suffix = Extension
    base_path = Location of log file
    '''
    # Set base filename for compare
    fileNameBase = base_path + prefix + "_" + datetime.datetime.now().strftime("%b_%d_%H_%M")
    # Set base for numbering system if filename exists
    num = 1
    # Generate complete filename to check existence
    fileName = fileNameBase + suffix
    # Find a unique filename
    while os.path.isfile(fileName):
        # if the filename is not unique, add a number to the end of it
        fileName = fileNameBase + "_" + str(num) + suffix
        # increments the number in case the filename is still not unique
        num = num + 1
    return fileName

class PDF_FILE:

    num_pdfs = 0
    loaded_pdfs = {}
    status = 0

    def __init__(self, filename):
        PDF_FILE.num_pdfs += 1
        self.name = filename[:-4]
        self.pdf = load_pdf(filename)
        self.pages = self.pdf.getNumPages()
        self.item_no = PDF_FILE.num_pdfs
        self.write_order = 0
        PDF_FILE.loaded_pdfs[self.item_no] = self

    @staticmethod
    def load_pdf(filename):
        f = open(filename, 'rb')
        return PyPDF2.PdfFileReader(f)

    @classmethod
    def find_pdf(cls):
        for file_name in os.listdir('.'):
            if file_name.endswith('.pdf'):
                if file_name.startswith('._'):
                    pass
                else:
                    cls(file_name)

    @classmethod
    def display_pdflist(cls):
        disptitle = ' PDF files in this folder not selected for merge '
        titlewidth = len(disptitle) + 8
        print(disptitle.center(titlewidth, '~'))
        for found_file in cls.loaded_pdfs:
            if found_file.write_order == 0:
                print('[ {} ] \t {}'.format(found_file.item_no, found_file.name))
        try:
            return input('Select item number or [m] for merge file list: ')


output_file = open(f'{output_filename}.pdf','wb')
writer = PyPDF2.PdfFileWriter()



add_to_writer(pdf1, writer, start1, end1)
add_to_writer(pdf2, writer, start2, end2)

writer.write(output_file)
output_file.close()

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
start1 = input('Start on page [1]: ')
if start1 == '':
        start1 = 1
else:
        start1 = int(start1)
end1 = input('End on page [last]: ')
if end1 == '':
        end1 = pdf1_pages
else:
        end1 = int(end1)

print(f'{filename2} has {pdf2_pages} pages.')
start2 = input('Start on page [1]: ')
if start2 == '':
        start2 = 1
else:
        start2 = int(start2)
end2 = input('End on page [last]: ')
if end2 == '':
        end2 = pdf2_pages
else:
        end2 = int(end2)

output_filename = input('Save new file as : ')
if output_filename == '':
        output_filename = 'combine'




