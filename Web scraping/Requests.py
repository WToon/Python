import requests


test = requests.get("http://www.hipstercode.com")

outfile = open("webscrape.html", "w")
test.encoding = 'ISO-8859-1'
outfile.write(str(test.text))
