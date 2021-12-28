from flask import Flask, render_template

from config import db
from models.house import house
from services.scrapeData import getHouseData

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/showHouse')
def hello_world():
    houses = getHouseData()
    # house1 = house(600, 'Area 6', '666666')
    # house2 = house(700, 'Area 7', '7777777')
    # house3 = house(800, 'Area 8', '8888888')
    # house4 = house(900, 'Area 9', '9999999')
    #
    # houses = []
    # houses.append(house1)
    # houses.append(house2)
    # houses.append(house3)
    # houses.append(house4)
    #
    # for item in houses:
    #     print(item.price)
    #     print(item.address)
    totalNum = []
    for num in range(1, (len(houses) // 10) + 1):
        totalNum.append(num)

    return render_template('house.html', houses=houses, totalNum=totalNum)


@app.route('/test')
def test():
    totalNum = []
    for num in range(1, 10):
        totalNum.append(num)
    return render_template('test.html', totalNum=totalNum)


if __name__ == '__main__':
    app.run()


@app.template_filter('sub')
def sub(list, start, end):
    return list[start:end]


@app.route('/demo')
def demo():
    return render_template('demo.html')
