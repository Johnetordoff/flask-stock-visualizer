import csv
import requests


URL = "http://www.nasdaq.com/quotes/nasdaq-100-stocks.aspx?render=download"


def get_data():
    with open('TicketSales.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
 #       for row in reader:
#            print(row['city'])

    return reader

