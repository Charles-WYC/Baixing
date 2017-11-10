import codecs

file = codecs.open("page.txt", "r", "utf-8")
pageFile = file.read()
file.close()
pageList = pageFile.split('\n')
print len(pageList)
pageSet = set(pageList)
print len(pageSet)
file = codecs.open("final_page.txt", "w", "utf-8")
for page in pageSet:
    if page != '':
        file.write(page)
        file.write('\n')
file.close()