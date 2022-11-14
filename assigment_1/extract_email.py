import PyPDF2
import os
import codecs
import re

search_text = "\n"
replace_text = ""

found_list = []

path = "./scans"
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
                page_data = page.extractText()
                f.write(page_data)
        with codecs.open(filename + ".txt", "r", encoding="utf-8") as f:
            data = f.read()
            data = data.replace(search_text, replace_text)
            plain_txt = data.encode('UTF-8')
            found = re.findall(r"[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*@[a-zA-Z0-9\-]+(?:\.[a-zA-Z0-9]+)*", plain_txt, re.M)
            for ele in found:
                found_list.append(ele)
with codecs.open(path + "/email.txt", "w", encoding="utf-8") as f:
    for string in found_list:
        f.write(string +"\n")