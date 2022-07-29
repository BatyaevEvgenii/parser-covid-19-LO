import requests
from bs4 import BeautifulSoup
import json

from user_agent import generate_user_agent
# представляемся что мы не бот
headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}

# откуда берем
# ковид в ЛО
url = 'http://47.rospotrebnadzor.ru/content/%D0%BE%D0%B1%D1%89%D0%B5%D0%B5-%D1%87%D0%B8%D1%81%D0%BB%D0%BE-%D0%B7%D0%B0%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D1%8B%D1%85-%D1%81%D0%BB%D1%83%D1%87%D0%B0%D0%B5%D0%B2-covid-2019-%D0%BD%D0%B0-%D1%82%D0%B5%D1%80%D1%80%D0%B8%D1%82%D0%BE%D1%80%D0%B8%D0%B8-%D0%BB%D0%B5%D0%BD%D0%B8%D0%BD%D0%B3%D1%80%D0%B0%D0%B4%D1%81%D0%BA%D0%BE%D0%B9-%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D0%B8-%D1%81-1'


# что бы не забанили ставим таймаут и "заголовок что мы не бот"
response = requests.get(url, timeout=5, headers=headers).text

with open('data.html', 'w') as output_file:
    output_file.write(response)

with open('data.html', 'r') as read_file:
    content = read_file.read()
    soup = BeautifulSoup(content, "lxml")
    table = soup.find('table')
    list = soup.find('div', attrs={'class': 'field-item even'})


with open('list.html', 'w') as output_file:
    output_file.write(list.prettify())

    count = 0
    arrayOfCOVID = []

    for row in table.tbody.find_all('tr'):
        columns = row.find_all('td')

        if (len(columns) == 4 ):
            city = columns[0].text.strip()
            # peopleSick = columns[2].contents[0].strip()
            # peopleHealth = columns[3].contents[0].strip()
            peopleSick = columns[2].text.strip()
            peopleHealth = columns[3].text.strip()
            # count += 1
            arrayOfCOVID.append({'city': city, 'peopleIll': peopleSick, 'peopleHealth': peopleHealth})

        if (len(columns) != 4):
            city = columns[2].text.strip()
            peopleSick = columns[4].text.strip()
            peopleHealth = columns[5].text.strip()
            # count += 1
            arrayOfCOVID.append({'city': city, 'peopleIll': peopleSick, 'peopleHealth': peopleHealth})
        count += 1
    
    print(count)

    for elem in arrayOfCOVID:
        if (elem['city'] == 'Населённый пункт' or elem['city'] == 'Всего случаев' or elem['city'] == '0'):
            index = arrayOfCOVID.index(elem)
            if (index > -1):
                arrayOfCOVID.pop(index)

    total = 0
    for elem in arrayOfCOVID:
        total += int(elem['peopleIll'])

    print("Всего человек по ЛО:", total)
    print("Всего городов по ЛО:", len(arrayOfCOVID))

    with open('cities.json', 'w', encoding='utf8') as output_file:
        json.dump(arrayOfCOVID[:999], output_file, ensure_ascii=False)
    
    with open('cities2.json', 'w', encoding='utf8') as output_file:
        json.dump(arrayOfCOVID[999:1998], output_file, ensure_ascii=False)
    
    with open('cities3.json', 'w', encoding='utf8') as output_file:
        json.dump(arrayOfCOVID[1999:], output_file, ensure_ascii=False)