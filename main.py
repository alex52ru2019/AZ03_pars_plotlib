# Необходимо спарсить цены на диваны с сайта divan.ru в csv файл,
# обработать данные, найти среднюю цену и вывести ее,
# а также сделать гистограмму цен на диваны

# !!!очистить содержимое файла prices_divan.csv перед новым запуском программы

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import matplotlib.pyplot as plt

start_url = "https://www.divan.ru/nizhny-novgorod/category/divany-i-kresla?types%5B%5D=1"  # только диваны
# Заголовки для имитации запроса от браузера
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


########################################################
########### Фйнкция парсинга цены ######################
########################################################
def next_pasrs(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Находим все элементы <span> с нужными классами и data-testid
        price_spans = soup.find_all('span', class_='ui-LD-ZU KIkOH', attrs={'data-testid': 'price'})
        prices = []
        for price_span in price_spans:
            price_text = price_span.get_text(strip=True)
            # Извлекаем только цифры
            price = ''.join(filter(str.isdigit, price_text))
            prices.append(price)
        # print(f"\npage = {i}\n{prices}")
        return (prices)
    else:
        print(f"Ошибка при запросе страницы: {response.status_code}")


########################################################
############ Узнаем количество страниц #################
########################################################

# Выполняем первый GET-запрос
response = requests.get(start_url, headers=headers)
# Проверяем, что запрос успешен
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # ищем количество страниц в категории
    pagination_links = soup.find_all('span', class_='ui-GPFV8 ui-BjeX1 ui-gI0j8 PaginationLink')
    number_of_page = int(pagination_links[len(pagination_links) - 2].get_text(strip=True))
#    print(f"page = {number_of_page}")
else:
    print(f"Ошибка при запросе страницы: {response.status_code}")

########################################################
############# Парсим и записываем в файл ###############
########################################################

for i in range(1, number_of_page + 1, 1):
    if i == 1:
        next_url = start_url
    else:
        next_url = "https://www.divan.ru/nizhny-novgorod/category/divany-i-kresla/page-" + str(i) + "?types%5B%5D=1"
    prices = next_pasrs(next_url)
    #  print(f"\npage = {i}\n{prices}")
    # Открываем CSV файл для записи
    with open('prices_divan.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if i == 1:
            writer.writerow(['Price'])  # Записываем заголовок столбца
        # Записываем данные
        for price in prices:
            writer.writerow([price])

########################################################
############## средняя цена ############################
########################################################

# Загрузка данных из CSV файла
data = pd.read_csv('prices_divan.csv')

# Вычисление средней цены
print(f"Средняя цена = {data['Price'].mean()}")

########################################################
############## График цен  #############################
########################################################

values = data['Price']

# Построение гистограммы
plt.hist(values, bins=25, color='blue', edgecolor='black')

# Добавление заголовка и меток осей
plt.title('Гистограмма цен по всем страницам с диванами')
plt.xlabel('Значение')
plt.ylabel('Частота')

# Отображение графика
plt.show()