import lxml
import requests
from lxml import html
from lxml import etree
import io

userId = 47305
mainLink = "http://gorod.gov.spb.ru"
pageNumber = 1

class Problem(object):
    def __init__(self):
        self.link = ""
        self.address = ""
        self.nomer = 0
        self.lat = 0.0
        self.lng = 0.0

    def toString(self):
        out = "Проблема" + "\n" + "Ссылка:" + self.link + "\n" + "Адрес:" + self.address + "\n"
        out += "Координаты: " + str(self.lat) + ", " + str(self.lng) + "\n"

        return out

def parseCoordPage(problem):
    url = problem.link + "map/"

    req = requests.get(url)

    tree = html.fromstring(req.text)

    problemsCords = tree.xpath('.//div[contains(@class, "map-page-block margin-top-sm")]/@data-map')[0]

    point1 = str(problemsCords).find(":", 30)
    point11 = str(problemsCords).find(",", 35)
    point2 = str(problemsCords).find(":", 50)
    point22 = str(problemsCords).find("}", 50)

    strLat = str(problemsCords)[point1 + 1: point11]
    strLng = str(problemsCords)[point2 + 1:point22]

    lat = float(strLat)
    lng = float(strLng)
    problem.lat = lat
    problem.lng = lng



url = mainLink + "/accounts/" + str(userId) + "/?per_page=60&page=" + str(pageNumber)

r = requests.get(url)

with io.open('test.html', 'w', encoding="utf-8") as output_file:
  output_file.write(r.text)

ht = r.text

tree = html.fromstring(ht)

# print tree.xpath('//div[contains(@class, \'row block-messages-container\')]//a')[0]
problems_links = tree.xpath('.//div[contains(@class, "row block-messages-container")]//a/@href')

address_list = tree.xpath('.//div[contains(@class, "address")]/@title')

pagesCount = tree.xpath('.//div[contains(@class, "btn-toolbar")]//a[contains(@class, "btn btn-default rounded")]/.')[0]


problems = list()

#for page in range (1, int(pagesCount.text) + 1 ):
for page in range(1, 2):

    url = mainLink + "/accounts/" + str(userId) + "/?per_page=60&page=" + str(page)

    r = requests.get(url)

    with io.open('test.html', 'w', encoding="utf-8") as output_file:
        output_file.write(r.text)

    ht = r.text

    tree = html.fromstring(ht)

    problems_links = tree.xpath('.//div[contains(@class, "row block-messages-container")]//a/@href')

    address_list = tree.xpath('.//div[contains(@class, "address")]/@title')

    i = 0
    for link in problems_links:
        prob = Problem()
        prob.address = address_list[i]
        prob.link = mainLink + link
        i = i + 1
        parseCoordPage(prob)
        problems.append(prob)


with open('problems.html', 'w') as output3_file:
    output3_file.write("Всего страниц: " + pagesCount.text)
    for problem in problems:
        output3_file.write(problem.toString() + "\n")











#
#with open('links.html', 'w') as output1_file:
#    for problem in problems_links:
#        output1_file.write("http://gorod.gov.spb.ru" + problem + "\n")
#
#with open('address.html', 'w', encoding='utf-8') as output2_file:
#    for problem in address_list:
#        # output2_file.write(etree.tostring(problem).decode('utf-8'))
#        # output2_file.write(str(problem).encode('cp1251').decode() + "\n")
#        output2_file.write(str(problem) + "\n")

