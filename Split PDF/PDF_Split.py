# -*- coding: utf-8 -*-

# This Python script is programmed to split several pages from the source PDF file.

import sys;
from PyPDF2 import PdfFileWriter, PdfFileReader;

def splitPDF(file, start, end):
    with open(file, "rb") as f1:
        src = PdfFileReader(f1);
        content = PdfFileWriter();
        for idx in range(start, end + 1): 
            content.addPage(src.getPage(idx));
        with open("Result.pdf", "wb") as f2:
            content.write(f2);
    
if(__name__ == "__main__"):
    # get filename and target pages
    file = sys.argv[1];
    start, end = int(sys.argv[2]), int(sys.argv[3]);
    splitPDF(file, start, end);