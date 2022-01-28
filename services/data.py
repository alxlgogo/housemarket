from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd


# Get all house rental page url
def get_urls(city_name, page_number, base_url):
    # base_url = "https://www.myhome.ie/rentals/" + city_name + "/property-to-rent?page="
    # base_url = "https://www.myhome.ie/rentals/dublin/property-to-rent-in-dublin-12?page="
    urls = []
    if page_number == 1:
        urls.append(base_url + "1")
    else:
        for x in range(1, int(page_number)):
            urls.append(base_url + str(x))
    return urls


def get_soup(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    return soup


def parse_page(soup, writer):
    houses = soup.find_all("div", {"class": "PropertyListingCard__PropertyInfo"})
    print("x")
    for house in houses:
        address = house.find("a", {"class": "PropertyListingCard__Address"}).text
        area = address.split(',')[-1]
        # print(address)
        price = house.find("div", {"class": "PropertyListingCard__Price"}).text
        price = price.replace(" ", "").replace(",", "").replace("€", "")
        # print(price)
        spans = house.find_all("span", {"class": "PropertyInfoStrip__Detail"})
        # print(spans)
        otherinfo = ""
        bed = ""
        bath = ""
        cube = ""
        home = ""
        for span in spans:
            bed_tage = span.find("app-mh-icon", {"icon": "bed"})
            bath_tage = span.find("app-mh-icon", {"icon": "bath"})
            cube_tage = span.find("app-mh-icon", {"icon": "cube"})
            home_tage = span.find("app-mh-icon", {"icon": "home"})
            if bed_tage is not None:
                bed = span.text
            if bath_tage is not None:
                bath = span.texts
            if cube_tage is not None:
                cube = span.text
            if home_tage is not None:
                home = span.text
            otherinfo += span.text
        writer.writerow([bed, bath, cube, home, price, area, address])


def scrape_data(city_name, file_name, page_number, base_url):
    file = open("./data/" + file_name + '.csv', 'w')
    writer = csv.writer(file)
    writer.writerow(['bed', 'bath', 'cube', 'home', 'price', 'area', 'address'])
    urls = get_urls(city_name, page_number, base_url)
    for url in urls:
        soup = get_soup(url)
        parse_page(soup, writer)
    file.close()


def convert_address_to_lat_and_lng(city_name):
    file_name = city_name + '.csv'
    data = pd.read_csv("../" + file_name)
    longitude = []
    latitude = []
    full_address = []
    addresses = data['address']
    for location in addresses:
        is_na_n = pd.isna(location)
        if is_na_n:
            latitude.append('')
            longitude.append('')
            full_address.append('')
        else:
            geo_data = get_latitude_and_longitude(location)
            geo_latitude = geo_data['results'][0]['geometry']['location']['lat']
            geo_longitude = geo_data['results'][0]['geometry']['location']['lng']
            formatted_address = geo_data['results'][0]['formatted_address']
            latitude.append(geo_latitude)
            longitude.append(geo_longitude)
            full_address.append(formatted_address)
    data['latitude'] = latitude
    data['longitude'] = longitude
    data['full_address'] = full_address
    write_data_to_csv(data, city_name)


def get_latitude_and_longitude(location):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?address="
    key = "&key="
    url = base_url + location + key
    r = requests.get(url=url)
    data = r.json()
    return data


def write_data_to_csv(data, file_name):
    data.to_csv("./new" + file_name + '.csv')

# convert_address_to_lat_and_lng("Dublin")
