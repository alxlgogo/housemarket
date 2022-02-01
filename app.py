import pandas as pd
import numpy as np
import statsmodels.api as sm
from flask import Flask, render_template, request, jsonify
from models.house import house
from services.scrapeData import getHouseData, getHouseLocation
from services.data import scrape_data, convert_address_to_lat_and_lng, get_google_key

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

    return render_template('monitor.html', heads=column_names, row_data=row_data, series=series, log_Adf=log_Adf,
                           avg_adf=avg_adf, difference_adf=difference_adf, citys=citys, zip=zip)


@app.route("/adf_log", methods=["GET", "POST"])
def adf_log():
    data = pd.read_csv('data/SecondHand_Property _prices.csv')
    city = request.form['city'];
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


@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
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
    scrape_data(city_name, city_name, page_number, base_url,data_type)
    return render_template('test.html')


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
