from tkinter import Tk
from tkinter.filedialog import askopenfilename
from PyPDF2 import PdfFileReader, PdfFileWriter
import sys

tk = Tk()
tk.withdraw()


class PDFManager:
    @staticmethod
    def delete_pages(pdf, *args):
        """
        :argument: pdf as PyPDF2.PdfFileReader-Object, list of pages to delete(int)
        :returns: PyPDF2.PdfFileWriter-Object of edited dpf
        """
        output = PdfFileWriter()
        pages_to_delete = []
        for i in args:
            pages_to_delete.append(i-1)

        for page in range(pdf.getNumPages()):
            if page not in pages_to_delete:
                output.addPage(pdf.getPage(page))
        return output

    @staticmethod
    def merge_pdf(*args):
        """
        :argument: list of PyPDF2.PdfFileReader-Objects, they are appended in order
        :returns: PyPDF2.PdfFileWriter-Object of merged pdfs
        """
        output = PdfFileWriter()
        for pdf in args:
            for page in range(pdf.getNumPages()):
                output.addPage(pdf.getPage(page))
        return output

    @staticmethod
    def generate_reader(path):
        """
        :argument: systempath to pdf
        :returns: PyPDF2.PdfFileReader-Object
        """
        return PdfFileReader(path, 'rb')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please run this script with either "-d"(delete pages) or "-m"(merge pdfs) as parameter!')
    else:
        if sys.argv[1] == '-d':
            deletable_pages = []
            print('Please select the pdf you want to delete pages of.')
            filename = askopenfilename()
            new_filename = filename[:-4] + '_edited.pdf'
            infile = PdfFileReader(filename, 'rb')
            raw_pages = input('Please insert all pages you want to delete, separated by a colon.')
            pages = raw_pages.split(',')
            try:
                for j in pages:
                    deletable_pages.append(int(j))
            except ValueError:
                print('At least one entered value was not a valid page-number!')
            outfile = PDFManager.delete_pages(infile, *deletable_pages)
            with open(new_filename, 'wb') as f:
                outfile.write(f)
            print(f'Your pdf was edited and saved as: {new_filename}')
        if sys.argv[1] == '-m':
            pdf_list = []
            print('Please select the pdf you want to append other pdfs to.')
            filename = askopenfilename()
            new_filename = filename[:-4] + '_edited.pdf'
            pdf_list.append(PDFManager.generate_reader(filename))
            state = True
            counter = 1
            while state is True:
                print(f'Do you want to append a pdf?, currently selected pdfs: {counter} (y|n)')
                answer = input()
                if answer == 'y' or answer == 'Y':
                    print('Please select a pdf you want to append to your currently selected ones.')
                    appendfilename = askopenfilename()
                    pdf_list.append(PDFManager.generate_reader(appendfilename))
                    counter += 1
                elif answer == 'n' or answer == 'N':
                    state = False
                else:
                    print('Invalid response, please use "y" or "n".')
            outfile = PDFManager.merge_pdf(*pdf_list)
            with open(new_filename, 'wb') as f:
                outfile.write(f)
            print(f'Your pdfs were merged and saved as: {new_filename}')
