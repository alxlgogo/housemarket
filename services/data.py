from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
import csv
import pandas as pd

# Get all house rental page url
from models.keys import Keys


def get_urls(city_name, page_number, base_url):
    # base_url = "https://www.myhome.ie/rentals/" + city_name + "/property-to-rent?page="
    # base_url = "https://www.myhome.ie/rentals/dublin/property-to-rent-in-dublin-12?page="
    urls = []
    if page_number == "1":
        urls.append(base_url + "1")
    else:
        for x in range(1, int(page_number)):
            urls.append(base_url + str(x))
    return urls


def get_soup(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    return soup


def parse_page(soup, writer, data_type):
    houses = soup.find_all("div", {"class": "PropertyListingCard__PropertyInfo"})
    for house in houses:
        address = house.find("a", {"class": "PropertyListingCard__Address"}).text
        area = address.split(',')[-1].strip()
        # print(address)
        price = house.find("div", {"class": "PropertyListingCard__Price"}).text

        if data_type.__eq__("selling"):
            price = price.replace(" ", "").replace(",", "").replace("€", "")
        else:
            prices = price.split("/")
            price = prices[0]
            if "to" in prices[0]:
                price = prices[0].split("to")[0]
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
                bed = span.text.strip()
            if bath_tage is not None:
                bath = span.text.strip()
            if cube_tage is not None:
                cube = span.text.strip()
            if home_tage is not None:
                home = span.text.strip()
            otherinfo += span.text
        writer.writerow([bed, bath, cube, home, price, area, address])


def scrape_data(city_name, file_name, page_number, base_url, data_type):
    file = open("./data/" + file_name + '.csv', 'w')
    writer = csv.writer(file)
    writer.writerow(['bed', 'bath', 'cube', 'home', 'price', 'area', 'address'])
    urls = get_urls(city_name, page_number, base_url)
    for url in urls:
        soup = get_soup(url)
        parse_page(soup, writer, data_type)
    file.close()


def convert_address_to_lat_and_lng(city_name, key):
    file_name = city_name + '.csv'
    data = pd.read_csv(file_name)
    data = remove_data_unit(data)
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
            geo_data = get_latitude_and_longitude(location, key)
            geo_latitude = geo_data['results'][0]['geometry']['location']['lat']
            geo_longitude = geo_data['results'][0]['geometry']['location']['lng']
            formatted_address = geo_data['results'][0]['formatted_address']
            latitude.append(geo_latitude)
            longitude.append(geo_longitude)
            full_address.append(formatted_address)
    data['latitude'] = latitude
    data['longitude'] = longitude
    # data.drop(["address"])
    # data['full_address'] = full_address
    data['address'] = full_address
    write_data_to_csv(data, city_name)


def remove_data_unit(data):
    beds = data['bed']
    new_beds = []
    for bed in beds:
        if pd.isnull(bed):
            new_beds.append(bed)
        else:
            per = bed.split(" ")[0].strip()
            #     print(per)
            new_beds.append(per)
    data["bed"] = new_beds

    bathes = data['bath']
    new_bathes = []
    for bath in bathes:
        if pd.isnull(bath):
            new_bathes.append(bath)
        else:
            per = bath.strip().split("bath")[0].strip()
            new_bathes.append(per)
    data["bath"] = new_bathes

    cubes = data['cube']
    new_cubes = []
    for cube in cubes:
        if pd.isnull(cube):
            new_cubes.append(cube)
        else:
            per = cube.strip().split("m")[0].strip()
            new_cubes.append(per)
    data['cube'] = new_cubes
    return data


def get_latitude_and_longitude(location, key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?address="
    googel_geo_key = "&key=" + key
    url = base_url + location + googel_geo_key
    r = requests.get(url=url)
    data = r.json()
    return data


def write_data_to_csv(data, city_name):
    data.to_csv(city_name + '_new.csv')


def get_google_key():
    engine = create_engine("mysql://root:root@127.0.0.1:3306/housemarket", pool_size=8)
    DbSession = sessionmaker(bind=engine)
    session = DbSession()
    keys = session.query(Keys).filter_by(key_name='google_key').all()
    key_value = ""
    if len(keys) == 1:
        key_value = keys[0].key_value
    session.close()
    return key_value
# convert_address_to_lat_and_lng("Dublin")

# get_google_key()
