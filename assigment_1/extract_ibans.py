import PyPDF2
import os
import codecs
import re

regex_string = "[A-Z]{2}\d{2} (?:\d{4} ){3}\d{4}(?: \d\d?)?"



search_text = "\n"
replace_text = ""

found_list = []

path = "./iban"
for file in os.listdir(path):
    filename = path + "/" + file
    try:
        PyPDF2.PdfFileReader(open(filename, "rb"))
    except:
        pass
    else:
        with codecs.open(filename + ".txt", "w", encoding="utf-8") as f:
            reader = PyPDF2.PdfFileReader(filename)
            pageObj = reader.getNumPages()
            for page_count in range(pageObj):
                page = reader.getPage(page_count)
                page_data = page.extract_text()
                f.write(page_data)
        with codecs.open(filename + ".txt", "r", encoding="utf-8") as f:
            data = f.read()
            data = data.replace(search_text, replace_text)
            plain_txt = data.encode('UTF-8')
            found = re.findall(regex_string, plain_txt, re.M)
            print(found)
with codecs.open(path + "/ibans.txt", "w", encoding="utf-8") as f:
    for string in found:
        f.write(string +"\n")