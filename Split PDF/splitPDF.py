# -*- coding: utf-8 -*-
# This program is created to split a PDF into multiple sub-PDFs, just for printing in Duke
import sys;
from PyPDF2 import PdfFileWriter, PdfFileReader;

cnt = 0; # splitted pdf index
for filename in sys.argv[1:]:
    inputpdf = PdfFileReader(open(filename, "rb"));
    for i in range(inputpdf.numPages):
        output = PdfFileWriter();
        output.addPage(inputpdf.getPage(i));
        with open("document-page%s.pdf" % cnt, "wb") as outputStream:
            cnt += 1;
            output.write(outputStream);