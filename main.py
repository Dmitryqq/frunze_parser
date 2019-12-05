import requests
import re
import io
import urllib.request
import os
from bs4 import BeautifulSoup

def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text

def main():
    import sitemap_parser
    with open("links.txt", "r") as links:
        urls = links.readlines()
    urls = [item.replace("\n", "") for item in urls]
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'result.txt')
    if(os.path.exists(path)):
        os.remove(path)
    count = 1
    elements_list = []
    for url in urls:
        try:
            r = requests.get(url)
            with io.open("test.html", "w") as output_file:
              output_file.write(r.text)
            text = read_file("test.html")
            soup = BeautifulSoup(text, features="lxml")
            item_list = soup.find('div', {'class': re.compile('products-flex-grid product-grid')})
            items = item_list.find_all('div', {'class': re.compile("products-flex-item isotope-item *")})
            for item in items:
                item_link = item.find('div', {'class': 'name'}).find('a').get('href')
                splitted_link = item_link.split('/')
                item_id = splitted_link[len(splitted_link)-2]
                if item_id not in elements_list:
                    elements_list.append(item_id)
                    item_name = item.find('div', {'class': 'name'}).find('a').text
                    item_price = item.find('div', {'id': re.compile('_price_block')}).text.strip().split()[0]
                    with open("result.txt", "a") as result_file:
                        string = item_id + "\t" + item_name
                        result_file.write(str(count) + ".\t\t" + string) if count < 100 else result_file.write(str(count) + ".\t" + string)
                        for k in range(len(string), 110):
                            string+=" "
                            result_file.write(" ")
                        string=str(count) + ".\t" + string
                        string+=item_price + "\n"
                        result_file.write(item_price + "\n")
                    print(string)
                    count+=1
                else:
                    print("Duplicate element with id: " + item_id)
        except:
            print("Nothing found on the %s" % url)

if __name__ == "__main__":
    main()
