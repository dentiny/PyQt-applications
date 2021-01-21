#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is for printing single-sided papers. 

import os;
import sys;
from PyPDF2 import PdfFileWriter, PdfFileReader;

filename = sys.argv[1];
outfile = "{}-{}.pdf".format(filename[:-4], "blank");
inputpdf = PdfFileReader(open(filename, "rb"));
output = PdfFileWriter();
for i in range(inputpdf.numPages):
    output.addPage(inputpdf.getPage(i));
    output.addBlankPage()
with open(outfile, "wb") as outputStream:
    output.write(outputStream);

# Delete original file and rename.
os.remove(filename);
os.rename(outfile, filename);