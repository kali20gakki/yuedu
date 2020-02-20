#!/usr/bin/env python3
# coding:utf-8

from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import os
import sys
import json, logging
from config import BookPath
logging.basicConfig(stream=sys.stderr, format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)



def add_bookmarks(path, file_dir):
    temp = os.path.join(file_dir, 'bookmark.json')
    with open(temp, 'rb') as f:
        bookmarks = json.load(f)['Data']
    book = PdfFileReader(path)
    pdf = PdfFileWriter()
    pdf.cloneDocumentFromReader(book)
    for bookmark in bookmarks:
        try:
            pdf.addBookmark(bookmark['Title'], bookmark['Page'] - 1)
        except:
            break
    try:
        with open(path[0:path.rfind('.')] + '.bookmark.pdf', 'wb') as fout:
            pdf.write(fout)
    except FileNotFoundError:
        pass


def file_name_walk(file_dir, bookid):
    for root, dirs, files in os.walk(file_dir):
        if 'bookmark.json' in files:
            files.remove('bookmark.json')
        files.sort(key=lambda x: int(x[x.rfind('-') + 1:][:-4]))

        merger = PdfFileMerger(strict=False)
        for file in files:
            temp = os.path.join(file_dir, file)
            merger.append(temp)

        name = files[0][:files[0].rfind('-')] + '.pdf'     
        path = os.path.join(BookPath, bookid, name)
        #logging.info(path)
        merger.write(path)
        logging.info('%s merger ok'%bookid)
        add_bookmarks(path, file_dir)


if __name__ == '__main__':
    pass
    #file_name_walk('')