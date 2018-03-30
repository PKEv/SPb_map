import lxml
import requests
from lxml import html
from lxml import etree
import io

#userId = 47305 #кустов
userId = 58004 #макаров
#userId = 7209 # Петр Г.
mainLink = "http://gorod.gov.spb.ru"
pageNumber = 1
problemsOnPage = 30


class Problem(object):
    def __init__(self):
        self.link = ""
        self.address = ""
        self.nomer = 0
        self.lat = 0.0
        self.lng = 0.0

    def toString(self):
        out = "Проблема " + str(self.nomer) + "\n" + "Ссылка:" + self.link + "\n" + "Адрес:" + self.address + "\n"
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


def writeMapFile(problems):
    lineStart = 18
    lineTitle = 12
    with open('shablon.html', 'r', encoding="utf-8") as f:
        shablonFile = list(f)
    my_file = open("map_new.html", 'w', encoding="utf-8")

    #Заменяем заголовок
    shablonFile[lineTitle - 1] = "<h3>Карта обращений поданных пользователем <a href=\"http://gorod.gov.spb.ru/accounts/"+ str(userId) +"\" target=\"_blank\">" + str(userId) + "</a></h3>"

    for ii in range (0, lineStart):
        my_file.write(shablonFile[ii])

    first = 1
    for problem in problems:
        if first == 1:
            first = 2
        else:
            my_file.write("         , ")
        my_file.write("{lat:" + str(problem.lat) + ",lng:" + str(problem.lng) + ",name:" + str(problem.nomer) + "} \n")

    for ii in range(lineStart, len(shablonFile)):
        my_file.write(shablonFile[ii])

    my_file.close()



url = mainLink + "/accounts/" + str(userId) + "/?per_page=" + str(problemsOnPage) + "&page=" + str(pageNumber)

r = requests.get(url)

with open('test.html', 'w', encoding="utf-8") as output_file:
  output_file.write(r.text)

ht = r.text
tree = html.fromstring(ht)
# читаем основные моменты
problems_links = tree.xpath('.//div[contains(@class, "row block-messages-container")]//a/@href')
address_list = tree.xpath('.//div[contains(@class, "address")]/@title')
pagesCount = tree.xpath('.//div[contains(@class, "btn-toolbar")]//a[contains(@class, "btn btn-default rounded")]/.')[0]

print("Total pages: " + str(pagesCount.text) + "\n")
problems = list()

for page in range (1, int(pagesCount.text) + 1 ):
# для тестов
#for page in range(1, 2):

    print("Current page: " + str(page )+ "/" + str(pagesCount.text) + "\n")

    url = mainLink + "/accounts/" + str(userId) + "/?per_page=" + str(problemsOnPage) + "&page=" + str(page)

    r = requests.get(url)
    ht = r.text
    tree = html.fromstring(ht)

    #читаем в списки
    problems_links = tree.xpath('.//div[contains(@class, "row block-messages-container")]//a/@href')
    address_list = tree.xpath('.//div[contains(@class, "address")]/@title')

    i = 0
    for link in problems_links:
        prob = Problem()
        prob.address = address_list[i]
        prob.link = mainLink + link
        addrList = str(link).split("/")
        prob.nomer = addrList[2]
        i = i + 1
        parseCoordPage(prob)
        problems.append(prob)
        print("Current problem: " + str(i) + "/" + str(len(problems_links)) + "\n")


with open('problems.html', 'w') as output3_file:
    for problem in problems:
        output3_file.write(problem.toString() + "\n")

writeMapFile(problems)
