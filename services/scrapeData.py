from bs4 import BeautifulSoup
import requests
from models.house import house


# Get all house rental page url
def getURLS():
    base_url = "https://www.myhome.ie/rentals/dublin/property-to-rent?page="
    urls = []
    for x in range(1, 3):
        urls.append(base_url + str(x))
    return urls;


urls = getURLS()


def getSoup(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    return soup;


def parsePage(soup):
    housesData = soup.find_all("div", {"class": "PropertyListingCard__PropertyInfo"})
    houseList = []
    for item in housesData:
        address = item.find("a", {"class": "PropertyListingCard__Address"}).text
        # print(address)
        price = item.find("div", {"class": "PropertyListingCard__Price"}).text
        # print(price)
        spans = item.find_all("span", {"class": "PropertyInfoStrip__Detail"})
        # print(spans)
        otherinfo = ""
        for span in spans:
            otherinfo += span.text
        # perHouse = house("1", "2", "3")
        perHouse = house(address, price, otherinfo)
        houseList.append(perHouse)
    return houseList


def getHouseData():
    houses = []
    urls = getURLS()
    for url in urls:
        soup = getSoup(url)
        houseList = parsePage(soup)
        houses.extend(houseList)
    return houses
