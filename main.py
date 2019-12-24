import requests
import re
import io
import urllib.request
import os
import variables
from threading import Thread
from bs4 import BeautifulSoup

def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text

def remove_file(filename):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
    if(os.path.exists(path)):
        os.remove(path)

def main():
    # import sitemap_parser
    with open("links.txt", "r") as links:
        urls = links.readlines()
    urls = [item.replace("\n", "") for item in urls]
    remove_file('result.txt')

    threads = []
    filenames = []

    for url in urls:
        test = url.split("/")
        name = test[len(test)-2]
        path = os.path.join(os.path.abspath(os.path.dirname(__file__) + "/txt/"), name  + ".txt")
        if(os.path.exists(path)):
            os.remove(path)
        filenames.append(name + ".txt")
        process = Thread(target=parseLinks, args=(url, name,), daemon = True)
        process.start()
        threads.append(process)

    for process in threads:
        process.join()

    with open('result.txt', 'w') as outfile:
        for fname in filenames:
            with io.open("./txt/" + fname) as infile:
                outfile.write(infile.read())
            path = os.path.join(os.path.abspath(os.path.dirname(__file__) + "/txt/"), fname)
            if(os.path.exists(path)):
                os.remove(path)

def parseLinks(url, name):
    # print("base url: ", url)
    r = requests.get(url)
    with io.open("./html/" + name + ".html", "w") as output_file:
        output_file.write(r.text)

    text = read_file("./html/" + name+".html")
    soup = BeautifulSoup(text, features="lxml")
    # try:
    pages = soup.find('div', {'class': re.compile('catalog-pagination')}).find_all('a')
    page_count = int(pages[len(pages)-2].text)
    for x in range(page_count+1):
        getItems(x, url, name)
    # except:
    #     print("Не нашел кол-во страниц")
    getItems(x, url, name)

def getItems(x, url, name):
    try:
        r = requests.get(url+"?PAGEN_1="+str(x))
        with io.open("./html/" + name+".html", "w") as output_file:
            output_file.write(r.text)
        # text = r.text
        text = read_file("./html/" + name+".html")
        soup = BeautifulSoup(text, features="lxml")
        item_list = soup.find('div', {'class': re.compile('products-flex-grid product-grid')})
        if(item_list):
            items = item_list.find_all('div', {'class': re.compile("products-flex-item isotope-item *")})
            for item in items:
                findItem(item, name)
    except Exception as e:
        print(e, "\nadditional url: " + url+"?PAGEN_1="+str(x))
        # print(r.text.encode().replace('\xb3',''))

def findItem(item, name):
    item_link = item.find('div', {'class': 'name'}).find('a').get('href')
    splitted_link = item_link.split('/')
    item_id = splitted_link[len(splitted_link)-2]
    if item_id not in variables.elements_list:
        variables.elements_list.append(item_id)
        item_name = item.find('div', {'class': 'name'}).find('a').text
        try:
            item_price = item.find('div', {'id': re.compile('_price_block')}).text.strip().split()[0]
        except:
            item_price = "Нет в наличии"
        with open("./txt/" + name+".txt", "a") as result_file:
            string = item_id + "\t" + item_name
            try:
                result_file.write(string)
            except UnicodeEncodeError as e:
                print(type(item_name))
            for k in range(len(string), 110):
                string+=" "
                result_file.write(" ")
            string=str(variables.count) + ".\t" + string
            string+=item_price + "\n"
            result_file.write(item_price + "\n")
        # print(string)
        variables.count+=1
    # else:
        # print("Duplicate element with id: " + item_id)

if __name__ == "__main__":
    main()
