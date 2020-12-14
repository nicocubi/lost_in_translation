# Nicolas Soler 06 Dec. 2020
# Script to extract text and Metadata from a pdf file
# All the PDF files were downloaded from https://www.elejandria.com/
# Several command line tools are used here
# - exiftool (install with sudo apt install  libimage-exiftool-perl)
# pdfinfo and pdftotext from xpdf

import os, sys, glob

root="/home/nicolas/CODE/lostInTranslation/data/pdf"
#cmd = 'exiftool -Title="<TITLE>" -Author="<AUTHOR>" -Subject="<SOURCE_LANG>"" <PDF_FILE>'
directories= ('spanish', 'english', 'french', 'german', 'italian', 'russian')

for lang in directories:
    if os.path.exists(diret):
        # Set correct metadata for all files
        pdfFiles= glob.glob(os.path.join(root,lang,"*.pdf"))
        for pdf in pdfFiles:
            title, author= os.path.basename(pdf).split('.')[0].split('-')
            print(title,author)


