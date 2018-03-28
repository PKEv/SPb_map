import lxml
import requests
from lxml import html
from lxml import etree
import io

# user_id = 12345

url = 'http://gorod.gov.spb.ru/accounts/47305/?per_page=60' 
r = requests.get(url)

with io.open('test.html', 'w', encoding="utf-8") as output_file:
  output_file.write(r.text)

ht = r.text

tree = html.fromstring(ht)

# print tree.xpath('//div[contains(@class, \'row block-messages-container\')]//a')[0]
problems_list = tree.xpath('.//div[contains(@class, "row block-messages-container")]//a/@href')

address_list = tree.xpath('.//div[contains(@class, "address")]/@title')

#for problem in

#print etree.tostring(problems_list)

    
with open('links.html', 'w') as output1_file:
    for problem in problems_list:
        output1_file.write(problem + "\n")

with open('address.html', 'w', encoding='utf-8') as output2_file:
    for problem in address_list:
        # output2_file.write(etree.tostring(problem).decode('utf-8'))
        # output2_file.write(str(problem).encode('cp1251').decode() + "\n")
        output2_file.write(str(problem) + "\n")

