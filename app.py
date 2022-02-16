import json

import pandas as pd
import numpy as np
import statsmodels.api as sm
from flask import Flask, render_template, request, jsonify
from models.house import house
from services.scrapeData import getHouseData, getHouseLocation
from services.data import scrape_data, convert_address_to_lat_and_lng, get_google_key
from collections import OrderedDict
from statsmodels.tsa.arima.model import ARIMA

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/showHouse')
def hello_world():
    houses = getHouseData()
    house1 = house(600, 'Area 6', '666666')
    house2 = house(700, 'Area 7', '7777777')
    house3 = house(800, 'Area 8', '8888888')
    house4 = house(900, 'Area 9', '9999999')

    houses = []
    houses.append(house1)
    houses.append(house2)
    houses.append(house3)
    houses.append(house4)

    for item in houses:
        print(item.price)
        print(item.address)
    total_num = []
    for num in range(1, (len(houses) // 10) + 1):
        total_num.append(num)

    return render_template('house.html', houses=houses, totalNum=total_num)


@app.route('/test')
def test():
    totalNum = []
    for num in range(1, 10):
        totalNum.append(num)
    return render_template('test.html', totalNum=totalNum)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)


@app.template_filter('sub')
def sub(my_list, start, end):
    return my_list[start:end]


@app.route('/demo')
def demo():
    address = "24 the waxworks, Ashtown, Dublin 15"
    address1 = "Park Avenue, Sandymount, Dublin 4"
    address2 = "Champ de Mars, Paris, France"
    location = getHouseLocation(address)
    latitude = location.latitude
    longitude = location.longitude
    return render_template('demo.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/style')
def style():
    # import data
    data = pd.read_csv('data/SecondHand_Property _prices.csv')
    heads = data.columns
    column_names = data.columns.values
    row_data = list(data.values.tolist())
    return render_template('style.html', heads=column_names, row_data=row_data)


@app.route('/highchart')
def highchart():
    # import data
    data = pd.read_csv('data/SecondHand_Property _prices.csv')

    citys = data.columns
    citys = citys[1:len(citys)]

    series = []
    for city in citys:
        cityData = data[city].dropna().apply(convert_currency)
        dd = cityData.to_list()

        dic = {
            "name": city + "",
            "data": dd
        }
        print(dic)
        series.append(dic)
    # print(series)
    return render_template('highchart.html', series=series)


def convert_currency(value):
    new_value = value.replace(',', '')
    return np.float64(new_value)


@app.route('/acf')
def acf():
    # import data
    data = pd.read_csv('data/SecondHand_Property _prices.csv')
    city = 'Dublin'
    data['YEAR'] = pd.to_datetime(data['YEAR'], format='%Y')
    ts = pd.DataFrame(data, columns=['YEAR', city])
    ts.index = ts['YEAR']
    del ts['YEAR']
    ts = ts[city].dropna().apply(convert_currency)
    # plt.figure(figsize=(12, 4))
    # plt.title('secondhand house price')
    # plt.savefig('squares_plot.png')
    # plt.savefig()
    # ts.plot()
    fig = sm.graphics.tsa.plot_acf(ts.dropna(), lags=len(ts.dropna()) - 1)
    fig.set_size_inches(12, 4)
    fig.savefig('squares_plot.png')
    return render_template('acf.html', ts=ts)


@app.route('/adf')
def adf():
    return render_template('adf.html')


def getAdf(ts):
    temp = np.array(ts)
    adf = sm.tsa.stattools.adfuller(temp)
    return adf


@app.route('/ana')
def ana():
    data = pd.read_csv('data/SecondHand_Property _prices.csv')
    city = 'Dublin'
    data['YEAR'] = pd.to_datetime(data['YEAR'], format='%Y')
    ts = pd.DataFrame(data, columns=['YEAR', city])
    ts.index = ts['YEAR']
    del ts['YEAR']
    ts = ts[city].dropna().apply(convert_currency)

    # Logarithmic transformation
    ts_log = np.log(ts.dropna())
    temp1 = np.array(ts_log.dropna())
    log_Adf = getAdf(temp1)

    # moving average
    expwighted_avg = ts_log.ewm(halflife=12).mean()
    temp2 = np.array(expwighted_avg.dropna())
    avg_adf = getAdf(temp2)

    # difference 1
    diff1 = expwighted_avg.diff(3)
    temp3 = np.array(diff1.dropna())
    difference_adf = getAdf(temp3)

    return render_template('ana.html', log_Adf=log_Adf, avg_adf=avg_adf, difference_adf=difference_adf)


@app.route('/model')
def model():
    return render_template('model.html')


@app.route('/monitor')
def monitor():
    # import data
    data = pd.read_csv('data/SecondHand_Property _prices.csv')
    heads = data.columns
    column_names = data.columns.values
    row_data = list(data.values.tolist())

    citys = data.columns
    citys = citys[1:len(citys)]

    series = []
    for city in citys:
        cityData = data[city].dropna().apply(convert_currency)
        dd = cityData.to_list()

        dic = {
            "name": city + "",
            "data": dd
        }
        print(dic)
        series.append(dic)

    city = 'Dublin'
    data['YEAR'] = pd.to_datetime(data['YEAR'], format='%Y')
    ts = pd.DataFrame(data, columns=['YEAR', city])
    ts.index = ts['YEAR']
    del ts['YEAR']
    ts = ts[city].dropna().apply(convert_currency)
    # Logarithmic transformation
    ts_log = np.log(ts.dropna())
    temp1 = np.array(ts_log.dropna())
    log_Adf = getAdf(temp1)

    # moving average
    expwighted_avg = ts_log.ewm(halflife=12).mean()
    temp2 = np.array(expwighted_avg.dropna())
    avg_adf = getAdf(temp2)

    # difference 1
    diff1 = expwighted_avg.diff(3)
    temp3 = np.array(diff1.dropna())
    difference_adf = getAdf(temp3)

    # bulidl model
    arima_model = ARIMA(diff1.dropna(), order=(1, 1, 2))
    model_fit = arima_model.fit()
    # model_fit.summary()

    # Prediction
    predict_ts = model_fit.forecast(16)

    # diff1 restoration
    diff_shift_ts = predict_ts.shift(1).dropna()

    # move restoration
    rol_sum = diff_shift_ts.rolling(window=4).sum()
    rol_recover = rol_sum * 12 - rol_sum.shift(1)

    # log restoration
    log_recover = np.exp(rol_recover)
    log_recover.dropna(inplace=True)
    years = []
    prices = []
    for per in log_recover.index:
        years.append(per.year)
    for per in log_recover:
        prices.append(round(per, 2))
    series_1 = pd.Series(years)
    series_2 = pd.Series(prices)
    prediction_result = pd.DataFrame(columns=['year', 'price'])
    prediction_result['year'] = series_1
    prediction_result['price'] = series_2

    return render_template('monitor.html', heads=column_names, row_data=row_data, series=series, log_Adf=log_Adf,
                           avg_adf=avg_adf, difference_adf=difference_adf, citys=citys,
                           prediction_result=prediction_result, zip=zip)


@app.route("/adf_log", methods=["GET", "POST"])
def adf_log():
    data = pd.read_csv('data/SecondHand_Property _prices.csv')
    city = request.form['city']
    data['YEAR'] = pd.to_datetime(data['YEAR'], format='%Y')
    ts = pd.DataFrame(data, columns=['YEAR', city])
    ts.index = ts['YEAR']
    del ts['YEAR']
    ts = ts[city].dropna().apply(convert_currency)
    # Logarithmic transformation
    ts_log = np.log(ts.dropna())
    temp1 = np.array(ts_log.dropna())
    log_Adf = getAdf(temp1)
    res = jsonify(log_Adf)
    return res


@app.route("/adf_move", methods=["GET", "POST"])
def adf_move():
    data = pd.read_csv('data/SecondHand_Property _prices.csv')
    city = request.form['city']
    data['YEAR'] = pd.to_datetime(data['YEAR'], format='%Y')
    ts = pd.DataFrame(data, columns=['YEAR', city])
    ts.index = ts['YEAR']
    del ts['YEAR']
    ts = ts[city].dropna().apply(convert_currency)
    # Logarithmic transformation
    ts_log = np.log(ts.dropna())
    temp1 = np.array(ts_log.dropna())

    # moving average
    expwighted_avg = ts_log.ewm(halflife=12).mean()
    temp2 = np.array(expwighted_avg.dropna())
    avg_adf = getAdf(temp2)
    res = jsonify(avg_adf)
    return res


@app.route("/adf_diff", methods=["GET", "POST"])
def adf_diff():
    data = pd.read_csv('data/SecondHand_Property _prices.csv')
    city = request.form['city']
    data['YEAR'] = pd.to_datetime(data['YEAR'], format='%Y')
    ts = pd.DataFrame(data, columns=['YEAR', city])
    ts.index = ts['YEAR']
    del ts['YEAR']
    ts = ts[city].dropna().apply(convert_currency)
    # Logarithmic transformation
    ts_log = np.log(ts.dropna())
    temp1 = np.array(ts_log.dropna())

    # moving average
    expwighted_avg = ts_log.ewm(halflife=12).mean()

    # difference 1
    diff1 = expwighted_avg.diff(3)
    temp3 = np.array(diff1.dropna())
    difference_adf = getAdf(temp3)
    res = jsonify(difference_adf)
    return res


@app.route('/go_to_scrape_data', methods=['GET', 'POST'])
def go_to_scrape_data():
    return render_template('scrape_data.html')


@app.route('/go_to_clean_data', methods=['GET', 'POST'])
def go_to_clean_data():
    return render_template('clean_data.html')


# @app.route('/get_data')
@app.route('/scrape_data', methods=['GET', 'POST'])
def scrape_data():
    city_name = request.form['cityName']
    page_number = request.form['pageNumber']
    data_type = request.form['dataType']

    if data_type.__eq__("renting"):
        base_url = "https://www.myhome.ie/rentals/" + city_name + "/property-to-rent?page="
        city_name = city_name + "_rent"
    else:
        # base_url = "https://www.myhome.ie/rentals/dublin/property-to-rent-in-dublin-12?page="
        base_url = "https://www.myhome.ie/residential/dublin/property-for-sale?page="
        city_name = city_name + "_sell"
    # scrape_data(city_name, city_name, page_number, base_url, data_type)

    # import data
    data = pd.read_csv('data/' + city_name + '.csv')
    size = len(data)
    page_size = int(size / 10)
    pages = []
    if page_size > 24:
        pages = list(range(1, 12))
        arrs2 = list(range(page_size - 7, page_size + 1))
        for x in arrs2:
            pages.append(x)
    else:
        pages = list(range(1, size + 1))
    row_data = list(data.values.tolist())
    heads = data.columns
    return render_template('scrape_data.html', row_data=row_data, heads=heads, pages=pages)


@app.route('/clean_data', methods=['GET', 'POST'])
def clean_data():
    city_name = request.form['cityName']
    data_type = request.form['dataType']
    if data_type.__eq__("renting"):
        city_name = city_name + "_rent"
    else:
        city_name = city_name + "_sell"
    key = get_google_key()
    # convert_address_to_lat_and_lng("./data/" + city_name, key)

    # import data
    data = pd.read_csv('data/' + city_name + '_new.csv')
    size = len(data)
    page_size = int(size / 10)
    pages = []
    if page_size > 24:
        pages = list(range(1, 12))
        arrs2 = list(range(page_size - 7, page_size + 1))
        for x in arrs2:
            pages.append(x)
    else:
        pages = list(range(1, size + 1))
    row_data = list(data.values.tolist())
    heads = data.columns
    return render_template('clean_data.html', row_data=row_data, heads=heads, pages=pages)


@app.route('/_add_numbers', methods=['GET', 'POST'])
def add_numbers():
    # import data
    data = pd.read_csv('data/Dublin_rent.csv')
    size = len(data)
    page_size = int(size / 10)
    # page_size = list(range(1, page_size))

    pages = []
    if page_size > 24:
        pages = list(range(1, 12))
        arrs2 = list(range(page_size - 7, page_size + 1))
        for x in arrs2:
            pages.append(x)
    else:
        pages = list(range(1, size + 1))

    column_names = data.columns.values
    row_data = list(data.values.tolist())
    heads = data.columns

    series = []
    for pre_house in row_data:
        bed = pre_house[0]
        bath = pre_house[1]
        cube = pre_house[2]
        home1 = pre_house[3]
        price = pre_house[4]
        area = pre_house[5]
        address = pre_house[6]
        dic = {
            "bed": bed,
            "bath": bath,
            "cube": cube,
            "home": home1,
            "price": price,
            "area": area,
            "address": address
        }
        series.append(dic)
    print("1")
    result = json.dumps(series)
    new_result = {
        "result": result
    }
    return render_template('scrape_data.html', row_data=row_data, heads=heads, pages=pages)


@app.route('/convert_address', methods=['GET', 'POST'])
def convert_address():
    city_name = request.form['cityName']
    data_type = request.form['dataType']
    if data_type.__eq__("renting"):
        city_name = city_name + "_rent"
    else:
        city_name = city_name + "_sell"
    key = get_google_key()
    convert_address_to_lat_and_lng("./data/" + city_name, key)

    return render_template('test.html')


@app.route('/rental_market', methods=['GET', 'POST'])
def rental_market():
    data = pd.read_csv('data/Dublin_rent_new.csv')
    arr = data["home"].value_counts()
    total = sum(arr)
    percentage = []
    indexs = arr.index
    for a in arr:
        percentage.append(round(a / total * 100, 2))
    a = np.array(indexs)
    b = np.array(percentage)
    pie_data = pd.DataFrame(OrderedDict({'type': pd.Series(a), 'percentage': pd.Series(b)})).to_json(orient="records")
    pie_data = json.loads(pie_data)

    # bed number presentage
    bed_pie_data = get_bed_pie_data(data)
    bath_pie_data = get_bath_pie_data(data)
    area_percentage_data = get_area_percentage_data(data)
    return render_template('rental_market.html', pie_data=pie_data, bed_pie_data=bed_pie_data,
                           bath_pie_data=bath_pie_data, area_percentage_data=area_percentage_data)


@app.route('/sell_house_pie', methods=['GET', 'POST'])
def sell_house_pie():
    data = pd.read_csv('data/Dublin_sell.csv')
    arr = data["home"].value_counts()
    total = sum(arr)
    percentage = []
    indexs = arr.index
    for a in arr:
        percentage.append(round(a / total * 100, 2))
    a = np.array(indexs)
    b = np.array(percentage)
    pie_data = pd.DataFrame(OrderedDict({'type': pd.Series(a), 'percentage': pd.Series(b)})).to_json(orient="records")
    pie_data = json.loads(pie_data)

    # Regional housing ratio
    area_arr = data["area"].value_counts().to_frame()
    area_arr = area_arr.drop(area_arr[area_arr['area'] < 10].index)
    area_arr_new = area_arr["area"]

    area_arr_total = sum(arr)
    area_percentage = []
    area_indexs = area_arr_new.index
    for per in area_arr_new:
        area_percentage.append(round(per / area_arr_total * 100, 2))

    area_ser = np.array(area_indexs)
    percentage_ser = np.array(area_percentage)
    area_pie_data = pd.DataFrame(
        OrderedDict({'area': pd.Series(area_ser), 'percentage': pd.Series(percentage_ser)})).to_json(orient="records")
    area_pie_data = json.loads(area_pie_data)

    return render_template('selling_house_pie.html', pie_data=pie_data, area_pie_data=area_pie_data)


def get_bed_pie_data(data):
    bed_arr = data["bed"].value_counts()
    bed_total = sum(bed_arr)
    bed_percentage = []
    bed_indexs = np.int_(bed_arr.index)
    for a in bed_arr:
        bed_percentage.append(round(a / bed_total * 100, 2))
    bed_a = np.array(bed_indexs)
    bed_b = np.array(bed_percentage)
    bed_pie_data = pd.DataFrame(OrderedDict({'type': pd.Series(bed_a), 'percentage': pd.Series(bed_b)})).to_json(
        orient="records")
    bed_pie_data = json.loads(bed_pie_data)
    return bed_pie_data


def get_bath_pie_data(data):
    bath_arr = data["bath"].value_counts()
    bath_total = sum(bath_arr)
    bath_percentage = []
    bath_indexs = np.int_(bath_arr.index)
    for a in bath_arr:
        bath_percentage.append(round(a / bath_total * 100, 2))
    bath_a = np.array(bath_indexs)
    bath_b = np.array(bath_percentage)
    bath_pie_data = pd.DataFrame(OrderedDict({'type': pd.Series(bath_a), 'percentage': pd.Series(bath_b)})).to_json(
        orient="records")
    bath_pie_data = json.loads(bath_pie_data)
    return bath_pie_data


def get_area_percentage_data(data):
    area_arr = data["area"].value_counts().to_frame()
    area_arr = area_arr.drop(area_arr[area_arr['area'] < 10].index)
    area_arr_new = area_arr["area"]
    arr = data["area"].value_counts()
    area_arr_total = sum(arr)
    area_percentage = []
    area_indexs = area_arr_new.index
    for per in area_arr_new:
        area_percentage.append(round(per / area_arr_total * 100, 2))

    area_ser = np.array(area_indexs)
    percentage_ser = np.array(area_percentage)
    area_pie_data = pd.DataFrame(
        OrderedDict({'type': pd.Series(area_ser), 'percentage': pd.Series(percentage_ser)})).to_json(orient="records")
    area_pie_data = json.loads(area_pie_data)
    return area_pie_data


@app.route('/data', methods=['GET', 'POST'])
def data():
    return render_template('scrape_data.html')
